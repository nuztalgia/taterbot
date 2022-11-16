import functools
from typing import Final

from discord import ApplicationContext, Embed, Emoji, Member, Message, User
from discord.channel import DMChannel, TextChannel

from taterbot import utils
from taterbot.bot import TaterBot


class Forwarder:
    def __init__(
        self,
        bot: TaterBot,
        message: Message,
        ctx: ApplicationContext | None = None,
        dst_channel: TextChannel | DMChannel | None = None,
    ) -> None:
        self.message: Final[Message] = message
        self.user: Final[Member | User] = (ctx and ctx.user) or message.author
        self.src_channel_id: Final[int] = (ctx and ctx.channel.id) or message.channel.id
        self.embed_color: Final[int] = message.author.color.value or bot.color_value
        self.success_emoji: Final[Emoji] = bot.emoji

        create_embed = functools.partial(utils.create_embed_for_message, message)
        self.embed_for_dst: Final[Embed] = create_embed(link=False)
        self.embed_for_src: Final[Embed] = create_embed()

        self.dst_channel: TextChannel | DMChannel | None = dst_channel
        self.src_response_content: str = "" if dst_channel else "Forwarded a message"

        if self.user.id != message.author.id:
            for embed in (self.embed_for_dst, self.embed_for_src):
                embed.set_footer(
                    text=f"Forwarded by {self.user}", icon_url=self.user.avatar.url
                )
            self.src_response_content += f" from {message.author.mention}"

    def set_destination(self, channel: TextChannel | DMChannel | None) -> None:
        if isinstance(channel, DMChannel):
            channel_label = channel.recipient.mention
        elif isinstance(channel, TextChannel):
            channel_label = utils.get_channel_display_name(channel, self.user)
        else:
            return

        self.src_response_content += f" to {channel_label}."
        self.dst_channel = channel

    async def execute(self, ctx: ApplicationContext | None = None) -> None:
        if not self.dst_channel:
            raise type(self).DestinationError

        different_channels = self.dst_channel.id != self.src_channel_id
        message_embeds = utils.get_embeds_from_message(self.message, self.embed_color)
        get_files = functools.partial(utils.get_files_from_message, self.message)

        if different_channels:
            await self.dst_channel.send(
                embeds=[self.embed_for_dst, *message_embeds],
                files=await get_files(),
            )

        if ctx:
            await utils.edit_or_respond(
                ctx,
                content=self.src_response_content if different_channels else None,
                embeds=[self.embed_for_src, *message_embeds],
                files=await get_files(),
            )
        await self.message.add_reaction(self.success_emoji)

    class DestinationError(Exception):
        def __init__(self) -> None:
            super().__init__("Cannot forward a message without setting a destination.")
