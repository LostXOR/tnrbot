import nextcord, sqlite3, time
from datetime import datetime
from nextcord.ext import commands
import config

# Get data for a user, returns tuple (user ID, user XP, last XP timestamp, cached username)
def getUserData(guildID, userID):
    cursor.execute(f"CREATE TABLE IF NOT EXISTS '{guildID}' (id, xp, lastxptime, cachedname, UNIQUE(id))")
    data = cursor.execute(f"SELECT * FROM '{guildID}' WHERE id = ?", [userID]).fetchone()
    return list(data) if data else [userID, 0, 0, ""]

# Save data for a user
def setUserData(guildID, userID, data):
    cursor.execute(f"CREATE TABLE IF NOT EXISTS '{guildID}' (id, xp, lastxptime, cachedname, UNIQUE(id))")
    cursor.execute(f"INSERT OR REPLACE INTO '{guildID}' VALUES (?, ?, ?, ?)", data)

def getUserCount(guildID):
    return cursor.execute(f"SELECT COUNT(id) FROM '{guildID}'").fetchone()[0]

def getLeaderboardPage(guildID, page):
    return cursor.execute(f"SELECT * FROM '{guildID}' WHERE id NOT IN (SELECT id FROM '{guildID}' ORDER BY xp DESC LIMIT ?) ORDER BY xp DESC LIMIT ?", [page * config.pageSize, config.pageSize]).fetchall()

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

# Load sqlite3 database
db = sqlite3.connect(config.databasePath, isolation_level = None)
cursor = db.cursor()
bot = commands.Bot(intents = nextcord.Intents.all())

@bot.event
async def on_ready():
    print("Bot started")

@bot.event
async def on_message(msg):
    if msg.author.bot: return
    # Get user data from database and update cached name
    userData = getUserData(msg.guild.id, msg.author.id)
    userData[3] = msg.author.name
    # Add XP to user if they haven't sent a message in xpTimeout seconds
    if userData[2] + config.xpTimeout < msg.created_at.timestamp():
        userData[2] = msg.created_at.timestamp()
        userData[1] += config.xpPerMessage
    # Save user data to database
    setUserData(msg.guild.id, msg.author.id, userData)

@bot.slash_command(description = "Get a user's level")
async def level(
    interaction: nextcord.Interaction,
    user: nextcord.Member = nextcord.SlashOption(name = "user", required = False)):
    # Fetch user data
    user = user if user else interaction.user
    userData = getUserData(interaction.guild.id, user.id)
    # Calculate level, XP, etc
    xpProgress, xpLevel, level = calcLevel(userData[1])
    # Embed and send
    embed = createEmbed(
        user.name, user.display_avatar.url,
        f"Level {level}, {xpProgress}/{xpLevel} XP", "",
        interaction.user, 0x00FF00)
    await interaction.send(embeds = [embed])

@bot.slash_command(description = "Set a user's level and XP")
async def set_level(
    interaction: nextcord.Interaction,
    user: nextcord.Member = nextcord.SlashOption(name = "user"),
    level: int = nextcord.SlashOption(name = "level"),
    xp: int = nextcord.SlashOption(name = "xp")):
    # Exit if the command executor doesn't have admin permissions
    if not interaction.channel.permissions_for(interaction.user).administrator:
        embed = createEmbed("", None, "Only admins can use this command.", "", interaction.user, 0xFF0000)
        await interaction.send(embeds = [embed])
        return
    # Clamp level and XP inputs
    level = max(min(level, 1000), 0)
    xp = max(min(xp, calcXP(level) - 1), 0)
    # Set new user XP
    userData = getUserData(interaction.guild.id, user.id)
    userData[1] = calcTotalXP(level) + xp
    setUserData(interaction.guild.id, user.id, userData)
    # Success message
    embed = createEmbed(
        user.name, user.display_avatar.url,
        f"Set to level {level}, {xp}/{calcXP(level)} XP", "",
        interaction.user, 0x00FF00)
    await interaction.send(embeds = [embed])

@bot.slash_command(description = "Get the leaderboard for a guild")
async def leaderboard(
    interaction: nextcord.Interaction,
    page: int = nextcord.SlashOption(name = "page", required = False)):
    # Calculate maximum pages and clamp page number
    if page is None:
        page = 1
    page -= 1
    userCount = getUserCount(interaction.guild.id)
    maxPages = (userCount - 1) // config.pageSize
    page = max(min(page, maxPages), 0)
    # Get leaderboard page
    leaderboard = getLeaderboardPage(interaction.guild.id, page)
    # Generate leaderboard text
    leaderboardText = ""
    for i in range(len(leaderboard)):
        xpProgress, xpLevel, level = calcLevel(leaderboard[i][1])
        username = leaderboard[i][3]
        leaderboardText += f"{1 + i + page * config.pageSize}. {username}, Level {level}, {xpProgress}/{xpLevel} XP\n"
    # Send embed
    embed = createEmbed(
        interaction.guild.name,
        interaction.guild.icon.url if interaction.guild.icon else None,
        f"Leaderboard, page {page + 1}/{maxPages + 1}",
        leaderboardText, interaction.user, 0x00FF00)
    await interaction.send(embeds = [embed])
bot.run(config.botToken)