# Represents a user's level
class Level:
    def __init__(self, xp):
        self.__XP = xp
    # Human-readable str() function
    def __str__(self):
        return f"Level {self.getLevel()}, {self.getXPProgress()}/{self.getXPLevel()} XP"
    # Get total XP to reach a level
    def __getTotalXP(self, level):
        return (10 * level ** 3 + 135 * level ** 2 + 455 * level) // 6
    # Get raw XP value
    def getXP(self):
        return self.__XP
    # Get level
    def getLevel(self):
        level = 0
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
