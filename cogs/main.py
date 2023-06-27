from __future__ import annotations

from typing import TYPE_CHECKING

from discord import app_commands, Permissions

from imp.better.cog import BetterCog
if TYPE_CHECKING:
    from imp.better.bot import BetterBot
    from imp.better.interaction import BetterInteraction


class Main(BetterCog):
    roles = app_commands.Group(
        name="roles",
        description="Everything you need for managing reaction roles",
        guild_only=True,
        default_permissions=Permissions(
            administrator=True
        )
    )

    @roles.command(
        name="test",
        description="Test command",
    )
    async def test(self, interaction: BetterInteraction):
        await interaction.response.send_message("Test")


async def setup(client: BetterBot):
    await client.add_cog(Main(client))