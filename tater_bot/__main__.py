from importlib.metadata import version

from botstrap import Botstrap, CliColors, Color, Option
from discord import Activity, ActivityType


def main() -> int:
    botstrap = Botstrap(
        name := "tater-bot",
        version=version(name),
        colors=CliColors(primary=Color.pink),
    )
    args = botstrap.parse_args(
        force_sync=Option(flag=True, help="Force-sync all TaterBot app commands."),
    )
    botstrap.run_bot(
        bot_class="tater_bot.bot.TaterBot",
        activity=Activity(type=ActivityType.listening, name="@TaterBot"),
        force_sync=args.force_sync,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
