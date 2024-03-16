import nextcord
import nextcord.ext.commands as commands
import embed

class RoleButtons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Hardcoded role buttons
    @commands.Cog.listener("on_interaction")
    async def on_interaction(self, intr):
        rolesMessage = 1010024261659918396
        robotButton = "reaction_roles.button.1010024258791018496"
        humanButton = "reaction_roles.button.1010024258790891520"
        robotRole = 1005309355182260327
        humanRole = 831569900777635922
        # Wrong message
        if not intr.message or intr.message.id != rolesMessage:
            return

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