import random
import asyncio
import requests
import nextcord
import nextcord.ext.commands as commands
import embed

class XKCD(commands.Cog):
        def __init__(self, bot):
            self.bot = bot

        # xkcd commands
        @nextcord.slash_command()
        async def xkcd(self, intr: nextcord.Interaction):
            pass

        @xkcd.subcommand(description = "Fetch an xkcd")
        async def fetch(self, intr: nextcord.Interaction, number: int):
            await self.fetchxkcd(number, intr)

        @xkcd.subcommand(description = "Fetch the latest xkcd")
        async def latest(self, intr: nextcord.Interaction):
            await self.fetchxkcd("latest", intr)

        @xkcd.subcommand(description = "Fetch a random xkcd")
        async def rand(self, intr: nextcord.Interaction):
            await self.fetchxkcd("random", intr)

        # Fetch an xkcd
        async def fetchxkcd(self, num, intr):
            # Get latest xkcd data
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, requests.get, "https://xkcd.com/info.0.json")
            latest = response.json()
            # Pick random xkcd from 1 to latest
            if num == "random":
                randomNum = random.randint(1, latest["num"])
                response = await loop.run_in_executor(None, requests.get, f"https://xkcd.com/{randomNum}/info.0.json")
                data = response.json()
            # Keep latest xkcd data
            elif num == "latest":
                data = latest
            # Invalid xkcd number
            elif num < 1 or num > latest["num"]:
                await intr.send(embeds = [
                    embed.createEmbed(None, f"xkcd number must be between 1 and {latest['num']}.", "", intr.user, 0xFF0000)
                ])
                return
            # Get specified xkcd number
            else:
                response = await loop.run_in_executor(None, requests.get, f"https://xkcd.com/{num}/info.0.json")
                data = response.json()

            # Create and send embed with xkcd
            e = embed.createEmbed(intr.guild, f"xkcd {data['num']}: {data['title']}", data["alt"], intr.user, 0x00FF00)
            e.set_image(data["img"])
            e.url = f"https://xkcd.com/{data['num']}"
            await intr.send(embeds = [e])
