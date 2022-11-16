import re
from collections.abc import Callable
from datetime import datetime
from functools import partial
from string import Template
from typing import Any, Final

import emoji
import humanize
from discord import ApplicationContext, ChannelType, Color, Embed, File, Member
from discord.abc import GuildChannel
from discord.ui import View
from discord.user import ClientUser, User
from discord.utils import utcnow

NO_COLOR: Final[int] = -1

_sanitize_channel_name: Final[Callable[[str], str]] = partial(
    re.compile(r"(:[\w-]+:|^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$)", re.ASCII).sub, ""
)


def _pop_color(kwargs_dict: dict[str, Any]) -> Color | int:
    for key in ("color", "colour"):
        if key in kwargs_dict:
            return kwargs_dict.pop(key)
    return NO_COLOR


def create_embed(description: str = "", *, title: str = "", **kwargs: Any) -> Embed:
    color = _pop_color(kwargs)
    return Embed(
        color=color if (color != NO_COLOR) else Embed.Empty,
        title=title or Embed.Empty,
        description=description or Embed.Empty,
        **kwargs,
    )


def create_embed_for_author(
    user: ClientUser | Member | User,
    description: str = "",
    *,
    header_template: str = "$user",
    header_link_url: str | None = None,
    **kwargs: Any,
) -> Embed:
    color = _pop_color(kwargs)

    if (color == NO_COLOR) and isinstance(user, Member):
        color = user.color

    return create_embed(description, color=color, **kwargs).set_author(
        name=Template(header_template).substitute(user=user.display_name),
        url=header_link_url or Embed.Empty,
        icon_url=user.avatar.url,
    )


def create_error_embed(
    description: str = "",
    *,
    title: str = "Something went wrong!",
) -> Embed:
    return create_embed(description, title=title, color=Color.brand_red())


async def edit_or_respond(
    ctx: ApplicationContext,
    *,
    content: str | None = None,
    embed: Embed | None = None,
    view: View | None = None,
    **kwargs: Any,
) -> None:
    embeds = [
        _embed
        for _embed in [embed, kwargs.pop("embed", None), *kwargs.pop("embeds", [])]
        if isinstance(_embed, Embed)
    ]
    func = ctx.edit if ctx.response.is_done() else ctx.respond
    await func(content=content, embeds=embeds, view=view, **kwargs)


def format_time(
    time: datetime,
    *,
    show_timestamp: bool = True,
    show_elapsed: bool = True,
) -> str:
    results = []

    if show_timestamp:
        results.append(f"<t:{int(time.timestamp())}>")

    if show_elapsed:
        elapsed_time = humanize.naturaltime(utcnow() - time)
        results.append(f"({elapsed_time})" if results else elapsed_time)

    return " ".join(results)


def get_asset_file(file_name: str) -> File:
    return File(f"taterbot/assets/{file_name}")


def get_channel_display_name(
    channel: GuildChannel,
    user: Member | User | None,
    *,
    allow_mention: bool = True,
    bold_text: bool = True,
) -> str:
    if user and allow_mention:
        mutual_guild_ids = [guild.id for guild in user.mutual_guilds]
        if channel.guild.id in mutual_guild_ids:
            return channel.mention

    sanitized_name = _sanitize_channel_name(emoji.demojize(channel.name))
    display_name = f"#{sanitized_name}" if sanitized_name else f"Channel #{channel.id}"
    return f"**{display_name}**" if bold_text else display_name


def get_channel_loggable_name(channel: GuildChannel) -> str:
    if channel.type == ChannelType.private:
        return "a direct message"
    else:
        return get_channel_display_name(
            channel, user=None, allow_mention=False, bold_text=False
        )


def get_color_value(color: str) -> int:
    color = re.sub(r"\W", "", color.lower(), re.ASCII)

    if color in ["", "default", "embed_background"]:
        return NO_COLOR
    elif hasattr(Color, color):
        return getattr(Color, color).value
    else:
        return min(abs(int(color, 16)), 0xFFFFFF)
