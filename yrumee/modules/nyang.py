import discord

from yrumee.modules import Module


class NyangModule(Module):
    """
[.냥하] 여름이가 고양이에 관련한 단어에 반응하도록 합니다.
[.냥바] 여름이가 고양이에 관련한 단어에 반응하지 않도록 합니다.
    """
    is_active = False

    async def on_command(self, command: str, payload: str, message: discord.Message):
        if command == "냥하":
            if self.is_active is False:
                await message.channel.send("냥하 🐈")
                self.is_active = True
        elif command == "냥바":
            if self.is_active is True:
                await message.channel.send("냥바 👋")
                self.is_active = False

    async def on_message(self, message: discord.Message) -> bool:
        # 냥냥이
        cat_count = 0
        for cat in ["냥", "야옹", "고영", "고양"]:
            cat_count += message.content.count(cat)

        if self.is_active and cat_count > 0:
            await message.channel.send("냥" * cat_count)
            return True

        return False
