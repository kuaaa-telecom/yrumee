from datetime import datetime

import discord

from yrumee import YrumeeClient
from yrumee.storage import StorageInstance


class Module:
    def __init__(self, yrumee_client: YrumeeClient, server_id: str):
        storage_instance = yrumee_client.storage.of(server_id)
        self.client = yrumee_client
        self.server_id = server_id
        self.storage_instance = storage_instance

    @property
    def server(self):
        return self.client.get_guild(self.server_id)

    async def on_time_elapse(self, dt: datetime) -> bool:
        return False

    async def on_message(self, message: discord.Message) -> bool:
        return False

    async def on_command(
        self, command: str, payload: str, message: discord.Message
    ) -> bool:
        return False

    async def on_message_delete(self, message: discord.Message) -> bool:
        return False
