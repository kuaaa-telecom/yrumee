import discord

from yrumee.modules import Module


class GradSchoolModule(Module):
    '''
    <대학원 제거기>
    [.대학원갈래요] 대학원제거기 비활성화
    [.대학원안가요] 대학원제거기 활성화
    [.대학원에 (유저명) 살아요] 대학원생 목록에 해당 유저 등록 (ex. .대학원에 이건우 살아요)
    [.교수님 (유저명) 안보여요] 대학원생 목록에 해당 유저 삭제 (ex. .교수님 이건우 안보여요)
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
