from typing import Dict, List

import discord

from yrumee.modules import Module
from yrumee.modules.covid19 import COVID19Module
from yrumee.modules.everyday import EverydayModule
from yrumee.modules.graderaser import GradEraserModule
from yrumee.modules.log import LogModule
from yrumee.modules.lotto import LottoModule
from yrumee.modules.mbti import MBTIModule
from yrumee.modules.nyang import NyangModule
from yrumee.modules.reaction import ReactionModule
from yrumee.modules.sora import SoraModule
from yrumee.modules.stack import StackModule
from yrumee.modules.teraforming import TeraformingModule
from yrumee.modules.what_to_eat import WhatToEatModule
from yrumee.modules.yrumee import YrumeeModule
from yrumee.storage import Storage


class YrumeeClient(discord.Client):

    modules: Dict[str, List[Module]] = {}
    storage: Storage

    def new_module(self, server_id: str) -> List[Module]:
        storage = self.storage.of(server_id)
        return [
            NyangModule(storage),
            LottoModule(storage),
            StackModule(storage),
            MBTIModule(storage),
            YrumeeModule(storage),
            COVID19Module(storage),
            ReactionModule(storage),
            SoraModule(storage),
            LogModule(storage),
            WhatToEatModule(storage),
            GradEraserModule(storage),
            TeraformingModule(storage),
            EverydayModule(storage)
        ]

    async def on_ready(self):
        print("Logged on as {0}!".format(self.user))

    async def get_helps(self, modules: List[Module], message: discord.Message):
        help_str = "".join(
            [
                "\n".join([m.lstrip() for m in (module.__doc__ or "").split("\n")])
                or ""
                for module in modules
            ]
        )
        await message.channel.send("여름이 🐈\n{}".format(help_str))

    async def on_message(self, message: discord.Message):
        if message.author.id == self.user.id:  # type: ignore
            return

        server_id = str(message.guild.id)

        if server_id not in self.modules:
            self.modules[server_id] = self.new_module(server_id)

        if message.content.startswith("."):
            cp = message.content.split(" ", 1)
            if len(cp) == 1:
                command, payload = cp[0], ""
            else:
                command, payload = cp

            command = command.lstrip(".")
            if command == "도움말":
                await self.get_helps(self.modules[server_id], message)
            elif command:
                await self.on_command(command, payload, message)
        else:
            await self.on_text(message)

    async def on_command(self, command, payload, message: discord.Message):
        server_id = str(message.guild.id)

        for module in self.modules[server_id]:
            await module.on_command(command, payload, message)

    async def on_text(self, message: discord.Message):
        server_id = str(message.guild.id)

        for module in self.modules[server_id]:
            if await module.on_message(message) is True:
                break
