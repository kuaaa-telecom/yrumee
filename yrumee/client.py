import discord

from yrumee.modules.covid19 import COVID19Module
from yrumee.modules.cute import CuteModule
from yrumee.modules.lotto import LottoModule
from yrumee.modules.mbti import MBTIModule
from yrumee.modules.nyang import NyangModule
from yrumee.modules.pingpong import PingpongModule
from yrumee.modules.reaction import ReactionModule
from yrumee.modules.stack import StackModule
from yrumee.modules.yrumee import YrumeeModule


class YrumeeClient(discord.Client):

    modules = {}

    def new_module(self):
        return [
            NyangModule(),
            LottoModule(),
            StackModule(),
            MBTIModule(),
            YrumeeModule(),
            COVID19Module(),
            ReactionModule(),
            # PingpongModule(),
            # CuteModule(),
        ]

    async def on_ready(self):
        print("Logged on as {0}!".format(self.user))

    async def on_message(self, message: discord.Message):
        if message.author.id == self.user.id:  # type: ignore
            return
        print("Message from {0.author}: {0.content}".format(message))

        if message.guild.id not in self.modules:
            self.modules[message.guild.id] = self.new_module()

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
        for module in self.modules[message.guild.id]:
            await module.on_command(command, payload, message)

    async def on_text(self, message: discord.Message):
        for module in self.modules[message.guild.id]:
            if await module.on_message(message) is True:
                break
