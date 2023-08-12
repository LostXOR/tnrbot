# LevelBot
This is a simple Discord bot that keeps track of users' levels. It's not much, but I thought I'd put it on GitHub in case anyone found it useful.
## Installation
Install `nextcord` and clone the repository.
```
pip3 install nextcord
git clone https://github.com/LostXOR/levelbot
cd levelbot
```
Add your bot's token to `config.json`.
```
{
  "botToken": "<YOUR TOKEN HERE>",
  "xpPerMessage": 20,
  "xpTimeout": 60
}
```
Run the bot.
```
python3 bot.py
```
