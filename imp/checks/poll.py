from discord import app_commands

from typing import TYPE_CHECKING

from imp.better.check import BetterCheckFailure
if TYPE_CHECKING:
    from imp.better.interaction import BetterInteraction


def test(*args, **kwargs):
    async def check(interaction: "BetterInteraction"):
        return True
    return app_commands.check(check)
