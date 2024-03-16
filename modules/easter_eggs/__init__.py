import os
import nextcord
import nextcord.ext.commands as commands

class EasterEggs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message(self, msg):
        # Respond to mistypings of !rank (Added at the request of TinRobit)
        if msg.content == "!raml":
            await msg.channel.send("https://imgur.com/a/fHdLJZU")
        elif msg.content == "!rabk":
            await msg.channel.send("<:roboHolyDivided0:834465408135987220>")
        # Respond to "/halp" with bird chopsticks picture (sent by LesPaulII)
        elif msg.content == "/halp":
            await msg.channel.send(files = [nextcord.File(os.path.dirname(__file__) + "/bird_halp.jpg")])

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        # Set status to "Playing Whack-a-MEE6"
        status = nextcord.Game("Whack-a-MEE6")
        await self.bot.change_presence(activity = status)