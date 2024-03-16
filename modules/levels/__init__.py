import nextcord
import nextcord.ext.commands as commands
import modules.levels.db as db
import embed
import config

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = db.Database(config.database_path)

    @nextcord.slash_command(description = "Get a user's level")
    async def level(self, intr: nextcord.Interaction, member: nextcord.Member = nextcord.SlashOption(name = "user", required = False)):
        # Fetch user data
        member = member if member else intr.user
        user = self.db.get_user(intr.guild, member)
        # Embed and send
        await intr.send(embeds = [
            embed.create_embed(member, str(user.level), "", intr.user, 0x00FF00)
        ])

    @nextcord.slash_command(description = "Set a user's level and XP")
    async def set_level(self, intr: nextcord.Interaction, member: nextcord.Member = nextcord.SlashOption(name = "user"), level: int = nextcord.SlashOption(name = "level"), xp: int = nextcord.SlashOption(name = "xp")):
        # Exit if the command executor doesn't have admin permissions
        if not intr.channel.permissions_for(intr.user).administrator:
            await intr.send(embeds = [
                embed.create_embed(None, "Only admins can use this command.", "", intr.user, 0xFF0000)
            ])
            return
        # Set new user XP
        user = self.db.get_user(intr.guild, member)
        user.set_cached_name(member.name)
        user.level.set_level(level, xp)
        self.db.save_user(user)
        # Success message
        await intr.send(embeds = [
            embed.create_embed(member, f"Set to {user.level}", "", intr.user, 0x00FF00)
        ])

    @nextcord.slash_command(description = "Get the leaderboard for a guild")
    async def leaderboard(self, intr: nextcord.Interaction, page: int = nextcord.SlashOption(name = "page", required = False)):
        # Calculate maximum pages and clamp page number
        if page is None:
            page = 1
        page -= 1
        user_count = self.db.get_user_count(intr.guild)
        max_pages = (user_count - 1) // config.page_size
        page = min(max(page, 0), max_pages)
        # Get leaderboard page
        leaderboard = self.db.get_leaderboard(intr.guild, page * config.page_size, config.page_size)
        # Generate leaderboard text
        leaderboard_text = ""
        for i in range(len(leaderboard)):
            user = leaderboard[i]
            leaderboard_text += f"{1 + i + page * config.page_size}. {user.get_cached_name()}, {user.level}\n"
        # Send embed
        await intr.send(embeds = [
            embed.create_embed(intr.guild, f"Leaderboard, page {page + 1}/{max_pages + 1}", leaderboard_text, intr.user, 0x00FF00)
        ])

    @commands.Cog.listener("on_message")
    async def on_message(self, msg):
        if msg.author.bot: return
        # Get user data from database and update cached name
        user = self.db.get_user(msg.guild, msg.author)
        user.set_cached_name(msg.author.name)
        # Add XP to user if they haven't sent a message in xpTimeout seconds
        if user.get_last_xp_time() + config.xp_timeout < msg.created_at.timestamp():
            user.set_last_xp_time(msg.created_at.timestamp())
            user.level.add_xp(config.xp_per_message)
            # Send a level up message if user's XP is less than the XP per message (user just leveled up)
            if config.announce_level_up and user.level.get_xp_progress() < config.xp_per_message:
                await msg.channel.send(embeds = [
                    embed.create_embed(msg.author, f"Leveled up to level {user.level.get_level()}!", "", None, 0x00FF00)
                ])
        # Save user data to database
        self.db.save_user(user)