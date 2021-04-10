import random

import discord

from yrumee.modules import Module


class StackModule(Module):
    """
[.푸시] 스택에 푸시를 합니다.
[.팝] 스택에 푸시한 값을 팝하여 출력합니다.
    """
    is_active = False
    stack = []

    async def on_command(self, command: str, payload: str, message: discord.Message):
        if command == "푸시":
            self.stack.append(payload)

        if command == "팝":
            if len(self.stack) > 0:
                await message.channel.send(self.stack.pop())
