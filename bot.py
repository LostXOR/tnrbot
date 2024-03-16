import nextcord
import nextcord.ext.commands as commands
import config

# Initialize bot
bot = commands.Bot(intents = nextcord.Intents.all())

@bot.event
async def on_ready():
    print("Bot started")

# Load modules
# TNR role buttons
import modules.role_buttons
bot.add_cog(modules.role_buttons.RoleButtons(bot))
# Factoring command
import modules.factor
bot.add_cog(modules.factor.Factor(bot))
# xkcd commands
import modules.xkcd
bot.add_cog(modules.xkcd.XKCD(bot))
# Level commands
import modules.levels
bot.add_cog(modules.levels.Levels(bot))
# Easter eggs ;)
import modules.easter_eggs
bot.add_cog(modules.easter_eggs.EasterEggs(bot))

# Start up bot
bot.run(config.botToken)