"""Confess your sins to the crowd!"""

import nextcord
from nextcord.ext import commands
import embeds
import config

class Confess(commands.Cog):
    """The class where all the magic happens."""

    @nextcord.slash_command(description = "Confess something, anything. Completely anonymous!", guild_ids = config.GUILDS)
    async def confess(self, intr: nextcord.Interaction, confession: str):
        """Sends a confession to the confession channel."""
        channel = intr.client.get_channel(config.CONFESSION_CHANNELS[intr.guild.id])
        await channel.send(embeds = [
            embeds.create_embed(None, "Confession", confession[:4096], None, 0x00FF00)
        ])

        await intr.send(embeds = [
            embeds.create_embed(None, "Confession sent!", "", intr.user, 0x00FF00)
        ], ephemeral = True)
