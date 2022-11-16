from functools import cached_property
from typing import Final

from discord import ApplicationContext, Embed, Emoji, File, Member, Message, User
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

        self.embed_for_dst: Final[Embed] = self._create_embed_for_message()
        self.embed_for_src: Final[Embed] = self._create_embed_for_message(link=True)

        self.dst_channel: TextChannel | DMChannel | None = dst_channel
        self.src_response_content: str = "" if dst_channel else "Forwarded a message"

        if self.user.id != message.author.id:
            self.src_response_content += f" from {message.author.mention}"

    @cached_property
    def _header_template(self) -> str:
        if self.message.guild:
            channel_label = utils.get_channel_loggable_name(self.message.channel)
            return f"Message from $user in {channel_label}"
        else:
            return "DM from $user"

    @cached_property
    def _footer_kwargs(self) -> dict[str, str]:
        kwargs = {"text": str(self.user)}

        if self.user.id != self.message.author.id:
            kwargs["text"] += f" 🗘 {self.message.author}"
            kwargs["icon_url"] = self.user.avatar.url

        return kwargs

    @cached_property
    def _original_message_embeds(self) -> list[Embed]:
        embeds = []
        unset_colors = (utils.NO_COLOR, Embed.Empty)
        should_set_colors = self.embed_color not in unset_colors

        for sticker in self.message.stickers:
            sticker_embed = utils.create_embed(
                title=f"{sticker.name} (Sticker)", color=self.embed_color
            ).set_image(url=sticker.url)
            embeds.append(sticker_embed)

        for embed in self.message.embeds:
            if should_set_colors and (embed.color in unset_colors):
                embed.colour = self.embed_color
            embeds.append(embed)

        embeds.extend(self.message.embeds)
        return embeds

    def _create_embed_for_message(self, *, link: bool = False) -> Embed:
        return utils.create_embed_for_author(
            self.message.author,
            description=self.message.content,
            header_template=self._header_template,
            header_link_url=self.message.jump_url if link else None,
            color=self.embed_color,
            timestamp=self.message.created_at,
        ).set_footer(**self._footer_kwargs)

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

        if different_channels := (self.dst_channel.id != self.src_channel_id):
            await self.dst_channel.send(
                embeds=[self.embed_for_dst, *self._original_message_embeds],
                files=await self._get_files_from_message(),
            )

        if ctx:
            await utils.edit_or_respond(
                ctx,
                content=self.src_response_content if different_channels else None,
                embeds=[self.embed_for_src, *self._original_message_embeds],
                files=await self._get_files_from_message(),
            )

        await self.message.add_reaction(self.success_emoji)

    async def _get_files_from_message(self) -> list[File]:
        return [
            (await attachment.to_file(use_cached=True))
            for attachment in self.message.attachments
        ]

    class DestinationError(Exception):
        def __init__(self) -> None:
            super().__init__("Cannot forward a message without setting a destination.")
