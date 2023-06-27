from abc import ABC

from discord import app_commands
from imp.better.check import BetterCheckFailure
from typing import TYPE_CHECKING, List, Union

if TYPE_CHECKING:
    from imp.better.interaction import BetterInteraction


class Test_Transformer(app_commands.Transformer, ABC):
    @classmethod
    async def transform(cls, interaction: "BetterInteraction", value: str, /) -> str:
        return value

    @classmethod
    async def autocomplete(cls, interaction: "BetterInteraction", value: str) -> List[app_commands.Choice[str]]:
        value = value.lower()
        choices: List[app_commands.Choice] = []
        return choices
