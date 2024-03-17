"""Commands and event handling related to the bot's level system."""

import nextcord
from nextcord.ext import commands
from modules.levels import db
import embeds
import config

class Levels(commands.Cog):
    """Cog that's loaded."""

    def __init__(self):
        """Set up database."""
        self.database = db.Database(config.DATABASE_PATH)

    @nextcord.slash_command(description = "Get a user's level")
    async def level(self, intr: nextcord.Interaction,
        member: nextcord.Member = nextcord.SlashOption(name = "user", required = False)):
        """Slash command to display a user's level."""
        # Fetch user data
        member = member if member else intr.user
        user = self.database.get_user(intr.guild, member)
        # Embed and send
        await intr.send(embeds = [
            embeds.create_embed(member, str(user.level), "", intr.user, 0x00FF00)
        ])

    @nextcord.slash_command(description = "Set a user's level and XP")
    async def set_level(self, intr: nextcord.Interaction,
        member: nextcord.Member = nextcord.SlashOption(name = "user"),
        level: int = nextcord.SlashOption(name = "level"),
        exp: int = nextcord.SlashOption(name = "xp")):
        """Slash command to set a user's level, admins only."""
        # Exit if the command executor doesn't have admin permissions
        if not intr.channel.permissions_for(intr.user).administrator:
            await intr.send(embeds = [
                embeds.create_embed(
                    None, "Only admins can use this command.", "", intr.user, 0xFF0000)
            ])
            return
        # Set new user XP
        user = self.database.get_user(intr.guild, member)
        user.set_cached_name(member.name)
        user.level.set_level(level, exp)
        self.database.save_user(user)
        # Success message
        await intr.send(embeds = [
            embeds.create_embed(member, f"Set to {user.level}", "", intr.user, 0x00FF00)
        ])

    @nextcord.slash_command(description = "Get the leaderboard for a guild")
    async def leaderboard(self, intr: nextcord.Interaction,
        page: int = nextcord.SlashOption(name = "page", required = False)):
        """Display the guild level leaderboard."""
        # Calculate maximum pages and clamp page number
        if page is None:
            page = 1
        page -= 1
        user_count = self.database.get_user_count(intr.guild)
        max_pages = (user_count - 1) // config.PAGE_SIZE
        page = min(max(page, 0), max_pages)
        # Get leaderboard page
        leaderboard = self.database.get_leaderboard(
            intr.guild, page * config.PAGE_SIZE, config.PAGE_SIZE)
        # Generate leaderboard text
        leaderboard_text = ""
        for i in enumerate(leaderboard):
            user = i[1]
            leaderboard_text += str(1 + i[0] + page * config.PAGE_SIZE) + ". " + \
                user.get_cached_name() + ", " + str(user.level) + "\n"
        # Send embed
        await intr.send(embeds = [
            embeds.create_embed(intr.guild, f"Leaderboard, page {page + 1}/{max_pages + 1}",
                leaderboard_text, intr.user, 0x00FF00)
        ])

    @commands.Cog.listener("on_message")
    async def on_message(self, msg):
        """Add XP to users when they send messages."""
        if msg.author.bot:
            return
        # Get user data from database and update cached name
        user = self.database.get_user(msg.guild, msg.author)
        user.set_cached_name(msg.author.name)
        # Add XP to user if they haven't sent a message in xpTimeout seconds
        if user.get_last_xp_time() + config.XP_TIMEOUT < msg.created_at.timestamp():
            user.set_last_xp_time(msg.created_at.timestamp())
            user.level.add_xp(config.XP_PER_MESSAGE)
            # Send a level up message if user just leveled up
            if config.ANNOUNCE_LEVEL_UP and user.level.get_xp_progress() < config.XP_PER_MESSAGE:
                await msg.channel.send(embeds = [
                    embeds.create_embed(msg.author,
                        f"Leveled up to level {user.level.get_level()}!", "", None, 0x00FF00)
                ])
        # Save user data to database
        self.database.save_user(user)
