import random

import discord

from yrumee.modules import Module


class LottoModule(Module):
    is_active = False

    async def on_command(self, command: str, payload: str, message: discord.Message):
        if command == "로또":
            lotto_num = sorted([random.randint(1, 46) for _ in range(6)], reverse=False)
            lotto_num = " ".join([str(x) for x in lotto_num])
            await message.channel.send("여름이의 로또 픽: {}".format(lotto_num))
