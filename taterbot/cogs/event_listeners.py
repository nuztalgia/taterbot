from typing import Final

from discord import Cog, Message

from taterbot import Forwarder, Log, TaterBot, utils


class EventListeners(Cog):
    def __init__(self, bot: TaterBot) -> None:
        self.bot: Final[TaterBot] = bot

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message.author.id == self.bot.user.id:
            return  # Completely ignore all messages that were sent by the bot.

        if message.guild and (self.bot.user not in message.mentions):
            return  # Completely ignore all non-DM messages that don't @mention the bot.

        channel_loggable_name = utils.get_channel_loggable_name(message.channel)
        ping_info = f"a ping from {message.author} in {channel_loggable_name}"

        is_self = message.author.id in (self.bot.user.id, self.bot.owner_id)
        if is_self or (message.guild and (message.guild.id == self.bot.home_guild.id)):
            Log.d(f"Ignoring {ping_info}.")
            return  # Do not forward messages 1) from bot owner, or 2) in home guild.

        Log.i(f"Received {ping_info}. Forwarding message to owner.")
        forwarder = Forwarder(self.bot, message, dst_channel=self.bot.owner.dm_channel)
        await forwarder.execute()


def setup(bot: TaterBot) -> None:
    bot.add_cog(EventListeners(bot))
