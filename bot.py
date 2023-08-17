import nextcord, json, os, time, heapq
from datetime import datetime
from nextcord.ext import commands

# Get data for a guild, initializing if it doesn't exist
def getGuild(guildID):
    guildID = str(guildID)
    if guildID not in db:
        db[guildID] = {"users":{}}
    return db[guildID]

# Get data for a user, initializing if it doesn't exist
def getUser(guildID, userID):
    userID = str(userID)
    guildData = getGuild(guildID)
    if userID not in guildData["users"]:
        guildData["users"][userID] = {"xp": 0, "lastxp": 0}
    return guildData["users"][userID]

# Calculate total XP given a level
def calcTotalXP(level):
    return int((10 * level ** 3 + 135 * level ** 2 + 455 * level) / 6)

# Calculate XP needed for a level
def calcXP(level):
    return 5 * level ** 2 + 50 * level + 100

# Calculate XP progress, XP, and level given total XP
def calcLevel(xp):
    level = 0
    while xp >= calcTotalXP(level + 1):
        level += 1
    return xp - calcTotalXP(level), calcXP(level), level

# Save the database to disk
def saveDB():
    with open("db.json", "w") as file:
        file.write(json.dumps(db))

def createEmbed(name, icon, title, description, author, color):
    embed = nextcord.Embed(title = title, description = description, color = color, timestamp = datetime.now())
    embed.set_author(name = name, icon_url = icon)
    embed.set_footer(text = "Requested by " + author.name, icon_url = author.display_avatar.url)
    return embed

config = json.loads(open("config.json", "r").read())
db = json.loads(open("db.json", "r").read()) if os.path.exists("db.json") else {}
bot = commands.Bot(intents = nextcord.Intents.all())


@bot.event
async def on_ready():
    print("Bot started")


@bot.event
async def on_message(msg):
    if msg.author.bot:
        return

    # Add XP to message sender if they haven't sent a message in xpTimeout seconds
    userData = getUser(msg.guild.id, msg.author.id)
    if userData["lastxp"] + config["xpTimeout"] < msg.created_at.timestamp():
        userData["lastxp"] = msg.created_at.timestamp()
        userData["xp"] += config["xpPerMessage"]
        saveDB()


@bot.slash_command(description = "Get a user's level")
async def level(
    interaction: nextcord.Interaction,
    user: nextcord.Member = nextcord.SlashOption(name = "user", required = False)
):
    if not user:
        user = interaction.user
    xpProgress, xpLevel, level = calcLevel(getUser(interaction.guild.id, user.id)["xp"])
    embed = createEmbed(
        user.name,
        user.display_avatar.url,
        f"Level {level}, {xpProgress}/{xpLevel} XP",
        "",
        interaction.user, 0x00FF00
    )
    await interaction.send(embeds = [embed])


@bot.slash_command(description = "Set a user's level and XP")
async def set_level(
    interaction: nextcord.Interaction,
    user: nextcord.Member = nextcord.SlashOption(name = "user"),
    level: int = nextcord.SlashOption(name = "level"),
    xp: int = nextcord.SlashOption(name = "xp")
):
    if interaction.channel.permissions_for(interaction.user).administrator:
        userData = getUser(interaction.guild.id, user.id)
        level = max(min(level, 1000), 0)
        xp = max(min(xp, calcXP(level) - 1), 0)
        userData["xp"] = calcTotalXP(level) + xp
        embed = createEmbed(
            user.name,
            user.display_avatar.url,
            f"Set to level {level}, {xp}/{calcXP(level)} XP",
            "",
            interaction.user,
            0x00FF00
        )
    else:
        embed = createEmbed(
            "",
            None,
            "Only administrators can use this command!",
            "",
            interaction.user,
            0xFF0000
        )
    await interaction.send(embeds = [embed])
    saveDB()


@bot.slash_command(description = "Get the leaderboard for a guild")
async def leaderboard(
    interaction: nextcord.Interaction,
    page: int = nextcord.SlashOption(name = "page", required = False)
):
    users = getGuild(interaction.guild.id)["users"]
    page = max(min(page, (len(users) - 1) // config["pageSize"] + 1), 1) if page else 1
    leaderboard = heapq.nlargest(page * config["pageSize"], users.items(), key = lambda u: u[1]["xp"])[(page - 1) * config["pageSize"]:]

    leaderboardText = ""
    for i in range(len(leaderboard)):
        xpProgress, xpLevel, level = calcLevel(leaderboard[i][1]["xp"])
        user = await bot.fetch_user(leaderboard[i][0])
        leaderboardText += f"{i + (page - 1) * config['pageSize'] + 1}. {user.name}, Level {level}, {xpProgress}/{xpLevel} XP\n"
    embed = createEmbed(
        interaction.guild.name,
        interaction.guild.icon.url if interaction.guild.icon else None,
        f"Leaderboard, page {page}/{(len(users) - 1) // config['pageSize'] + 1}",
        leaderboardText,
        interaction.user,
        0x00FF00
    )
    await interaction.send(embeds = [embed])

bot.run(config["botToken"])