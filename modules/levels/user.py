"""Represents a user."""

from modules.levels import level

# Represents a user from the database
class User:
    """The class itself."""

    def __init__(self, guild_id, user_id, exp, last_xp_time, cached_name): # pylint: disable=R0913,R0917
        """Set all the internal attributes and things."""
        self.__guild_id = guild_id
        self.__id = user_id
        self.__last_xp_time = last_xp_time
        self.__cached_name = cached_name
        self.level = level.Level(exp)

    # Accessor and modifier functions (not putting docstrings in all of these)
    def get_guild_id(self): # pylint: disable=C0116
        return self.__guild_id
    def get_id(self): # pylint: disable=C0116
        return self.__id
    def get_last_xp_time(self): # pylint: disable=C0116
        return self.__last_xp_time
    def get_cached_name(self): # pylint: disable=C0116
        return self.__cached_name
    def set_last_xp_time(self, time): # pylint: disable=C0116
        self.__last_xp_time = time
    def set_cached_name(self, cached_name): # pylint: disable=C0116
        self.__cached_name = cached_name
