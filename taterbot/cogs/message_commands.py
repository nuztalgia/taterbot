from datetime import timedelta
from typing import Final

from discord import ApplicationContext, Cog, Embed, Message
from discord.commands import message_command

from taterbot import Forwarder, Log, TaterBot, utils

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

        fwd = Forwarder(self.bot, ctx, message)

        if fwd.is_in_private_channel:
            if not fwd.is_from_owner:
                Log.d("Refusing to let non-owner forward message from DM / home guild.")
                user, owner = ctx.user.mention, f"<@{self.bot.owner_id}>"
                await ctx.respond(f"Sorry {user}, I only answer to {owner}! :innocent:")
                return

            await ctx.defer(ephemeral=True)
            source_text = "in home guild" if fwd.is_in_home_guild else "via DM"
            Log.d(f"Received command from bot owner {source_text}. Forwarding message.")

            prompt = "To which channel should I forward this message?"
            fwd.set_destination(await self.bot.get_text_channel(ctx, prompt=prompt))
        else:
            time_delta = utils.utcnow() - message.created_at
            await ctx.defer(ephemeral=time_delta < timedelta(seconds=60 * 5))

            Log.d("Received command in external guild. Forwarding message to owner.")
            fwd.set_destination(self.bot.owner.dm_channel)

        try:
            await fwd.execute()
        except Forwarder.DestinationError:
            Log.e("Could not determine a destination channel for the message.")
            await ctx.respond(embed=channel_error_embed)
        else:
            Log.d("Successfully forwarded the message.")


def setup(bot: TaterBot) -> None:
    bot.add_cog(MessageCommands(bot))
