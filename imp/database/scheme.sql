CREATE TABLE guilds (
    "id" SERIAL PRIMARY KEY NOT NULL UNIQUE,
    "guild_id" BIGINT NOT NULL UNIQUE
);

CREATE TABLE guild_settings (
    "guild" BIGINT PRIMARY KEY NOT NULL UNIQUE,
    "display_language" VARCHAR(5) NOT NULL DEFAULT 'de-de',
     
    CONSTRAINT fk_guild FOREIGN KEY("guild") REFERENCES guilds("id") ON DELETE CASCADE
);