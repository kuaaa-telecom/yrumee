import asyncio
import io
from collections import defaultdict
from typing import Dict

import aiohttp
import discord

from config import config
from config_secrets import PINGPONG_API_TOKEN
from yrumee.modules import Module


class PingpongModule(Module):

    PINGPONG_API_URL = "https://builder.pingpong.us/api/builder/5ff7d083e4b078d8738c6f8e/integration/v0.2/custom/{sessionId}"
    CONTEXT_TIMEOUT = 1.5
    PRESERVE_CONTEXT_TIMEOUT = 10

    session = None
    contexts = {}
    scheduled_request = {}
    clear_context_task = {}
    preserve_context: Dict[str, bool] = defaultdict(lambda: False)

    async def _get_image_from_url(self, url):
        resp = await self.session.get(url)
        if resp.status != 200:
            return
        data = io.BytesIO(await resp.read())
        return discord.File(data, "image.png")

    async def _clear_context(self, key):
        self.contexts[key] = []
        await asyncio.sleep(self.PRESERVE_CONTEXT_TIMEOUT)
        self.preserve_context[key] = False

    async def _request_pingpong(self, key, message):
        context = self.contexts[key]
        immediate = len(context) >= 5

        if not immediate:
            if self.scheduled_request.get(key, False) is True:
                return
            self.scheduled_request[key] = True
            await asyncio.sleep(self.CONTEXT_TIMEOUT)

        if not self.session:
            self.session = aiohttp.ClientSession()

        try:
            response = await self.session.post(
                self.PINGPONG_API_URL.format(sessionId=key),
                json={"request": {"dialog": context}},
                headers={"Authorization": "Basic {}".format(config.pingpong_api_token)},
            )
            json = await response.json()

            for reply in json["response"]["replies"]:
                print(reply["from"])
                if reply["type"] == "text":
                    await message.channel.send(reply["text"])
                elif reply["type"] == "image":
                    await message.channel.send(
                        file=(await self._get_image_from_url(reply["image"]["url"]))
                    )
        except Exception as e:
            print(e)

        self.scheduled_request[key] = False
        if key in self.clear_context_task:
            self.clear_context_task[key].cancel()
        self.clear_context_task[key] = asyncio.create_task(self._clear_context(key))

    async def on_message(self, message: discord.Message) -> bool:
        is_myself_mentioned = any([m.id == config.bot_id for m in message.mentions])

        if is_myself_mentioned:
            self.contexts[message.author.id] = []
            self.preserve_context[message.author.id] = True

        if self.preserve_context[message.author.id] is True:
            self.contexts[message.author.id].append(message.content)
            await self._request_pingpong(key=message.author.id, message=message)
            return True
        else:
            return False
