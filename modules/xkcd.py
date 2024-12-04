"""A set of commands to fetch xkcd comics."""

import random
import asyncio
import requests
import nextcord
from nextcord.ext import commands
import embeds

class XKCD(commands.Cog):
    """The class where all the magic happens."""

    @nextcord.slash_command()
    async def xkcd(self, intr: nextcord.Interaction):
        """Main "dummy" command that subcommands are attached to."""

    @xkcd.subcommand(description = "Fetch an xkcd")
    async def fetch(self, intr: nextcord.Interaction, number: int):
        """Fetch a specific xkcd."""
        await fetchxkcd(number, intr)

    @xkcd.subcommand(description = "Fetch the latest xkcd")
    async def latest(self, intr: nextcord.Interaction):
        """Fetch the latest xkcd."""
        await fetchxkcd("latest", intr)

    @xkcd.subcommand(description = "Fetch a random xkcd")
    async def rand(self, intr: nextcord.Interaction):
        """Fetch a random xkcd."""
        await fetchxkcd("random", intr)

async def fetchxkcd(num, intr):
    """The function that does the actual fetching."""
    # Get latest xkcd data
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None, requests.get, "https://xkcd.com/info.0.json")
    latest = response.json()
    # Pick random xkcd from 1 to latest
    if num == "random":
        random_num = random.randint(1, latest["num"])
        response = await loop.run_in_executor(
            None, requests.get, f"https://xkcd.com/{random_num}/info.0.json")
        data = response.json()
    # Keep latest xkcd data
    elif num == "latest":
        data = latest
    # Invalid xkcd number
    elif num < 1 or num > latest["num"]:
        await intr.send(embeds = [
            embeds.create_embed(
                None, f"xkcd number must be between 1 and {latest['num']}.",
                "", intr.user, 0xFF0000)
        ])
        return
    # Get specified xkcd number
    else:
        response = await loop.run_in_executor(
            None, requests.get, f"https://xkcd.com/{num}/info.0.json")
        data = response.json()

    # Create and send embed with xkcd
    embed = embeds.create_embed(
        intr.guild, f"xkcd {data['num']}: {data['title']}", data["alt"], intr.user, 0x00FF00)
    embed.set_image(data["img"])
    embed.url = f"https://xkcd.com/{data['num']}"
    await intr.send(embeds = [embed])
