"""A class to represent a user's level and provide handy ways to interact with it."""

class Level:
    """The class, omg!"""

    def __init__(self, exp):
        """Standard init function."""
        self.__xp = exp

    def __str__(self):
        """Human-readable str() function."""
        return f"Level {self.get_level()}, {self.get_xp_progress()}/{self.get_xp_level()} XP"

    def get_xp(self):
        """Get raw XP value."""
        return self.__xp

    def get_level(self):
        """Get level."""
        level = 0
        while self.__xp >= get_total_xp(level + 1):
            level += 1
        return level

    def get_xp_progress(self):
        """Get XP progress to next level."""
        return self.__xp - get_total_xp(self.get_level())

    def get_xp_level(self):
        """Get XP required for current level."""
        return 5 * self.get_level() ** 2 + 50 * self.get_level() + 100

    def add_xp(self, exp):
        """Add XP."""
        self.__xp += exp

    def set_level(self, level, exp):
        """Set level and XP."""
        level = max(min(level, 1000), 0)
        self.__xp = get_total_xp(level)
        exp = max(min(exp, self.get_xp_level() - 1), 0)
        self.__xp += exp

def get_total_xp(level):
    """Get total XP to reach a level."""
    return (10 * level ** 3 + 135 * level ** 2 + 455 * level) // 6
