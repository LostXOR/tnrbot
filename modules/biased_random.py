"""A biased random number generator."""

import pathlib
import os
import random
import nextcord
from nextcord.ext import commands
import embeds

class BiasedRandom(commands.Cog):
    """The class where all the magic happens."""

    @nextcord.slash_command(description = "Generate a mildly biased random number.")
    async def biasedrandom(self, intr: nextcord.Interaction, size: int): # pylint: disable=R0201
        """Generates a random number."""
        dir = os.path.dirname(os.path.dirname(__file__))
        paths = [str(p) for p in pathlib.Path(dir).rglob("*.py") if "config.py" not in str(p)]
        length = max(0, min(256, int(0.5 + size * (0.5 + random.random()))))

        with open(random.choice(paths), "r") as f:
            end = f.seek(0, 2)
            f.seek(random.randint(0, end - length))
            contents = f.read(length)
        number = int.from_bytes(bytes(contents, encoding = "utf-8"), byteorder = "big")

        embed = embeds.create_embed(intr.guild, str(number)[:256], "", intr.user, 0x00FF00)
        await intr.send(embeds = [embed])
