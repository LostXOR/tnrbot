import nextcord
import nextcord.ext.commands as commands
import embed

class RoleButtons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Hardcoded role buttons
    @commands.Cog.listener("on_interaction")
    async def on_interaction(self, intr):
        roles_message = 1010024261659918396
        robot_button = "reaction_roles.button.1010024258791018496"
        human_button = "reaction_roles.button.1010024258790891520"
        robot_role = 1005309355182260327
        human_role = 831569900777635922
        # Wrong message
        if not intr.message or intr.message.id != roles_message:
            return

        # Figure out what roles need to be added and removed
        if intr.data["custom_id"] == robot_button:
            role_to_remove = robot_role if intr.user.get_role(robot_role) else human_role if intr.user.get_role(human_role) else None
            role_to_add = robot_role if not intr.user.get_role(robot_role) else None
        elif intr.data["custom_id"] == human_button:
            role_to_remove = human_role if intr.user.get_role(human_role) else robot_role if intr.user.get_role(robot_role) else None
            role_to_add = human_role if not intr.user.get_role(human_role) else None
        # Send response to interaction
        if role_to_add and not role_to_remove: embed_text = f"Added <@&{role_to_add}>"
        elif role_to_remove and not role_to_add: embed_text = f"Removed <@&{role_to_remove}>"
        else: embed_text = f"Added <@&{role_to_add}> and removed <@&{role_to_remove}>"
        await intr.send(embeds = [
            embed.create_embed(intr.user, "", embed_text, intr.user, 0x00FF00)
        ], ephemeral = True)
        # Add/remove roles
        if role_to_add: await intr.user.add_roles(nextcord.Object(role_to_add))
        if role_to_remove: await intr.user.remove_roles(nextcord.Object(role_to_remove))