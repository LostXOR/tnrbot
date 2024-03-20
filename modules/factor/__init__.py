"""A command to factor numbers using a very fast quadratic sieve implementation (that I stole)."""

import os
import asyncio
import nextcord
from nextcord.ext import commands
import embeds

class Factor(commands.Cog):
    """The Cog where everything happens."""

    @nextcord.slash_command(description = "Factor a number")
    async def factor(self, intr: nextcord.Interaction, number: str): # pylint: disable=R0201
        """The command that handles the factoring."""
        # Just for LesPaulII :)
        if number == "💩":
            await intr.send(embeds = [
                embeds.create_embed(
                    intr.guild, f"Factorization of {number}", "🧑 * 🍔", intr.user, 0x00FF00)
            ])
            return
        # Protect against any sort of command injection (and invalid numbers in general)
        try:
            number_safe = int(number)
        except ValueError:
            await intr.send(embeds = [
                embeds.create_embed(None, "Invalid number.", "", intr.user, 0xFF0000)
            ])
            return
        # Protect against numbers that are unreasonably large
        if number_safe > 10 ** 224:
            await intr.send(embeds = [
                embeds.create_embed(
                    None, "Number must be less than 10^224.", "", intr.user, 0xFF0000)
            ])
            return

        # Run qs on the number in the background
        command = f"bash -c 'time {os.path.dirname(__file__)}/qs limit=99999 -s {number_safe}'"
        process = await asyncio.create_subprocess_shell(command, stdout = asyncio.subprocess.PIPE,
            stderr = asyncio.subprocess.PIPE, env = {"TIMEFORMAT": "%3R"})
        # Start handler for long running factorings
        task = asyncio.create_task(handle_long(intr, process))
        result, time = await process.communicate()
        # Cancel handler
        task.cancel()
        # Process threw an error instead of a 5-6 digit timestamp
        if len(time) > 6 or len(time) < 5:
            print(time)
            await intr.send(embeds = [
                embeds.create_embed(None, "Error during factorization.", "", intr.user, 0xFF0000)
            ])
        # Process timed out and was killed
        elif len(result) == 0:
            await intr.send(embeds = [
                embeds.create_embed(None, "Timeout during factorization.", "", intr.user, 0xFF0000)
            ])
        # Success
        else:
            await intr.send(embeds = [
                embeds.create_embed(intr.guild,
                    f"Factorization of {number_safe}", result.decode() + \
                    "\nExecution time: " + time.decode()[:-1] + "s", intr.user, 0x00FF00)
            ])

async def handle_long(intr, process):
    """Handle long-running factorings by deferring after 1 second and killing after 60 seconds."""
    await asyncio.sleep(1)
    await intr.response.defer()
    await asyncio.sleep(60)
    await process._transport.close() # pylint: disable=W0212
