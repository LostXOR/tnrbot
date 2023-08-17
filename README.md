
# LevelBot
This is a simple Discord bot that keeps track of users' levels. It's not much, but I thought I'd put it on GitHub in case anyone found it useful.
## Installation
Install `nextcord` and clone the repository.
```
pip3 install nextcord
git clone https://github.com/LostXOR/levelbot
cd levelbot
```
Add your bot's token to `config.py` and tweak any other configuration settings.
```
botToken = "<YOUR TOKEN HERE>"
databasePath = "db.sqlite3"
xpPerMessage = 20
xpTimeout = 60
pageSize = 10
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