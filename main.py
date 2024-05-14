import asyncio

import discord
from dotenv import dotenv_values

from src.bot import Bot
from src.commands import BotManagementCommands


async def main():
    config = dotenv_values()
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    commands = [
        BotManagementCommands
    ]

    async with Bot(command_prefix="\\", intents=intents, commands=commands) as bot:
        await bot.start(config["DISCORD_TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())
