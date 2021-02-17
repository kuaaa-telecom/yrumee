from collections import defaultdict

import discord

from yrumee.modules import Module


class ReactionModule(Module):
    is_active = False
    target_ids = defaultdict(lambda: {})

    async def on_command(self, command: str, payload: str, message: discord.Message):
        if command == "리액션":
            if len(message.mentions) < 1:
                await message.channel.send("사용법: .리액션 @대상 [:리액션할_이모티콘:] [리액션할 단어]")
                return

            target_id = message.mentions[0].id

            _, emoji, word = payload.split(" ", 2)
            self.target_ids[target_id][word] = emoji
            await message.channel.send("등록 완료!")

    async def on_message(self, message: discord.Message) -> bool:
        for word, emoji in self.target_ids[message.author.id].items():
            if word in message.content:
                await message.add_reaction(emoji)

        return False