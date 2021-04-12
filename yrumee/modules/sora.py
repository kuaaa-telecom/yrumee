from collections import defaultdict

import discord
import random

from yrumee.modules import Module

class SoraModule(Module):

    contents = [
        "그걸 말이라고 하냥!?",
        "당연하다냥!",
        "절대 안 된다냥!",
        "안 된다냥..",
        "언젠가는 될 거다냥!",
        "다시 한번 물어봐냥!",
        "된다냥!",
    ]

    async def on_message(self, message: discord.Message) -> bool:

        if message.content.startswith("여름아") and message.content.endswith("?"):
            content = random.choice(self.contents)
            await message.channel.send("<@{}> {}".format(message.author.id, content))

        return False
