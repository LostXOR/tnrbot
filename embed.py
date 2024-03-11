import nextcord
from datetime import datetime

def createEmbed(object, title, description, author, color):
    embed = nextcord.Embed(title = title, description = description, color = color, timestamp = datetime.now())
    name = object.name if object else ""
    if isinstance(object, nextcord.Member): icon = object.display_avatar.url
    elif isinstance(object, nextcord.Guild): icon = object.icon.url if object.icon else None
    else: icon = None
    embed.set_author(name = name, icon_url = icon)
    if author: embed.set_footer(text = "Requested by " + author.name, icon_url = author.display_avatar.url)
    return embed