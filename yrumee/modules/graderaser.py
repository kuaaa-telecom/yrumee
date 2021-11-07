import discord

from yrumee.modules import Module


class GradEraserModule(Module):
    """
    <대학원 제거기>
    [.대학원생] 대학원생 목록 표시
    [.대학원갈래요] 대학원제거기 비활성화
    [.대학원안가요] 대학원제거기 활성화
    [.대학원에 @대상 살아요] 대학원생 목록에 해당 유저 등록 (ex. .대학원에 @이건우 살아요)
    [.교수님 @대상 안보여요] 대학원생 목록에 해당 유저 삭제 (ex. .교수님 @이건우 안보여요)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_active = False
        self.slaves = self.storage_instance.get("slaves", [])

    async def on_command(self, command: str, payload: str, message: discord.Message):
        if command == "대학원생":
            await message.channel.send(f"쿠아의 대학원생들 : {self.slaves}")
        elif command == "대학원안가요":
            if self.is_active is False:
                self.is_active = True
                await message.add_reaction("👌")
        elif command == "대학원갈래요":
            if self.is_active is True:
                self.is_active = False
                await message.add_reaction("👌")
        elif command == "대학원에":
            slave = message.mentions[0].id
            self.slaves.append(slave)
            await message.add_reaction("👌")
        elif command == "교수님":
            slave = message.mentions[0].id
            if slave in self.slaves:
                self.slaves.pop(self.slaves.index(slave))
                await message.add_reaction("👌")
            else:
                await message.add_reaction("❓")

    async def on_message(self, message: discord.Message) -> bool:
        if (
            "대학원" in message.content
            and self.is_active
            and message.author.id in self.slaves
        ):
            await message.delete()
            await message.channel.send("대학원은 여름이가 치워버렸다냥!")
        return False
