"""General configuration for the bot."""

BOT_TOKEN = ""
DATABASE_PATH = "db.sqlite3"
XP_PER_MESSAGE = 20
XP_TIMEOUT = 60
PAGE_SIZE = 10
ANNOUNCE_LEVEL_UP = True
RATE_LIMIT_THRESHOLD = 400
RATE_LIMIT_COSTS = {
    "xkcd": 20,
    "biasedrandom": 20,
    "factor": 30,
    "leaderboard": 20,
    "level": 10,
    "set_level": 0,
    "magicball": 75,
    "fortune": 100,
    "confess": 200
}
GUILDS = [1234]
CONFESSION_CHANNELS = {
    1234: 5678
}
