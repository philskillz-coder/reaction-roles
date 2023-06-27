from typing import Type
import os
from imp.database import driver
from dotenv import load_dotenv

load_dotenv()


class MISSING:
    pass


class BaseDriverConfig:
    pass


class SqliteDriverConfig(BaseDriverConfig):
    database: str = "imp/data/data.sqlite"


DB_DRIVER = Type[driver.BaseDriver]
DRIVER_CONFIG = Type[BaseDriverConfig]


class BaseConfig:
    token: str = os.getenv("token")
    database_driver: DB_DRIVER = MISSING
    driver_config: DRIVER_CONFIG = MISSING

    guild_hashids_salt: str = os.getenv("guild_hashids_salt")
    guild_hashids_min_length: int = 6
    guild_hashids_alphabet: str = "ABCDFGHKNOPRSTWXYZ"


class DevelopmentConfig(BaseConfig):
    database_driver = driver.SqliteDriver
    driver_config = SqliteDriverConfig


class ProductionConfig(BaseConfig):
    database_driver = driver.SqliteDriver
    driver_config = SqliteDriverConfig
