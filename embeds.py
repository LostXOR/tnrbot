"""A function to quickly create standardized embeds."""

from datetime import datetime
import nextcord

def create_embed(obj, title, description, author, color):
    """Yup, this is the function. :)"""
    embed = nextcord.Embed(
        title = title,
        description = description,
        color = color,
        timestamp = datetime.now()
    )
    # Get correct name and URL to display from object
    name = obj.name if obj else ""
    if isinstance(obj, nextcord.Member):
        icon = obj.display_avatar.url
    elif isinstance(obj, nextcord.Guild):
        icon = obj.icon.url if obj.icon else None
    else:
        icon = None

    embed.set_author(name = name, icon_url = icon)
    if author:
        embed.set_footer(text = "Requested by " + author.name, icon_url = author.display_avatar.url)
    return embed
