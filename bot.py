import config, db
from nextcord import SlashOption, Member, Interaction, Embed, Intents
from datetime import datetime
from nextcord.ext import commands

# Create an embed with given parameters
def createEmbed(name, icon, title, description, author, color):
    embed = Embed(title = title, description = description, color = color, timestamp = datetime.now())
    embed.set_author(name = name, icon_url = icon.url if icon else None)
    embed.set_footer(text = "Requested by " + author.name, icon_url = author.display_avatar.url)
    return embed

# Initialize database and bot
db = db.Database(config.databasePath)
bot = commands.Bot(intents = Intents.all())

@bot.event
async def on_ready():
    print("Bot started")

@bot.event
async def on_message(msg):
    if msg.author.bot: return
    # Get user data from database and update cached name
    user = db.getUser(msg.guild, msg.author)
    user.setCachedName(msg.author.name)
    # Add XP to user if they haven't sent a message in xpTimeout seconds
    if user.getLastXPTime() + config.xpTimeout < msg.created_at.timestamp():
        user.setLastXPTime(msg.created_at.timestamp())
        user.level.addXP(config.xpPerMessage)
    # Save user data to database
    db.saveUser(user)

@bot.slash_command(description = "Get a user's level")
async def level(intr: Interaction, member: Member = SlashOption(name = "user", required = False)):
    # Fetch user data
    member = member if member else intr.user
    user = db.getUser(intr.guild, member)
    # Embed and send
    embed = createEmbed(
        member.name, member.display_avatar,
        f"Level {user.level.getLevel()}, {user.level.getXPProgress()}/{user.level.getXPLevel()} XP", "",
        intr.user, 0x00FF00)
    await intr.send(embeds = [embed])

@bot.slash_command(description = "Set a user's level and XP")
async def set_level(intr: Interaction, member: Member = SlashOption(name = "user"), level: int = SlashOption(name = "level"), xp: int = SlashOption(name = "xp")):
    # Exit if the command executor doesn't have admin permissions
    if not intr.channel.permissions_for(intr.user).administrator:
        embed = createEmbed("", None, "Only admins can use this command.", "", intr.user, 0xFF0000)
        await intr.send(embeds = [embed])
        return
    # Set new user XP
    user = db.getUser(intr.guild, member)
    user.setCachedName(member.name)
    user.level.setLevel(level, xp)
    db.saveUser(user)
    # Success message
    embed = createEmbed(
        member.name, member.display_avatar,
        f"Set to level {level}, {xp}/{user.level.getXPLevel()} XP", "",
        intr.user, 0x00FF00)
    await intr.send(embeds = [embed])

@bot.slash_command(description = "Get the leaderboard for a guild")
async def leaderboard(intr: Interaction, page: int = SlashOption(name = "page", required = False)):
    # Calculate maximum pages and clamp page number
    if page is None:
        page = 1
    page -= 1
    userCount = db.getUserCount(intr.guild)
    maxPages = (userCount - 1) // config.pageSize
    page = max(min(page, maxPages), 0)
    # Get leaderboard page
    leaderboard = db.getLeaderboard(intr.guild, page * config.pageSize, config.pageSize)
    # Generate leaderboard text
    leaderboardText = ""
    for i in range(len(leaderboard)):
        user = leaderboard[i]
        leaderboardText += f"{1 + i + page * config.pageSize}. {user.getCachedName()}, Level {user.level.getLevel()}, {user.level.getXPProgress()}/{user.level.getXPLevel()} XP\n"
    # Send embed
    embed = createEmbed(
        intr.guild.name, intr.guild.icon,
        f"Leaderboard, page {page + 1}/{maxPages + 1}",
        leaderboardText, intr.user, 0x00FF00)
    await intr.send(embeds = [embed])
bot.run(config.botToken)