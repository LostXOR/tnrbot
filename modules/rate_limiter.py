"""A score-based rate limiter to preserve the sanctity of our holy server."""

import asyncio
import time
import nextcord
from nextcord.ext import commands
import embeds
import config

class RateLimiter(commands.Cog):
    """The class where all the magic happens."""

    def __init__(self, bot):
        self.scores = {}
        self.last_updated = time.time()

        # Need to define the event in the bot context so it's executed first
        @bot.event
        async def on_interaction(intr):
            # Not a slash command or an unknown one
            if "name" not in intr.data or intr.data["name"] not in config.RATE_LIMIT_COSTS:
                await bot.process_application_commands(intr)
                return

            # Decrement existing scores and delete negative ones
            for key in list(self.scores.keys()):
                if key == 1156003455438159933: # Spammy guy gets 10x slow penalty
                    self.scores[key] -= (time.time() - self.last_updated) / 10
                else:
                    self.scores[key] -= time.time() - self.last_updated
                if self.scores[key] < 0:
                    del self.scores[key]
            self.last_updated = time.time()

            if intr.user.id not in self.scores:
                self.scores[intr.user.id] = 0

            # Run command if score is acceptable
            cost = config.RATE_LIMIT_COSTS[intr.data["name"]]
            if self.scores[intr.user.id] + cost < config.RATE_LIMIT_THRESHOLD:
                self.scores[intr.user.id] += cost
                await bot.process_application_commands(intr)
            # Rate limit error
            else:
                await intr.send(embeds = [
                    embeds.create_embed(
                        None, "Rate limit exceeded!",
                        f"Calm down there, wait a bit before trying again.",
                        intr.user, 0xFF0000)], ephemeral = True)
