from datetime import datetime
from functools import cached_property
from pathlib import Path
from typing import Any, Final

from botstrap import Color
from discord import Bot, Embed, Emoji, Guild, Message, TextChannel, User
from discord.abc import GuildChannel
from discord.commands import ApplicationContext
from discord.enums import ButtonStyle
from discord.errors import Forbidden
from discord.flags import Intents
from uikitty import dynamic_select

from taterbot import utils
from taterbot.config import Config
from taterbot.log import Log


# noinspection PyDunderSlots, PyUnresolvedReferences
def _get_required_intents() -> Intents:
    intents = Intents.default()
    intents.members = True
    intents.message_content = True
    return intents


# noinspection PyAbstractClass
class TaterBot(Bot):
    def __init__(self, force_sync: bool, **options: Any) -> None:
        super().__init__(
            intents=_get_required_intents(),
            owner_id=Config.owner_id,
            **options,
        )

        self.owner: User = self.get_user(self.owner_id)
        self.home_guild: Guild = self.get_guild(Config.home_id)
        self.emoji: Emoji = self.get_emoji(Config.emoji_id)

        self.known_channels: Final[dict[str, GuildChannel]] = {}
        self.known_users: Final[dict[str, User]] = {}
        self.started_at: Final[datetime] = utils.utcnow()

        self._force_sync: Final[bool] = force_sync
        self._initialized: bool = False
        self._messages_forwarded: int = 0

        for file_path in Path(__file__).parent.glob("cogs/[!_]*.py"):
            Log.d(f"Loading extension '{file_path.stem}'.")
            self.load_extension(f"taterbot.cogs.{file_path.stem}")

    @property
    def messages_forwarded(self) -> str:
        plural = self._messages_forwarded != 1
        return f"**{self._messages_forwarded}** message{'s' if plural else ''}"

    @cached_property
    def color_value(self) -> int:
        color = utils.get_color_value(Config.accent_color)
        if color != utils.NO_COLOR:
            return color
        elif accent_color := self.user.accent_color:
            return accent_color.value
        else:
            return utils.NO_COLOR

    def create_branded_embed(self, **kwargs: Any) -> Embed:
        if "color" not in kwargs:
            kwargs["color"] = self.color_value
        return utils.create_embed_for_author(self.user, **kwargs)

    def get_channel_keys(
        self, *allowed_types: type[GuildChannel], exclude_id: int = 0
    ) -> list[str]:
        if not allowed_types:
            allowed_types = (GuildChannel,)
        return [
            channel_key
            for channel_key, channel in self.known_channels.items()
            if (isinstance(channel, allowed_types) and (channel.id != exclude_id))
        ]

    async def get_text_channel(
        self,
        ctx: ApplicationContext,
        prompt: str = "Select a channel:",
        exclude_current_channel: bool = True,
        button_style: ButtonStyle = ButtonStyle.primary,
    ) -> TextChannel | None:
        exclude_id = ctx.channel.id if exclude_current_channel else 0
        keys = self.get_channel_keys(TextChannel, exclude_id=exclude_id)

        selected_channel_key = await dynamic_select(
            ctx, *keys, content=prompt, button_style=button_style, log=Log.d
        )
        channel = self.known_channels.get(selected_channel_key)
        return channel if isinstance(channel, TextChannel) else None

    def log_attributes(self, prefix: str = "  - ") -> None:
        loggable_home_guild = self.home_guild.name + Color.grey(
            f" (Members: {self.home_guild.approximate_member_count})"
        )
        loggable_channels = utils.dict_to_str(
            self.known_channels, utils.get_channel_loggable_name
        )
        loggable_users = utils.dict_to_str(self.known_users)

        for attribute_name, attribute_value in [
            ("Owner", self.owner),
            ("Home Guild", loggable_home_guild),
            ("Known Channels", loggable_channels),
            ("Known Users", loggable_users),
            ("Signature Emoji", f":{self.emoji.name}:"),
        ]:
            Log.i(f"{Color.cyan(f'{prefix}{attribute_name}:')} {attribute_value}")

        Log.d("Finished logging bot attributes.")

    # noinspection PyPropertyAccess, PyProtectedMember
    async def make_fetch_happen(self) -> None:
        if self._initialized:
            Log.d(f"Reloading config from '{Config._file_path}'.")
            Config.reload_from_file()
            del self.color_value  # Invalidate the cached property.
        else:
            Log.d(f"Loaded config from '{Config._file_path}'.")

        if self._initialized or not self.owner:
            Log.d("Fetching bot owner user.")
            self.owner = await self.get_or_fetch_user(self.owner_id)
            await self.owner.create_dm()

        if self._initialized or not self.home_guild:
            Log.d("Fetching home guild/server.")
            self.home_guild = await self.fetch_guild(Config.home_id)

        if self._initialized or not self.emoji:
            Log.d("Fetching signature emoji from home guild.")
            self.emoji = await self.home_guild.fetch_emoji(Config.emoji_id)

        self.known_channels.clear()
        for channel_key, channel_id in Config.channels.items():
            await self._cache_channel(channel_key, channel_id)

        self.known_users.clear()
        for user_key, user_id in Config.users.items():
            await self._cache_user(user_key, user_id)

    async def _cache_channel(self, channel_key: str, channel_id: int) -> None:
        try:
            if self._initialized or not (channel := self.get_channel(channel_id)):
                Log.d(f"Fetching known channel '{channel_key}'.")
                channel = await self.fetch_channel(channel_id)
            self.known_channels[channel_key] = channel
        except Forbidden:
            Log.w(f"Missing access to channel '{channel_key}'.")

    async def _cache_user(self, user_key: str, user_id: int) -> None:
        if self._initialized or not (user := self.get_user(user_id)):
            Log.d(f"Fetching known user '{user_key}'.")
            user = await self.fetch_user(user_id)
        self.known_users[f"@{user_key}"] = user

    # noinspection PyMethodMayBeStatic
    async def on_application_command(self, ctx: ApplicationContext) -> None:
        command_name = ctx.command.qualified_name
        channel_name = utils.get_channel_loggable_name(ctx.channel)
        Log.i(f"{ctx.user} used command '{command_name}' in {channel_name}.")

    async def on_message_forwarded(self, message: Message) -> None:
        await message.add_reaction(self.emoji)
        Log.d(f"Successfully forwarded message {message.id}.")
        self._messages_forwarded += 1

    async def on_ready(self) -> None:
        if self._initialized:
            Log.i("Received another 'on_ready' event. Ignoring.")
            return

        if self._force_sync:
            Log.w("Force-syncing commands. Be mindful of the rate limit.")
            await self.sync_commands(force=True)

        await self.make_fetch_happen()
        self._initialized = True

        Log.i("TaterBot is online and ready!")
        self.log_attributes()
