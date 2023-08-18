import sqlite3

# Represents a user's level
class Level:
    def __init__(self, xp):
        self.__XP = xp
    # Get total XP to reach a level
    def __getTotalXP(self, level):
        return (10 * level ** 3 + 135 * level ** 2 + 455 * level) // 6
    # Get raw XP value
    def getXP(self):
        return self.__XP
    # Get level
    def getLevel(self):
        level = 1
        while self.__XP >= self.__getTotalXP(level + 1):
            level += 1
        return level
    # Get XP progress to next level
    def getXPProgress(self):
        return self.__XP - self.__getTotalXP(self.getLevel())
    # Get XP required for current level
    def getXPLevel(self):
        return 5 * self.getLevel() ** 2 + 50 * self.getLevel() + 100
    # Add XP
    def addXP(self, XP):
        self.__XP += XP
    # Set level and XP
    def setLevel(self, level, XP):
        level = max(min(level, 1000), 0)
        self.__XP = self.__getTotalXP(level)
        XP = max(min(XP, self.getXPLevel() - 1), 0)
        self.__XP += XP

# Represents a user from the database
class User:
    def __init__(self, guildID, userID, XP, lastXPTime, cachedName):
        self.__guildID = guildID
        self.__ID = userID
        self.__lastXPTime = lastXPTime
        self.__cachedName = cachedName
        self.level = Level(XP)
    # Accessor and modifier functions
    def getGuildID(self): return self.__guildID
    def getID(self): return self.__ID
    def getLastXPTime(self): return self.__lastXPTime
    def getCachedName(self): return self.__cachedName
    def setLastXPTime(self, time): self.__lastXPTime = time
    def setCachedName(self, cachedName): self.__cachedName = cachedName

class Database:
    def __init__(self, databasePath):
        self.__db = sqlite3.connect(databasePath, isolation_level = None)
        self.__cursor = self.__db.cursor()
    # Get a user from the database
    def getUser(self, guild, user):
        self.__cursor.execute(f"CREATE TABLE IF NOT EXISTS '{guild.id}' (id, xp, lastxptime, cachedname, UNIQUE(id))")
        data = self.__cursor.execute(f"SELECT * FROM '{guild.id}' WHERE id = ?", [user.id]).fetchone()
        return User(guild.id, *data) if data else User(guild.id, user.id, 0, 0, None)
    # Save a user to the database
    def saveUser(self, user):
        guildID = user.getGuildID()
        data = [user.getID(), user.level.getXP(), user.getLastXPTime(), user.getCachedName()]
        self.__cursor.execute(f"CREATE TABLE IF NOT EXISTS '{guildID}' (id, xp, lastxptime, cachedname, UNIQUE(id))")
        self.__cursor.execute(f"INSERT OR REPLACE INTO '{guildID}' VALUES (?, ?, ?, ?)", data)
    # Get tracked users in a guild
    def getUserCount(self, guild):
        return self.__cursor.execute(f"SELECT COUNT(id) FROM '{guild.id}'").fetchone()[0]
    # Get a portion of the leaderboard of a guild
    def getLeaderboard(self, guild, start, count):
        leaderboard = self.__cursor.execute(f"SELECT * FROM '{guild.id}' WHERE id NOT IN (SELECT id FROM '{guild.id}' ORDER BY xp DESC LIMIT ?) ORDER BY xp DESC LIMIT ?", [start, count]).fetchall()
        return [User(guild.id, *user) for user in leaderboard]