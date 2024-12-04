
# TNRBot
This is the Discord bot for the TotallyNotRobots Discord server.
## Installation
Install dependencies.
```
pip3 install nextcord
pip3 install requests
pip3 install torch
pip3 install transformers
pip3 install sentencepiece
pip3 install protobuf
```
Clone the repository.
```
git clone https://github.com/LostXOR/tnrbot
cd tnrbot
```
Clone and build the quadratic sieve program from [here](https://github.com/michel-leonard/C-Quadratic-Sieve) and place the `qs` executable in the `tnrbot/modules/factor/` directory.

Add your bot's token to `config.py` and tweak any other configuration settings.
```
botToken = "<YOUR TOKEN HERE>"
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
CONFESSION_CHANNEL = <CONFESSION CHANNEL ID>
```
Run the bot.
```
python3 bot.py
```
## Getting level data from MEE6
To get level data from MEE6, run the `mee6_ripper.py` script.
```
python3 mee6_ripper.py
```
Enter your guild ID when prompted and wait for the bot to finish requesting users. Level data will be saved to the database in the config file.
