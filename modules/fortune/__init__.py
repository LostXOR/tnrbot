import os
import random
import nextcord
import nextcord.ext.commands as commands
import embed

# Factor a number
class Fortune(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Load fortunes
        fortune_file = open(os.path.dirname(__file__) + "/fortunes.txt", "r")
        self.fortunes = fortune_file.read().split("\n%\n")

    @nextcord.slash_command(description = "Tell your future!")
    async def fortune(self, intr: nextcord.Interaction):
        fortune = random.choice(self.fortunes)
        await intr.send(embeds = [
            embed.create_embed(intr.guild, fortune, "", intr.user, 0x00FF00)
        ])