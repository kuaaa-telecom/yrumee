import discord

from yrumee.storage import StorageInstance

class Module:
    def __init__(self, storage_instance: StorageInstance):
        self.storage_instance = storage_instance

    async def on_message(self, message: discord.Message) -> bool:
        return False

    async def on_command(
        self, command: str, payload: str, message: discord.Message
    ) -> bool:
        return False
