import nextcord, config, db
from datetime import datetime

# Create an embed with given parameters
def createEmbed(object, title, description, author, color):
    embed = nextcord.Embed(title = title, description = description, color = color, timestamp = datetime.now())
    name = object.name if object else None
    if isinstance(object, Member): icon = object.display_avatar.url
    elif isinstance(object, Guild): icon = object.icon.url if object.icon else None
    else: icon = None
    embed.set_author(name = name, icon_url = icon)
    embed.set_footer(text = "Requested by " + author.name, icon_url = author.display_avatar.url)
    return embed

# Initialize database and bot
db = db.Database(config.databasePath)
bot = nextcord.Client(intents = Intents.all())

@bot.event
async def on_ready():
    # Set status to "Playing Whack-a-MEE6"
    status = nextcord.Game("Whack-a-MEE6")
    await bot.change_presence(activity = status)
    print("Bot started")

@bot.event
async def on_message(msg):
    # Respond to mistypings of !rank (Added at the request of TinRobit)
    if msg.content == "!raml":
        await msg.channel.send("https://imgur.com/a/fHdLJZU")
    if msg.content == "!rabk":
        await msg.channel.send("<:roboHolyDivided0:834465408135987220>")

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
async def level(intr: nextcord.Interaction, member: nextcord.Member = nextcord.SlashOption(name = "user", required = False)):
    # Fetch user data
    member = member if member else intr.user
    user = db.getUser(intr.guild, member)
    # Embed and send
    embed = createEmbed(member, str(user.level), "", intr.user, 0x00FF00)
    await intr.send(embeds = [embed])

@bot.slash_command(description = "Set a user's level and XP")
async def set_level(intr: nextcord.Interaction, member: nextcord.Member = nextcord.SlashOption(name = "user"), level: int = nextcord.SlashOption(name = "level"), xp: int = nextcord.SlashOption(name = "xp")):
    # Exit if the command executor doesn't have admin permissions
    if not intr.channel.permissions_for(intr.user).administrator:
        embed = createEmbed(None, "Only admins can use this command.", "", intr.user, 0xFF0000)
        await intr.send(embeds = [embed])
        return
    # Set new user XP
    user = db.getUser(intr.guild, member)
    user.setCachedName(member.name)
    user.level.setLevel(level, xp)
    db.saveUser(user)
    # Success message
    embed = createEmbed(member, f"Set to {user.level}", "", intr.user, 0x00FF00)
    await intr.send(embeds = [embed])

@bot.slash_command(description = "Get the leaderboard for a guild")
async def leaderboard(intr: nextcord.Interaction, page: int = nextcord.SlashOption(name = "page", required = False)):
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
        leaderboardText += f"{1 + i + page * config.pageSize}. {user.getCachedName()}, {user.level}\n"
    # Send embed
    embed = createEmbed(intr.guild, f"Leaderboard, page {page + 1}/{maxPages + 1}", leaderboardText, intr.user, 0x00FF00)
    await intr.send(embeds = [embed])

bot.run(config.botToken)