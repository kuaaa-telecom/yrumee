import discord

from yrumee.modules.cute import CuteModule
from yrumee.modules.lotto import LottoModule
from yrumee.modules.nyang import NyangModule
from yrumee.modules.stack import StackModule


class YrumeeClient(discord.Client):

    modules = [
        NyangModule(),
        LottoModule(),
        StackModule(),
        CuteModule(),
    ]

    async def on_ready(self):
        print(self.modules[0].__class__.__name__)
        print("Logged on as {0}!".format(self.user))

    async def on_message(self, message: discord.Message):
        if message.author.id == self.user.id:  # type: ignore
            return
        print("Message from {0.author}: {0.content}".format(message))

        if message.content.startswith("."):
            cp = message.content.split(" ", 1)
            if len(cp) == 1:
                command, payload = cp[0], ""
            else:
                command, payload = cp
            await self.on_command(command.lstrip("."), payload, message)
        else:
            await self.on_text(message)

    async def on_command(self, command, payload, message: discord.Message):
        for module in self.modules:
            await module.on_command(command, payload, message)

    async def on_text(self, message: discord.Message):
        for module in self.modules:
            if await module.on_message(message) is True:
                break
