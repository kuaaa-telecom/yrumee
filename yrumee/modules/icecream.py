import discord

from yrumee.modules import Module


class IcecreamModule(Module):
    """
    [.아이스크림] 🍦
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icecreams = self.storage_instance.get("icecreams", {})

    async def on_command(self, command: str, payload: str, message: discord.Message):
        if command == "아이스크림":
            target_id = message.mentions[0].id
            if target_id:
                if target_id not in self.icecreams:
                    self.icecreams[target_id] = True
                else:
                    self.icecreams[target_id] = not self.icecreams[target_id]
                await message.channel.send(
                    "{} 완료!".format("등록" if self.icecreams[target_id] else "삭제")
                )

    async def on_message(self, message: discord.Message) -> bool:
        if message.content == "아":
            for id, icecream in self.icecreams.items():
                if id == message.author.id and icecream:
                    await message.channel.send("이스크림")
                    return True
        return False
