import discord

from yrumee.ext.pyjosa import replace_josa
from yrumee.modules import Module


class CuteModule(Module):
    """
[.귀여운사람] '이 서버에서 제일 귀여운 사람'을 등록합니다.
여름이에게 `여름아 세상에서 제일 귀여운 사람은?`이라고 물어보면 등록된 사람을 알려줍니다.
    """
    cute_person = ""

    async def on_command(self, command: str, payload: str, message: discord.Message):
        if command == "귀여운사람":
            self.cute_person = payload
            await message.channel.send("등록 완료!")

    async def on_message(self, message: discord.Message) -> bool:
        if not self.cute_person:
            return False
        # 여름아 여름아 세상에서 제일 귀여운 사람은?
        eun = message.content.replace("여름아", "").replace(" ", "")
        if message.content.startswith("여름아") and "세상에서제일귀여운사람" in eun:
            await message.channel.send(
                "{}{}".format(
                    replace_josa("{}(이)요".format(self.cute_person)),
                    "!" * eun.count("?"),
                )
            )
            return True
        else:
            return False
