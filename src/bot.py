import json

import discord
from discord.ext import commands


class Bot(commands.Bot):
    def __init__(self, commands: list[type[commands.Cog]] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._commands = commands

    async def setup_hook(self) -> None:
        if self._commands is not None:
            for extension in self._commands:
                await self.load_extension(extension.path)

        loaded_cogs = {cog_name: cog_cls.description for cog_name, cog_cls in self.cogs.items()}
        print(f"Cogs loaded:\n{json.dumps(loaded_cogs, indent=2)}")

    async def on_ready(self) -> None:
        print(f"Logged in as '{self.user}'")

    async def on_message(self, message: discord.Message) -> None:
        context = await self.get_context(message)

        if context.valid:
            if context.command:
                print(f"'{message.author}' used '{context.command}'")

                await self.process_commands(message)
