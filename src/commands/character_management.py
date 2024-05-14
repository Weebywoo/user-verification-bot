from typing import Optional

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from src.functions import detect_reasons, get_date_from_message


class BotManagementCommands(commands.Cog, description="Bot management commands"):
    path: str = __name__

    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.open_ticket_ids: list[int] = []
        self.ticket_reviewer: Optional[discord.Role] = None
        self.ticket_category: Optional[str] = None
        self.role_to_remove: Optional[discord.Role] = None
        self.role_to_add: Optional[discord.Role] = None

    @commands.command(name="ping")
    async def ping(self, context: commands.Context):
        await context.channel.send("pong!")

    @commands.command()
    @commands.has_any_role("Server Lead", "Admin", "Moderator")
    async def config(self, context: commands.Context):
        await context.channel.send(
            f"Open ticket channel ids: {'.'.join(map(str, self.open_ticket_ids))}\n" +
            f"Ticket reviewer: {self.ticket_reviewer}\n" +
            f"Ticket category: {self.ticket_category}\n" +
            f"Role to remove: {self.role_to_remove}\n" +
            f"Role to add: {self.role_to_add}")

    @commands.command(name="setTicketReviewer")
    @commands.has_any_role("Server Lead", "Admin", "Moderator")
    async def set_reviewer(self, context: commands.Context, reviewer: discord.Role):
        self.ticket_reviewer = reviewer

        await context.channel.send(f"Reviewer set to {reviewer.name}.")

    @commands.command(name="setRoleToRemove")
    @commands.has_any_role("Server Lead", "Admin", "Moderator")
    async def set_role_to_remove(self, context: commands.Context, role: discord.Role):
        self.role_to_remove = role

        await context.channel.send(f"Role to remove set to {role.name}.")

    @commands.command(name="setRoleToAdd")
    @commands.has_any_role("Server Lead", "Admin", "Moderator")
    async def set_role_to_add(self, context: commands.Context, role: discord.Role):
        self.role_to_add = role

        await context.channel.send(f"Role to add set to {role.name}.")

    @commands.command(name="setTicketCategory")
    @commands.has_any_role("Server Lead", "Admin", "Moderator")
    async def set_ticket_category(self, context: commands.Context, ticket_category: str):
        category = discord.utils.get(self.bot.guilds[0].categories, name=ticket_category)

        if category is None:
            await context.channel.send(f"Category '{ticket_category}' does not exist.")

        else:
            self.ticket_category = ticket_category

            await context.channel.send(f"Ticket category set to {ticket_category}.")

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.TextChannel):
        if channel.category.name == self.ticket_category and channel.name.startswith("ageverify"):
            print(f"Added channel {channel.name} with id {channel.id} to watcher list.")

            self.open_ticket_ids.append(channel.id)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.author.bot and message.channel.id in self.open_ticket_ids:
            date = get_date_from_message(message)
            reasons = detect_reasons(message, date)

            if reasons is None:
                await message.author.remove_roles(self.role_to_remove)
                await message.author.add_roles(self.role_to_add)

                if self.role_to_add in message.author.roles:
                    await message.channel.send(f"Added role {self.role_to_add} to you!")

                else:
                    await message.channel.send(f"Something went wrong! {self.ticket_reviewer.mention}")

            else:
                reason_message = "\n".join("- " + reason for reason in reasons)

                await message.channel.send(
                    f"A reviewer will be with you shortly.\nReasons:\n{reason_message}\n{self.ticket_reviewer.mention}")

                print(f"Remove channel {message.channel.name} with id {message.channel.id} from watcher list.")

            self.open_ticket_ids.remove(message.channel.id)

    async def cog_command_error(self, context: commands.Context, error: commands.CommandError):
        await context.message.reply(str(error))


async def setup(bot: Bot):
    await bot.add_cog(BotManagementCommands(bot))
