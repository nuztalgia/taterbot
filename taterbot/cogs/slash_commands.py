from typing import Final

from discord import ApplicationContext, ButtonStyle, Cog, option, slash_command
from discord.abc import Messageable
from discord.utils import utcnow
from uikitty import dynamic_select

from taterbot import Config, Log, TaterBot, utils


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

    @slash_command(
        description="Send a goodbye message and log out.",
        guild_ids=[Config.home_id],
    )
    @option(
        "message",
        default="",
        description="The message to send. If omitted, will not send a public message.",
    )
    async def signoff(self, ctx: ApplicationContext, message: str) -> None:
        if ctx.user.id != self.bot.owner_id:
            response_gif = utils.get_asset_file("you-think-you-can-stop-me.gif")
            await ctx.respond(file=response_gif)
            return

        if message:
            other_channel_keys = [
                channel_key
                for channel_key, channel in self.bot.known_channels.items()
                if channel.id != ctx.channel.id
            ]
            if other_channel_keys:
                await self._announce_signoff(ctx, message, other_channel_keys)
            else:
                Log.d("There are no channels available for announcing signoff.")

        send_final_message = ctx.channel.send if ctx.response.is_done() else ctx.respond
        content = f"Signing off. Bye for now, {self.bot.owner.mention} {self.bot.emoji}"
        await send_final_message(content=content)

        Log.i(f"Logging out and shutting down.")
        await self.bot.close()

    async def _announce_signoff(
        self, ctx: ApplicationContext, message: str, channel_keys: list[str]
    ) -> None:
        destination_channel_key = await dynamic_select(
            ctx,
            *channel_keys,
            content=f"Which channel should I send your goodbye message to?",
            button_style=ButtonStyle.primary,
            log=Log.d,
        )
        destination_channel = self.bot.known_channels[destination_channel_key]
        edit_or_respond = ctx.edit if ctx.response.is_done() else ctx.respond

        display_name = utils.get_channel_display_name(destination_channel, ctx.user)
        loggable_name = utils.get_loggable_channel_name(destination_channel)

        if isinstance(destination_channel, Messageable):
            Log.d(f"Delivering a goodbye message to {loggable_name}.")

            # noinspection PyTypeChecker
            embed = utils.create_embed_for_author(
                self.bot.user,
                description=f"> {message}",
                header_template="$user is signing off!",
                timestamp=utcnow(),
            ).set_footer(text=f"—  {self.bot.owner}")

            await destination_channel.send(embed=embed)
            success_message = f"Delivered this message to {display_name}."
            await edit_or_respond(content=success_message, embed=embed, view=None)
        else:
            error_message = f"Selected channel ({display_name}) is not messageable."
            await edit_or_respond(
                content=None, embed=utils.create_error_embed(error_message), view=None
            )


def setup(bot: TaterBot) -> None:
    bot.add_cog(SlashCommands(bot))
