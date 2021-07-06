import discord

from yrumee.modules import Module


class ReactionModule(Module):
    """
    [.리액션] 특정인이 특정 단어 또는 이모티콘을 사용하면, 여름이가 그 메시지에 리액션을 합니다.
    예) .리액션 @대상 [리액션할 단어] [:리액션할-이모티콘:]
    '리액션할-이모티콘' 자리에 ❌ 이모지를 입력하는 경우 해당 단어에 대한 리액션이 삭제됩니다.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_ids = self.storage_instance.get("target_ids", {})

    async def on_command(self, command: str, payload: str, message: discord.Message):
        if command == "리액션":
            if len(message.mentions) < 1:
                await message.channel.send("사용법: .리액션 @대상 [리액션할 단어] [:리액션할_이모티콘:]")
                return

            target_id = message.mentions[0].id

            _, word, emoji = payload.split(" ", 2)
            if target_id not in self.target_ids:
                self.target_ids[target_id] = {}

            if emoji == "❌":
                self.target_ids[target_id].pop(word)
                await message.channel.send("삭제 완료!")
            else:
                self.target_ids[target_id][word] = emoji
                await message.channel.send("등록 완료!")

    async def on_message(self, message: discord.Message) -> bool:
        for word, emoji in self.target_ids.get(message.author.id, {}).items():
            if word in message.content:
                await message.add_reaction(emoji)

        return False
