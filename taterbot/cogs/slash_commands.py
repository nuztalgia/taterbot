from typing import Final

from discord import ApplicationContext, Cog, slash_command

from taterbot import Log, TaterBot, utils


class SlashCommands(Cog):
    def __init__(self, bot: TaterBot) -> None:
        self.bot: Final[TaterBot] = bot

    @slash_command(description="Make fetch happen.")
    async def fetch(self, ctx: ApplicationContext) -> None:
        if ctx.user.id == self.bot.owner_id:
            await ctx.response.defer(invisible=False)

            Log.d("Triggering a re-fetch of all custom bot attributes.")
            await self.bot.make_fetch_happen()

            Log.i("Successfully re-fetched all custom bot attributes.")
            self.bot.log_attributes()
            file_to_send = "that-is-so-fetch.gif"
        else:
            file_to_send = "stop-trying-to-make-fetch-happen.gif"

        await ctx.respond(file=utils.get_asset_file(file_to_send))


def setup(bot: TaterBot) -> None:
    bot.add_cog(SlashCommands(bot))
