import sqlite3, user

class Database:
    def __init__(self, databasePath):
        self.__db = sqlite3.connect(databasePath, isolation_level = None)
        self.__cursor = self.__db.cursor()
    # Get a user from the database
    def getUser(self, guild, member):
        self.__cursor.execute(f"CREATE TABLE IF NOT EXISTS '{guild.id}' (id, xp, lastxptime, cachedname, UNIQUE(id))")
        data = self.__cursor.execute(f"SELECT * FROM '{guild.id}' WHERE id = ?", [member.id]).fetchone()
        return user.User(guild.id, *data) if data else user.User(guild.id, member.id, 0, 0, None)
    # Save a user to the database
    def saveUser(self, member):
        guildID = member.getGuildID()
        data = [member.getID(), member.level.getXP(), member.getLastXPTime(), member.getCachedName()]
        self.__cursor.execute(f"CREATE TABLE IF NOT EXISTS '{guildID}' (id, xp, lastxptime, cachedname, UNIQUE(id))")
        self.__cursor.execute(f"INSERT OR REPLACE INTO '{guildID}' VALUES (?, ?, ?, ?)", data)
    # Get tracked users in a guild
    def getUserCount(self, guild):
        return self.__cursor.execute(f"SELECT COUNT(id) FROM '{guild.id}'").fetchone()[0]
    # Get a portion of the leaderboard of a guild
    def getLeaderboard(self, guild, start, count):
        leaderboard = self.__cursor.execute(f"SELECT * FROM '{guild.id}' WHERE id NOT IN (SELECT id FROM '{guild.id}' ORDER BY xp DESC LIMIT ?) ORDER BY xp DESC LIMIT ?", [start, count]).fetchall()
        return [user.User(guild.id, *member) for member in leaderboard]