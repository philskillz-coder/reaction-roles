from discord.ext.commands import Bot
from hashids import Hashids

from imp.better.logger import BetterLogger
from imp.translation.translator import Translator
from imp.data import config
from imp.database import driver

from typing import Type, TYPE_CHECKING


BOT_CONFIG = Type[config.BaseConfig]
DB_DRIVER = Type[driver.BaseDriver]


class BetterBot(Bot, BetterLogger):
    config: BOT_CONFIG
    db_driver: DB_DRIVER
    translator: Translator

    guild_hashids: Hashids

    async def init_hash_ids(self):
        self.guild_hashids = Hashids(
            salt=self.config.guild_hashids_salt,
            alphabet=self.config.guild_hashids_alphabet,
            min_length=self.config.guild_hashids_min_length
        )

    async def init_translator(self):
        self.translator = await Translator.load(self, "imp/translation/data")
