import modules.levels.level as level

# Represents a user from the database
class User:
    def __init__(self, guildID, userID, XP, lastXPTime, cachedName):
        self.__guildID = guildID
        self.__ID = userID
        self.__lastXPTime = lastXPTime
        self.__cachedName = cachedName
        self.level = level.Level(XP)
    # Accessor and modifier functions
    def getGuildID(self): return self.__guildID
    def getID(self): return self.__ID
    def getLastXPTime(self): return self.__lastXPTime
    def getCachedName(self): return self.__cachedName
    def setLastXPTime(self, time): self.__lastXPTime = time
    def setCachedName(self, cachedName): self.__cachedName = cachedName