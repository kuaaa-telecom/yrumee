import discord

from yrumee.modules import Module


class GradSchoolModule(Module):
    '''
    [.] GradSchool : 대학원 제거기
    '''
    is_active = False

    async def on_command(self, command: str, payload: str, message: discord.Message):
        if command == "대학원안가요":
            if self.is_active is False:
                self.is_active = True
                await message.add_reaction("👌")
        elif command == "대학원갈래요":
            if self.is_active is True:
                self.is_active = False
                await message.add_reaction("👌")


    async def on_message(self, message: discord.Message) -> bool:
        if "대학원" in message.content and self.is_active:
            await message.delete()
            await message.channel.send("대학원은 여름이가 치워버렸다냥!")
        return False
