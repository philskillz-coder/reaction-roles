import json
import os
from typing import List, Dict, TYPE_CHECKING

import aiofiles

from imp.better.logger import BetterLogger
from imp.data.colors import Colors

if TYPE_CHECKING:
    from imp.better.bot import BetterBot
    from imp.database.driver import BaseSession


class AdvancedFormat(dict):
    def __missing__(self, key):
        return "{" + key + "}"


class Translator(BetterLogger):
    DEFAULT_LOCALE = "de-de"

    # noinspection PyTypeChecker
    def __init__(self, client: "BetterBot"):
        self.client = client
        self.available_locales: List[str] = None
        self.data: Dict[str, Dict[str, str]] = None
        self.default_locale: Dict[str, str] = None

    @classmethod
    async def load(cls, client: "BetterBot", locales_path: str):
        instance = cls(client)

        async with aiofiles.open(os.path.join(locales_path, "locales.json"), "rb") as f:
            _available_locales = (await f.read()).decode()
            available_locales: List[str] = json.loads(_available_locales)
            instance.log("load", f"{len(available_locales)} in locales.json")

        async with aiofiles.open(os.path.join(locales_path, "main.json"), "rb") as f:
            _main = (await f.read()).decode()
            main: List[str] = json.loads(_main)
            instance.log("load", f"{len(main)} translations in main.json")

        data: Dict[str, Dict[str, str]] = {}
        for locale in available_locales:
            async with aiofiles.open(os.path.join(locales_path, locale + ".json"), "rb") as f:
                _locale_data = (await f.read()).decode()
                locale_data: dict[str, str] = json.loads(_locale_data)

                if not all(key in locale_data for key in main):
                    instance.log("load", f"Missing translations in {locale}", Colors.YELLOW)

                else:
                    data[locale] = locale_data
                    instance.log("load", f"Locale {locale} loaded successfully")

        instance.log("load", f"{len(data)} locales available")
        instance.available_locales = list(data.keys())
        instance.data = data
        instance.default_locale = data.get(instance.DEFAULT_LOCALE)

        return instance

    async def translate(
            self,
            session: "BaseSession",
            /,
            guild_rid: int,
            key: str,
            **format_args
    ):
        guild_language = await session.guild_language(guild_rid)

        locale = self.data.get(guild_language, self.default_locale)
        _translation = locale.get(key, f"<TRANSLATION:{key}>")

        translation = _translation.format_map(AdvancedFormat(**format_args))

        return translation
