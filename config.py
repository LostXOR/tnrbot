"""General configuration for the bot."""

BOT_TOKEN = ""
DATABASE_PATH = "db.sqlite3"
XP_PER_MESSAGE = 20
XP_TIMEOUT = 60
PAGE_SIZE = 10
ANNOUNCE_LEVEL_UP = True
RATE_LIMIT_THRESHOLD = 200
RATE_LIMIT_COSTS = {
    "biasedrandom": 20,
    "factor": 30,
    "leaderboard": 20,
    "level": 10,
    "set_level": 0,
    "magicball": 90,
    "fortune": 60
}
