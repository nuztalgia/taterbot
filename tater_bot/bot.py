from pathlib import Path
from typing import Any, Final

from discord import Bot, Intents

from tater_bot.config import Config
from tater_bot.log import Log


# noinspection PyAbstractClass
class TaterBot(Bot):
    def __init__(self, force_sync: bool, **options: Any) -> None:
        intents = Intents.default()
        # noinspection PyDunderSlots,PyUnresolvedReferences
        intents.message_content = True

        super().__init__(intents=intents, owner_id=Config.owner_id, **options)

        self._force_sync: Final[bool] = force_sync
        self._initialized: bool = False

        for file_path in Path(__file__).parent.glob("cogs/[!_]*.py"):
            Log.d(f"Loading extension '{file_path.stem}'.")
            self.load_extension(f"tater_bot.cogs.{file_path.stem}")

    async def on_ready(self) -> None:
        if self._initialized:
            return

        if self._force_sync:
            Log.w("Force-syncing commands. Be mindful of the rate limit.")
            await self.sync_commands(force=True)

        self._initialized = True
        Log.i(f"TaterBot is online and ready!")
