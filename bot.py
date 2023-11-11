import nextcord, config, db, embed

# Initialize database and bot
db = db.Database(config.databasePath)
bot = nextcord.Client(intents = nextcord.Intents.all())

@bot.event
async def on_ready():
    # Set status to "Playing Whack-a-MEE6"
    status = nextcord.Game("Whack-a-MEE6")
    await bot.change_presence(activity = status)
    print("Bot started")

# Hardcoded role buttons
@bot.event
async def on_interaction(intr):
    rolesMessage = 1010024261659918396
    robotButton = "reaction_roles.button.1010024258791018496"
    humanButton = "reaction_roles.button.1010024258790891520"
    robotRole = 1005309355182260327
    humanRole = 831569900777635922
    # Wrong message
    if not intr.message or intr.message.id != rolesMessage:
        await bot.process_application_commands(intr)
    # Figure out what roles need to be added and removed
    if intr.data["custom_id"] == robotButton:
        roleToRemove = robotRole if intr.user.get_role(robotRole) else humanRole if intr.user.get_role(humanRole) else None
        roleToAdd = robotRole if not intr.user.get_role(robotRole) else None
    elif intr.data["custom_id"] == humanButton:
        roleToRemove = humanRole if intr.user.get_role(humanRole) else robotRole if intr.user.get_role(robotRole) else None
        roleToAdd = humanRole if not intr.user.get_role(humanRole) else None
    # Send response to interaction
    if roleToAdd and not roleToRemove: embedText = f"Added <@&{roleToAdd}>"
    elif roleToRemove and not roleToAdd: embedText = f"Removed <@&{roleToRemove}>"
    else: embedText = f"Added <@&{roleToAdd}> and removed <@&{roleToRemove}>"
    await intr.send(embeds = [
        embed.createEmbed(intr.user, "", embedText, intr.user, 0x00FF00)
    ], ephemeral = True)
    # Add/remove roles
    if roleToAdd: await intr.user.add_roles(nextcord.Object(roleToAdd))
    if roleToRemove: await intr.user.remove_roles(nextcord.Object(roleToRemove))

@bot.event
async def on_message(msg):
    # Respond to mistypings of !rank (Added at the request of TinRobit)
    if msg.content == "!raml":
        await msg.channel.send("https://imgur.com/a/fHdLJZU")
    elif msg.content == "!rabk":
        await msg.channel.send("<:roboHolyDivided0:834465408135987220>")
    # Respond to "/halp" with bird chopsticks picture (sent by LesPaulII)
    elif msg.content == "/halp":
        await msg.channel.send(files = [nextcord.File("bird_halp.jpg")])

    if msg.author.bot: return
    # Get user data from database and update cached name
    user = db.getUser(msg.guild, msg.author)
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
    db.saveUser(user)

@bot.slash_command(description = "Get a user's level")
async def level(intr: nextcord.Interaction, member: nextcord.Member = nextcord.SlashOption(name = "user", required = False)):
    # Fetch user data
    member = member if member else intr.user
    user = db.getUser(intr.guild, member)
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
    user = db.getUser(intr.guild, member)
    user.setCachedName(member.name)
    user.level.setLevel(level, xp)
    db.saveUser(user)
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
    userCount = db.getUserCount(intr.guild)
    maxPages = (userCount - 1) // config.pageSize
    page = min(max(page, 0), maxPages)
    # Get leaderboard page
    leaderboard = db.getLeaderboard(intr.guild, page * config.pageSize, config.pageSize)
    # Generate leaderboard text
    leaderboardText = ""
    for i in range(len(leaderboard)):
        user = leaderboard[i]
        leaderboardText += f"{1 + i + page * config.pageSize}. {user.getCachedName()}, {user.level}\n"
    # Send embed
    await intr.send(embeds = [
        embed.createEmbed(intr.guild, f"Leaderboard, page {page + 1}/{maxPages + 1}", leaderboardText, intr.user, 0x00FF00)
    ])

bot.run(config.botToken)
