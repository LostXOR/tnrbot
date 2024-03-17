"""Dispense infinite wisdom upon the users of the server via fortunes."""

import os
import random
import nextcord
from nextcord.ext import commands
import embeds

# Factor a number
class Fortune(commands.Cog):
    """Cog that's loaded."""

    def __init__(self):
        """Load the fortunes."""
        fortune_file = open(os.path.dirname(__file__) + "/fortunes.txt", "r", encoding = "utf-8") # pylint:disable=R1732
        self.fortunes = fortune_file.read().split("\n%\n")

    @nextcord.slash_command(description = "Tell your future!")
    async def fortune(self, intr: nextcord.Interaction):
        """Slash command to pick a random fortune."""
        fortune = random.choice(self.fortunes)
        await intr.send(embeds = [
            embeds.create_embed(intr.guild, fortune, "", intr.user, 0x00FF00)
        ])
