
# TNRBot
This is the Discord bot for the TotallyNotRobots Discord server.
## Installation
Install dependencies.
```
pip3 install nextcord
pip3 install requests
pip3 install torch
pip3 install sentencepiece
```
Clone the repository.
```
git clone https://github.com/LostXOR/levelbot
cd levelbot
```
Clone and build the quadratic sieve program from [here](https://github.com/michel-leonard/C-Quadratic-Sieve) and place the `qs` executable in the `levelbot/modules/factor/` directory.

Add your bot's token to `config.py` and tweak any other configuration settings.
```
botToken = "<YOUR TOKEN HERE>"
databasePath = "db.sqlite3"
xpPerMessage = 20
xpTimeout = 60
pageSize = 10
announceLevelUp = True
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
