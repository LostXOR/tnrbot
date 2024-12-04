"""A score-based rate limiter to preserve the sanctity of our holy server."""

import asyncio
import time
import nextcord
from nextcord.ext import commands
import embeds

class RateLimiter(commands.Cog):
    """The class where all the magic happens."""

    def __init__(self, bot):
        self.scores = {}
        self.costs = {
            "biasedrandom": 20,
            "factor": 30,
            "leaderboard": 20,
            "level": 10,
            "set_level": 0,
            "magicball": 90,
            "fortune": 60
        }
        self.last_updated = time.time()

        # Need to define the event in the bot context so it's executed first
        @bot.event
        async def on_interaction(intr):
            # Decrement existing scores and delete negative ones
            for key in list(self.scores.keys()):
                self.scores[key] -= time.time() - self.last_updated
                if self.scores[key] < 0:
                    del self.scores[key]
            self.last_updated = time.time()

            if intr.user.id not in self.scores:
                self.scores[intr.user.id] = 0

            # Run command if score is acceptable
            cost = self.costs[intr.data["name"]]
            if self.scores[intr.user.id] + cost < 200:
                self.scores[intr.user.id] += cost
                await bot.process_application_commands(intr)
            # Rate limit error
            else:
                await intr.send(embeds = [
                    embeds.create_embed(
                        None, "Rate limit exceeded!",
                        f"Calm down there, and wait a bit before trying again.",
                        intr.user, 0xFF0000)], ephemeral = True)
