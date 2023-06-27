from typing import Optional, Literal

import discord
from discord.ext import commands

from imp.better import BetterBot
from imp.data import config
import asyncio
from argparse import ArgumentParser

discord.utils.setup_logging()

parser = ArgumentParser()
parser.add_argument(
    "-c", "--configuration",
    type=str,
    required=False,
    metavar="configuration"
)

sys_args = parser.parse_args()


class Bot(BetterBot):
    INIT_COGS = [
        "cogs.main",
        "cogs.listeners",
        "cogs.errors"
    ]

    async def load_cogs(self):
        for cog in self.INIT_COGS:
            await self.load_extension(cog)

    async def on_ready(self):
        self.log("on_ready", f"Running as {self.user} with {sys_args.configuration} configuration")
        self.log("on_ready", "Online")

        for guild in self.guilds:
            self.log("on_ready", f"Guild: {guild.name}:{guild.id}")

    def prepare_config(self):
        print(sys_args.configuration)
        if sys_args.configuration in ["dev", "development"]:
            self.config = config.DevelopmentConfig
        elif sys_args.configuration in ["prod", "production"]:
            self.config = config.ProductionConfig
        else:
            raise ValueError("Invalid configuration")

    async def setup_hook(self) -> None:
        await self.init_hash_ids()
        await self.init_translator()
        await self.init_hash_ids()

        await self.load_cogs()


async def main():
    async with Bot(commands.when_mentioned, intents=discord.Intents.default(), log_handler=None) as bot:
        bot.prepare_config()

        @bot.command()
        @commands.guild_only()
        @commands.is_owner()
        async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object],
                       spec: Optional[Literal["~", "*", "^"]] = None) -> None:
            if not guilds:
                if spec == "~":
                    synced = await ctx.bot.tree.sync(guild=ctx.guild)
                elif spec == "*":
                    ctx.bot.tree.copy_global_to(guild=ctx.guild)
                    synced = await ctx.bot.tree.sync(guild=ctx.guild)
                elif spec == "^":
                    ctx.bot.tree.clear_commands(guild=ctx.guild)
                    await ctx.bot.tree.sync(guild=ctx.guild)
                    synced = []
                else:
                    synced = await ctx.bot.tree.sync()

                await ctx.send(
                    f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
                )
                return

            ret = 0
            for guild in guilds:
                try:
                    await ctx.bot.tree.sync(guild=guild)
                except discord.HTTPException:
                    pass
                else:
                    ret += 1

            await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

        await bot.start(token=bot.config.token, reconnect=True)


asyncio.run(main())
