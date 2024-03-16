import os
import asyncio
import nextcord
import nextcord.ext.commands as commands
import embed

# Factor a number
class Factor(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        @bot.slash_command(description = "Factor a number")
        async def factor(intr: nextcord.Interaction, number: str):
            # Factor a number using a quadratic sieve
            # Just for LesPaulII :)
            if number == "💩":
                await intr.send(embeds = [
                    embed.createEmbed(intr.guild, f"Factorization of {number}", "🧑 * 🍔", intr.user, 0x00FF00)
                ])
                return
            # Protect against any sort of command injection (and invalid numbers in general)
            try:
                numberSafe = int(number)
            except:
                await intr.send(embeds = [
                    embed.createEmbed(None, "Invalid number.", "", intr.user, 0xFF0000)
                ])
                return
            # Protect against numbers that are unreasonably large
            if numberSafe > 10 ** 224:
                await intr.send(embeds = [
                    embed.createEmbed(None, "Number must be less than 10^224.", "", intr.user, 0xFF0000)
                ])
                return

            # Run qs on the number in the background
            command = os.path.dirname(__file__) + "/qs --limit=99999 -s " + str(numberSafe)
            process = await asyncio.create_subprocess_shell(command, stdout = asyncio.subprocess.PIPE, stderr = asyncio.subprocess.PIPE)
            # Start handler for long running factorings
            task = asyncio.create_task(self.handleLong(intr, process))
            result, err = await process.communicate()
            # Cancel handler
            task.cancel()

            # Process threw an error
            if err:
                print(err)
                await intr.send(embeds = [
                    embed.createEmbed(None, "Error during factorization.", "", intr.user, 0xFF0000)
                ])
            # Process timed out and was killed
            elif result == b"":
                await intr.send(embeds = [
                    embed.createEmbed(None, "Timeout during factorization.", "", intr.user, 0xFF0000)
                ])
            # Success
            else:
                await intr.send(embeds = [
                    embed.createEmbed(intr.guild, f"Factorization of {numberSafe}", result.decode(), intr.user, 0x00FF00)
                ])

    # Handle long-running factorings by deferring response after 2 seconds and killing after 60 seconds
    async def handleLong(self, intr, process):
        await asyncio.sleep(2)
        await intr.response.defer()
        await asyncio.sleep(60)
        await process._transport.close()