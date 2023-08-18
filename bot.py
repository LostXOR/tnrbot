import nextcord, config, db
from nextcord import SlashOption, Member, Interaction
from datetime import datetime
from nextcord.ext import commands

# Calculate total XP to reach a level using a very ugly expression
def calcTotalXP(level):
    return int((10 * level ** 3 + 135 * level ** 2 + 455 * level) / 6)

# Calculate XP needed for a level
def calcXP(level):
    return 5 * level ** 2 + 50 * level + 100

# Calculate XP progress of the current level, total XP for the current level, and the level
def calcLevel(xp):
    level = 0
    while xp >= calcTotalXP(level + 1):
        level += 1
    return xp - calcTotalXP(level), calcXP(level), level

# Function to create an embed with parameters
def createEmbed(name, icon, title, description, author, color):
    embed = nextcord.Embed(title = title, description = description, color = color, timestamp = datetime.now())
    embed.set_author(name = name, icon_url = icon)
    embed.set_footer(text = "Requested by " + author.name, icon_url = author.display_avatar.url)
    return embed

db = db.Database(config.databasePath)
bot = commands.Bot(intents = nextcord.Intents.all())

@bot.event
async def on_ready():
    print("Bot started")

@bot.event
async def on_message(msg):
    if msg.author.bot: return
    # Get user data from database and update cached name
    user = db.getUser(msg.guild, msg.author)
    user.cachedName = msg.author.name
    # Add XP to user if they haven't sent a message in xpTimeout seconds
    if user.lastXPTime + config.xpTimeout < msg.created_at.timestamp():
        user.lastXPTime = msg.created_at.timestamp()
        user.XP += config.xpPerMessage
    # Save user data to database
    db.saveUser(user)

@bot.slash_command(description = "Get a user's level")
async def level(
    interaction: Interaction,
    member: Member = SlashOption(name = "user", required = False)):
    # Fetch user data
    member = member if member else interaction.user
    user = db.getUser(interaction.guild, member)
    # Calculate level, XP, etc
    xpProgress, xpLevel, level = calcLevel(user.XP)
    # Embed and send
    embed = createEmbed(
        member.name, member.display_avatar.url,
        f"Level {level}, {xpProgress}/{xpLevel} XP", "",
        interaction.user, 0x00FF00)
    await interaction.send(embeds = [embed])

@bot.slash_command(description = "Set a user's level and XP")
async def set_level(
    interaction: Interaction,
    member: Member = SlashOption(name = "user"),
    level: int = SlashOption(name = "level"),
    xp: int = SlashOption(name = "xp")):
    # Exit if the command executor doesn't have admin permissions
    if not interaction.channel.permissions_for(interaction.user).administrator:
        embed = createEmbed("", None, "Only admins can use this command.", "", interaction.user, 0xFF0000)
        await interaction.send(embeds = [embed])
        return
    # Clamp level and XP inputs
    level = max(min(level, 1000), 0)
    xp = max(min(xp, calcXP(level) - 1), 0)
    # Set new user XP
    user = db.getUser(interaction.guild, member)
    user.cachedName = member.name
    user.XP = calcTotalXP(level) + xp
    db.saveUser(user)
    # Success message
    embed = createEmbed(
        member.name, member.display_avatar.url,
        f"Set to level {level}, {xp}/{calcXP(level)} XP", "",
        interaction.user, 0x00FF00)
    await interaction.send(embeds = [embed])

@bot.slash_command(description = "Get the leaderboard for a guild")
async def leaderboard(
    interaction: Interaction,
    page: int = SlashOption(name = "page", required = False)):
    # Calculate maximum pages and clamp page number
    if page is None:
        page = 1
    page -= 1
    userCount = db.getUserCount(interaction.guild)
    maxPages = (userCount - 1) // config.pageSize
    page = max(min(page, maxPages), 0)
    # Get leaderboard page
    leaderboard = db.getLeaderboard(interaction.guild, page * config.pageSize, (page + 1) * config.pageSize)
    # Generate leaderboard text
    leaderboardText = ""
    for i in range(len(leaderboard)):
        xpProgress, xpLevel, level = calcLevel(leaderboard[i].XP)
        leaderboardText += f"{1 + i + page * config.pageSize}. {leaderboard[i].cachedName}, Level {level}, {xpProgress}/{xpLevel} XP\n"
    # Send embed
    embed = createEmbed(
        interaction.guild.name,
        interaction.guild.icon.url if interaction.guild.icon else None,
        f"Leaderboard, page {page + 1}/{maxPages + 1}",
        leaderboardText, interaction.user, 0x00FF00)
    await interaction.send(embeds = [embed])
bot.run(config.botToken)