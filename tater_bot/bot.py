from typing import Any, Final

from discord import Bot, Intents


# noinspection PyAbstractClass
class TaterBot(Bot):
    def __init__(self, force_sync: bool, **options: Any) -> None:
        super().__init__(intents=self._intents, **options)
        self._force_sync: Final[bool] = force_sync
        self._initialized: bool = False

    @property
    def _intents(self) -> Intents:
        intents = Intents()
        # noinspection PyDunderSlots,PyUnresolvedReferences
        intents.message_content = True
        return intents

    async def on_ready(self) -> None:
        if not self._initialized:
            if self._force_sync:
                print("Force-syncing commands. Be mindful of the rate limit.")
                await self.sync_commands(force=True)
            self._initialized = True
        print(f"TaterBot is online and ready!")
