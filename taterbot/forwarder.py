import functools
from typing import Final

from discord import ApplicationContext, Embed, Emoji, Message
from discord.channel import DMChannel, TextChannel

from taterbot import utils
from taterbot.bot import TaterBot


class Forwarder:
    def __init__(
        self,
        bot: TaterBot,
        message: Message,
        ctx: ApplicationContext,
    ) -> None:
        self.ctx: Final[ApplicationContext] = ctx
        self.message: Final[Message] = message
        self.success_emoji: Final[Emoji] = bot.emoji
        self.embed_color: Final[int] = message.author.color.value or bot.color_value

        create_embed = functools.partial(utils.create_embed_for_message, message)
        self.embed_for_destination: Final[Embed] = create_embed(link=False)
        self.embed_for_source: Final[Embed] = create_embed()

        self.destination_channel: TextChannel | DMChannel | None = None
        self.source_response_content: str = "Forwarded a message"

        if (user := self.ctx.user).id != message.author.id:
            self.source_response_content += f" from {message.author.mention}"
            for embed in (self.embed_for_destination, self.embed_for_source):
                embed.set_footer(text=f"Forwarded by {user}", icon_url=user.avatar.url)

    def set_destination(self, channel: TextChannel | DMChannel | None) -> None:
        if isinstance(channel, TextChannel):
            channel_label = utils.get_channel_display_name(channel, self.ctx.user)
        elif isinstance(channel, DMChannel):
            channel_label = channel.recipient.mention
        else:
            return

        self.source_response_content += f" to {channel_label}."
        self.destination_channel = channel

    async def execute(self) -> None:
        if not self.destination_channel:
            raise type(self).DestinationError

        separate_channels = self.destination_channel.id != self.ctx.channel.id
        message_embeds = utils.get_embeds_from_message(self.message, self.embed_color)

        if separate_channels:
            await self.destination_channel.send(
                embeds=[self.embed_for_destination, *message_embeds],
                files=await utils.get_files_from_message(self.message),
            )

        await utils.edit_or_respond(
            self.ctx,
            content=self.source_response_content if separate_channels else None,
            embeds=[self.embed_for_source, *message_embeds],
            files=await utils.get_files_from_message(self.message),
        )
        await self.message.add_reaction(self.success_emoji)

    class DestinationError(Exception):
        def __init__(self) -> None:
            super().__init__("Cannot forward a message without setting a destination.")
