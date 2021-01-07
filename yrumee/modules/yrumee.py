import discord

from yrumee.modules import Module


class YrumeeModule(Module):
    async def on_message(self, message: discord.Message) -> bool:
        if "여름이" in message.content:
            await message.add_reaction("🐈")
        return False
