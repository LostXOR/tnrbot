"""Initializes the bot and loads all the modules."""

import nextcord
from nextcord.ext import commands
import config
import modules

bot = commands.Bot(intents = nextcord.Intents.all())

@bot.event
async def on_ready():
    """Log when the bot's fully started up."""
    print("Bot started")

# Load modules
bot.add_cog(modules.role_buttons.RoleButtons())
bot.add_cog(modules.factor.Factor())
bot.add_cog(modules.xkcd.XKCD())
bot.add_cog(modules.levels.Levels())
bot.add_cog(modules.language_model.LanguageModel())
bot.add_cog(modules.easter_eggs.EasterEggs(bot))

bot.run(config.BOT_TOKEN)
