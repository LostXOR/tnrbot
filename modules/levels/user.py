import modules.levels.level as level

# Represents a user from the database
class User:
    def __init__(self, guild_id, user_id, xp, last_xp_time, cached_name):
        self.__guild_id = guild_id
        self.__id = user_id
        self.__last_xp_time = last_xp_time
        self.__cached_name = cached_name
        self.level = level.Level(xp)
    # Accessor and modifier functions
    def get_guild_id(self): return self.__guild_id
    def get_id(self): return self.__id
    def get_last_xp_time(self): return self.__last_xp_time
    def get_cached_name(self): return self.__cached_name
    def set_last_xp_time(self, time): self.__last_xp_time = time
    def set_cached_name(self, cached_name): self.__cached_name = cached_name