from typing import TypeVar, Optional, Tuple, List, TYPE_CHECKING, Iterable
import aiosqlite

if TYPE_CHECKING:
    from imp.data.config import BaseDriverConfig, SqliteDriverConfig

T = TypeVar("T")

DB_BOOL = Optional[Tuple[bool, ]]
DB_STR = Optional[Tuple[str, ]]
DB_INT = Optional[Tuple[int, ]]
DB_FLOAT = Optional[Tuple[float, ]]
DB_LIST = Optional[List[T]]

DB_GENERIC = Optional[Tuple[T, ]]
RT_GENERIC = Optional[T]


def save_unpack(values: Optional[Iterable[T]]) -> Tuple[Optional[T], List[T]]:
    if not values:
        return None, []

    x, *y = values
    return x, y


class BaseSession:
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()

    async def guild_id_exists(self, /, guild_id: int) -> RT_GENERIC[bool]:
        raise NotImplementedError()

    async def create_guild(self, /, guild_id: int) -> RT_GENERIC[int]:
        raise NotImplementedError()

    async def get_guild_rid(self, /, guild_id: int) -> RT_GENERIC[int]:
        raise NotImplementedError()

    async def guild_language(self, /, guild_rid: int) -> RT_GENERIC[str]:
        raise NotImplementedError()

    async def set_guild_language(self, /, guild_rid: int, language: str) -> None:
        raise NotImplementedError()


class BaseDriver:
    @classmethod
    async def setup(cls, config: "BaseDriverConfig"):
        return cls()

    async def session(self) -> BaseSession:
        raise NotImplementedError()


class SqliteSession(BaseSession):
    def __init__(self, cursor):
        self.cursor = cursor

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cursor.close()

    async def guild_id_exists(self, /, guild_id: int) -> RT_GENERIC[bool]:
        await self.cursor.execute(
            "SELECT EXISTS(SELECT 1 FROM guilds WHERE \"guild_id\" = $1);",
            guild_id
        )
        values: DB_GENERIC[bool] = await self.cursor.fetchone()
        exists, *_ = save_unpack(values)

        return exists

    async def create_guild(self, /, guild_id: int) -> RT_GENERIC[int]:
        await self.cursor.fetchrow(
            "INSERT INTO guilds(\"guild_id\") VALUES($1) RETURNING \"ROWID\";",
            guild_id
        )
        values: DB_GENERIC[str] = await self.cursor.fetchone()
        _guild_hid, *_ = save_unpack(values)

        await self.cursor.execute("INSERT INTO guild_settings(\"guild\") VALUES($1);", _guild_hid)

        return _guild_hid

    async def get_guild_rid(self, /, guild_id: int) -> RT_GENERIC[int]:
        await self.cursor.fetchrow(
            "SELECT \"id\" FROM guilds WHERE \"guild_id\" = $1;",
            guild_id
        )
        values: DB_GENERIC[int] = await self.cursor.fetchone()
        guild_rid, *_ = save_unpack(values)
        return guild_rid

    async def guild_language(self, /, guild_rid: int) -> RT_GENERIC[str]:
        await self.cursor.fetchrow(
            "SELECT \"display_language\" FROM guild_settings WHERE \"guild\" = $1;",
            guild_rid
        )
        values: DB_GENERIC[str] = await self.cursor.fetchone()
        display_language, *_ = save_unpack(values)

        return display_language

    async def set_guild_language(self, /, guild_rid: int, language: str) -> None:
        await self.cursor.execute(
            "UPDATE guild_settings SET \"display_language\" = $1 WHERE guild = $2;",
            language, guild_rid
        )


class SqliteDriver(BaseDriver):
    def __init__(self, db: aiosqlite.Connection):
        self.db = db

    @classmethod
    async def setup(cls, /, config: "SqliteDriverConfig"):
        db = await aiosqlite.connect(config.database)
        return cls(db)

    async def session(self) -> SqliteSession:
        cursor = await self.db.cursor()
        return SqliteSession(cursor)
