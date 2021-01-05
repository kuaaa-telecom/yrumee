import discord


class Module:
    async def on_message(self, message: discord.Message) -> bool:
        return False

    async def on_command(
        self, command: str, payload: str, message: discord.Message
    ) -> bool:
        return False
