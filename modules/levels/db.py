"""Represents the database of user level data."""

import sqlite3
from modules.levels import user

class Database:
    """The class."""

    def __init__(self, database_path):
        """Connect to the database."""
        self.__db = sqlite3.connect(database_path, isolation_level = None)
        self.__cursor = self.__db.cursor()

    def get_user(self, guild, member):
        """Get a user from the database."""
        self.__cursor.execute(
            f"CREATE TABLE IF NOT EXISTS '{guild.id}' (id, xp, lastxptime, cachedname, UNIQUE(id))")
        data = self.__cursor.execute(f"SELECT * FROM '{guild.id}' WHERE id = ?", [member.id]) \
            .fetchone()
        return user.User(guild.id, *data) if data else user.User(guild.id, member.id, 0, 0, None)

    def save_user(self, member):
        """Save a user to the database."""
        guild_id = member.get_guild_id()
        data = [member.get_id(), member.level.get_xp(),
            member.get_last_xp_time(), member.get_cached_name()]
        self.__cursor.execute(
            f"CREATE TABLE IF NOT EXISTS '{guild_id}' (id, xp, lastxptime, cachedname, UNIQUE(id))")
        self.__cursor.execute(f"INSERT OR REPLACE INTO '{guild_id}' VALUES (?, ?, ?, ?)", data)

    def get_user_count(self, guild):
        """Get tracked users in a guild."""
        return self.__cursor.execute(f"SELECT COUNT(id) FROM '{guild.id}'").fetchone()[0]

    def get_leaderboard(self, guild, start, count):
        """Get a portion of the leaderboard of a guild."""
        leaderboard = self.__cursor.execute(f"SELECT * FROM '{guild.id}' \
            WHERE id NOT IN (SELECT id FROM '{guild.id}' \
            ORDER BY xp DESC LIMIT ?) ORDER BY xp DESC LIMIT ?", [start, count]).fetchall()
        return [user.User(guild.id, *member) for member in leaderboard]
