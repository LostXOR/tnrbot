import sqlite3

class User:
    def __init__(self, guildID, data):
        self.guildID = guildID
        self.ID = data[0]
        self.XP = data[1]
        self.lastXPTime = data[2]
        self.cachedName = data[3]

    def toList(self):
        return self.guildID, [self.ID, self.XP, self.lastXPTime, self.cachedName]

class Database:
    def __init__(self, databasePath):
        self.db = sqlite3.connect(databasePath, isolation_level = None)
        self.cursor = self.db.cursor()

    def getUser(self, guild, user):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS '{guild.id}' (id, xp, lastxptime, cachedname, UNIQUE(id))")
        data = self.cursor.execute(f"SELECT * FROM '{guild.id}' WHERE id = ?", [user.id]).fetchone()
        return User(guild.id, data) if data else User(guild.id, [user.id, 0, 0, None])

    def saveUser(self, user):
        guildID, data = user.toList()
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS '{guildID}' (id, xp, lastxptime, cachedname, UNIQUE(id))")
        self.cursor.execute(f"INSERT OR REPLACE INTO '{guildID}' VALUES (?, ?, ?, ?)", data)

    def getUserCount(self, guild):
        return self.cursor.execute(f"SELECT COUNT(id) FROM '{guild.id}'").fetchone()[0]

    def getLeaderboard(self, guild, start, count):
        data = self.cursor.execute(f"SELECT * FROM '{guild.id}' WHERE id NOT IN (SELECT id FROM '{guild.id}' ORDER BY xp DESC LIMIT ?) ORDER BY xp DESC LIMIT ?", [start, count]).fetchall()
        return [User(guild.id, d) for d in data]