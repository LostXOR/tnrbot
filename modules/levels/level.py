# Represents a user's level
class Level:
    def __init__(self, xp):
        self.__xp = xp
    # Human-readable str() function
    def __str__(self):
        return f"Level {self.get_level()}, {self.get_xp_progress()}/{self.get_xp_level()} XP"
    # Get total XP to reach a level
    def __get_total_xp(self, level):
        return (10 * level ** 3 + 135 * level ** 2 + 455 * level) // 6
    # Get raw XP value
    def get_xp(self):
        return self.__xp
    # Get level
    def get_level(self):
        level = 0
        while self.__xp >= self.__get_total_xp(level + 1):
            level += 1
        return level
    # Get XP progress to next level
    def get_xp_progress(self):
        return self.__xp - self.__get_total_xp(self.get_level())
    # Get XP required for current level
    def get_xp_level(self):
        return 5 * self.get_level() ** 2 + 50 * self.get_level() + 100
    # Add XP
    def add_xp(self, xp):
        self.__xp += xp
    # Set level and XP
    def set_level(self, level, XP):
        level = max(min(level, 1000), 0)
        self.__xp = self.__get_total_xp(level)
        XP = max(min(XP, self.get_xp_level() - 1), 0)
        self.__xp += XP
