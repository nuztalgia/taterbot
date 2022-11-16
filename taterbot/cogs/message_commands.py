import functools
from datetime import timedelta
from typing import Final

from discord import ApplicationContext, Cog, Embed, Emoji, Message
from discord.channel import DMChannel, TextChannel
from discord.commands import message_command

from taterbot import Log, TaterBot, utils

message_error_embed: Final[Embed] = utils.create_error_embed(
    title="Ummm...",
    description="Why do you want me to forward my own message?"
    "\nYou're making me feel self-conscious! :flushed:",
)
channel_error_embed: Final[Embed] = utils.create_error_embed(
    "Ummm... I couldn't figure out where to deliver that message."
    "\nPlease update my `channels`, then try forwarding it again!"
)


class MessageCommands(Cog):
    def __init__(self, bot: TaterBot) -> None:
        self.bot: Final[TaterBot] = bot

    @message_command(name="Forward Message")
    async def forward_message(self, ctx: ApplicationContext, message: Message) -> None:
        if message.author.id == self.bot.user.id:
            await ctx.respond(embed=message_error_embed, ephemeral=True)
            Log.d("Will not forward a message that was originally sent by this bot.")
            return

        cmd = _ForwardMessageCommand(self.bot, ctx, message)

        if cmd.is_in_private_channel:
            if not cmd.is_from_owner:
                Log.d("Refusing to let non-owner forward message from DM / home guild.")
                user, owner = ctx.user.mention, f"<@{self.bot.owner_id}>"
                await ctx.respond(f"Sorry {user}, I only answer to {owner}! :innocent:")
                return

            await ctx.defer(ephemeral=True)
            source_text = "in home guild" if cmd.is_in_home_guild else "via DM"
            Log.d(f"Received command from bot owner {source_text}. Forwarding message.")

            prompt = "To which channel should I forward this message?"
            cmd.set_destination(await self.bot.get_text_channel(ctx, prompt=prompt))
        else:
            time_delta = utils.utcnow() - message.created_at
            await ctx.defer(ephemeral=time_delta < timedelta(seconds=60 * 5))

            Log.d("Received command in external guild. Forwarding message to owner.")
            cmd.set_destination(self.bot.owner.dm_channel)

        if not cmd.destination_channel:
            Log.e("Could not determine a destination channel for the message.")
            await ctx.respond(embed=channel_error_embed)
            return

        await cmd.execute()
        Log.d("Successfully forwarded the message.")


class _ForwardMessageCommand:
    def __init__(
        self,
        bot: TaterBot,
        ctx: ApplicationContext,
        message: Message,
    ) -> None:
        self.ctx: Final[ApplicationContext] = ctx
        self.message: Final[Message] = message
        self.success_emoji: Final[Emoji] = bot.emoji
        self.embed_color: Final[int] = message.author.color.value or bot.color_value

        self.is_from_owner: Final[bool] = ctx.user.id == bot.owner_id
        self.is_in_home_guild: Final[bool] = ctx.guild_id == bot.home_guild.id
        self.is_in_private_channel: Final[bool] = self.is_in_home_guild or not ctx.guild

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
            raise TypeError(
                "Can't execute 'Forward Message' command without 'destination_channel'."
            )

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


def setup(bot: TaterBot) -> None:
    bot.add_cog(MessageCommands(bot))
