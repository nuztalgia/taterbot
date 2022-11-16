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
reaction_error_embed: Final[Embed] = utils.create_error_embed(
    title="I already forwarded that message!",
    description="(You can tell by the reaction I added to it.)",
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

        for reaction in message.reactions:
            reaction_user_ids = [user.id for user in await reaction.users().flatten()]
            if self.bot.user.id in reaction_user_ids:  # reaction.me wasn't consistent.
                await ctx.respond(embed=reaction_error_embed, ephemeral=True)
                Log.d("Will not forward a message that has this bot's reaction on it.")
                return

        forwarder = Forwarder(self.bot, message, ctx)
        is_in_home_guild = ctx.guild_id == self.bot.home_guild.id

        if is_in_home_guild or (not ctx.guild):
            if ctx.user.id != self.bot.owner_id:
                user, owner = ctx.user.mention, f"<@{self.bot.owner_id}>"
                await ctx.respond(f"Sorry {user}, I only answer to {owner}! :innocent:")
                Log.d("Refusing to let non-owner forward message from DM / home guild.")
                return

            await ctx.defer(ephemeral=True)
            source_text = "in home guild" if is_in_home_guild else "via DM"
            Log.i(f"Received command from bot owner {source_text}. Forwarding message.")

            prompt = "To which channel should I forward this message?"
            forwarder.set_destination(
                await self.bot.get_text_channel(ctx, prompt=prompt)
            )
        else:
            time_delta = utils.utcnow() - message.created_at
            await ctx.defer(ephemeral=time_delta < timedelta(seconds=60 * 5))

            Log.i("Received command in external guild. Forwarding message to owner.")
            forwarder.set_destination(self.bot.owner.dm_channel)

        try:
            await forwarder.execute(ctx)
        except Forwarder.DestinationError:
            Log.e("Could not determine a destination channel for the message.")
            await ctx.respond(embed=channel_error_embed)


def setup(bot: TaterBot) -> None:
    bot.add_cog(MessageCommands(bot))
