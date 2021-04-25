import random

import discord

from yrumee.modules import Module


class LottoModule(Module):
    """
    [.로또] 여름이가 추천하는 로또 번호를 출력합니다.
    """

    async def on_command(self, command: str, payload: str, message: discord.Message):
        if command == "로또":
            lotto_num = sorted(random.sample(range(1, 46), 6))
            lotto_num = " ".join([str(x) for x in lotto_num])
            await message.channel.send("여름이의 로또 픽: {}".format(lotto_num))
