"""A logger that logs slash command use, for moderation purposes and such."""

import time
import nextcord
from nextcord.ext import commands
import config

class Logger(commands.Cog):
    """The class where all the magic happens."""

    def __init__(self):
        self.log_file = open(config.LOG_PATH, "a")

    # Need to define the event in the bot context so it's executed first
    @commands.Cog.listener("on_interaction")
    async def on_interaction(self, intr):
        self.log_file.write(
            f"time: {time.time():.3f}\t" +
            f"user id: {intr.user.id}\t" +
            f"guild id: {intr.guild.id if intr.guild is not None else 'none'}\t" +
            f"interaction data: {intr.data}\n"
        )
