from functools import cached_property
from string import Template
from typing import Final

import emoji
from discord import ApplicationContext, Cog, TextChannel
from discord.commands import option, slash_command
from discord.errors import Forbidden

from taterbot import Config, Log, TaterBot, utils

_ABOUT: Final[list[tuple[str, Template]]] = [
    (f"\n** **\n{emoji.emojize(title_emoji)}\u2009\u2002{title_text}", description)
    for (title_emoji, title_text), description in {
        (":postbox:", "What I Do"): Template(
            "I deliver messages to/from ${bot_owner}, but only when I'm **online** and "
            "told to do so. To let me know that I should pass a message along, you can "
            "directly mention me (${bot_user}) in it, or right-click on it and select "
            "`Apps > Forward Message`."
        ),
        (":alarm_clock:", "When I Woke Up"): Template(
            "I've currently been **online** since ${start_time}."
        ),
        (":construction_site:", "How I Work"): Template(
            "I'm completely open-source! Check out my code and documentation on "
            "[GitHub](https://github.com/nuztalgia/taterbot)."
        ),
    }.items()
]


class SlashCommands(Cog):
    def __init__(self, bot: TaterBot) -> None:
        self.bot: Final[TaterBot] = bot

    @cached_property
    def _about(self) -> list[tuple[str, str]]:
        kwargs = {
            "bot_owner": self.bot.owner.mention,
            "bot_user": self.bot.user.mention,
            "start_time": utils.format_time(self.bot.started_at),
        }
        return [
            (title, description.safe_substitute(**kwargs))
            for title, description in _ABOUT
        ]

    @slash_command(description="Show information about this bot.")
    async def about(self, ctx: ApplicationContext) -> None:
        embed = self.bot.create_branded_embed(
            description=Config.about_message,
            header_template="Hello there! My name is $user.",
        )

        for title, description in self._about:
            embed.add_field(name=title, value=description, inline=False)

        await ctx.respond(embed=embed)

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
            channel = await self.bot.get_text_channel(
                ctx, prompt="Where should I send your goodbye message?", ephemeral=False
            )
            message_delivered = False

            if channel:
                message_delivered = await self._announce_signoff(ctx, channel, message)
            else:
                Log.e(f"A signoff message was provided, but no channels are available.")
                error_embed = utils.create_error_embed(
                    "Umm... I don't know where to send your goodbye message.\nPlease "
                    "update my `channels`, or run `/signoff` again without a message!"
                )
                await utils.edit_or_respond(ctx, embed=error_embed)

            if not message_delivered:
                return

        send_final_message = ctx.channel.send if ctx.response.is_done() else ctx.respond
        content = f"Signing off. Bye for now, {self.bot.owner.mention} {self.bot.emoji}"
        await send_final_message(content=content)

        Log.i(f"Logging out and shutting down.")
        await self.bot.close()

    async def _announce_signoff(
        self,
        ctx: ApplicationContext,
        channel: TextChannel,
        message: str,
    ) -> bool:
        channel_display_name = utils.get_channel_display_name(channel, ctx.user)
        channel_loggable_name = utils.get_channel_loggable_name(channel)

        try:
            Log.i(f"Delivering a goodbye message to {channel_loggable_name}.")

            embed = self.bot.create_branded_embed(
                description=f"> {message}",
                header_template="$user is signing off!",
                timestamp=utils.utcnow(),
            ).set_footer(text=f"—  {self.bot.owner}")

            await channel.send(embed=embed)
        except Forbidden:
            Log.e(f"Missing permission(s) to send message to {channel_loggable_name}.")
            error_embed = utils.create_error_embed(
                f"I'm not allowed to send messages in {channel_display_name}.\n"
                "Please make sure I have the correct permissions, then try again!"
            )
            await utils.edit_or_respond(ctx, embed=error_embed)
            return False

        await utils.edit_or_respond(
            ctx,
            content=f"I delivered your message to {channel_display_name}:",
            embed=embed,
        )
        return True


def setup(bot: TaterBot) -> None:
    bot.add_cog(SlashCommands(bot))
