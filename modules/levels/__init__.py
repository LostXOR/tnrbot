import nextcord
import nextcord.ext.commands as commands
import modules.levels.db as db
import embed
import config

class Levels(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self.db = db.Database(config.databasePath)

        @bot.slash_command(description = "Get a user's level")
        async def level(intr: nextcord.Interaction, member: nextcord.Member = nextcord.SlashOption(name = "user", required = False)):
            # Fetch user data
            member = member if member else intr.user
            user = self.db.getUser(intr.guild, member)
            # Embed and send
            await intr.send(embeds = [
                embed.createEmbed(member, str(user.level), "", intr.user, 0x00FF00)
            ])

        @bot.slash_command(description = "Set a user's level and XP")
        async def set_level(intr: nextcord.Interaction, member: nextcord.Member = nextcord.SlashOption(name = "user"), level: int = nextcord.SlashOption(name = "level"), xp: int = nextcord.SlashOption(name = "xp")):
            # Exit if the command executor doesn't have admin permissions
            if not intr.channel.permissions_for(intr.user).administrator:
                await intr.send(embeds = [
                    embed.createEmbed(None, "Only admins can use this command.", "", intr.user, 0xFF0000)
                ])
                return
            # Set new user XP
            user = self.db.getUser(intr.guild, member)
            user.setCachedName(member.name)
            user.level.setLevel(level, xp)
            self.db.saveUser(user)
            # Success message
            await intr.send(embeds = [
                embed.createEmbed(member, f"Set to {user.level}", "", intr.user, 0x00FF00)
            ])

        @bot.slash_command(description = "Get the leaderboard for a guild")
        async def leaderboard(intr: nextcord.Interaction, page: int = nextcord.SlashOption(name = "page", required = False)):
            # Calculate maximum pages and clamp page number
            if page is None:
                page = 1
            page -= 1
            userCount = self.db.getUserCount(intr.guild)
            maxPages = (userCount - 1) // config.pageSize
            page = min(max(page, 0), maxPages)
            # Get leaderboard page
            leaderboard = self.db.getLeaderboard(intr.guild, page * config.pageSize, config.pageSize)
            # Generate leaderboard text
            leaderboardText = ""
            for i in range(len(leaderboard)):
                user = leaderboard[i]
                leaderboardText += f"{1 + i + page * config.pageSize}. {user.getCachedName()}, {user.level}\n"
            # Send embed
            await intr.send(embeds = [
                embed.createEmbed(intr.guild, f"Leaderboard, page {page + 1}/{maxPages + 1}", leaderboardText, intr.user, 0x00FF00)
            ])

    @commands.Cog.listener("on_message")
    async def on_message(self, msg):
        if msg.author.bot: return
        # Get user data from database and update cached name
        user = self.db.getUser(msg.guild, msg.author)
        user.setCachedName(msg.author.name)
        # Add XP to user if they haven't sent a message in xpTimeout seconds
        if user.getLastXPTime() + config.xpTimeout < msg.created_at.timestamp():
            user.setLastXPTime(msg.created_at.timestamp())
            user.level.addXP(config.xpPerMessage)
            # Send a level up message if user's XP is less than the XP per message (user just leveled up)
            if config.announceLevelUp and user.level.getXPProgress() < config.xpPerMessage:
                await msg.channel.send(embeds = [
                    embed.createEmbed(msg.author, f"Leveled up to level {user.level.getLevel()}!", "", None, 0x00FF00)
                ])
        # Save user data to database
        self.db.saveUser(user)