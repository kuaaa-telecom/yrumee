import logging
import os
import time

import discord

from yrumee.modules import Module


class LogModule(Module):
    """
    [.채팅수집동의] 이 계정의 `채팅 내역 수집`에 동의합니다.
    [.채팅수집동의내역] 이 계정의 `채팅 내역 수집` 동의 현황을 가져옵니다. 동의한 적이 없는 경우, 기본값은 동의하지 않은 상태입니다.
    [.채팅수집동의거부] 이 계정의 `채팅 내역 수집` 동의를 철회합니다.
    """

    @staticmethod
    def add_file_handler(filename):
        FORMAT = "[%(asctime)s]%(message)s;;;"
        directory = os.path.join(os.getcwd(), "logs")
        if not os.path.isdir(directory):
            os.makedirs(directory)

        fh = logging.FileHandler(os.path.join(directory, filename))
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter(FORMAT))
        return fh

    def __init__(self, storage_instance):
        self.agree_status = storage_instance.get("chat_log_agree_status", {})
        handlers = [
            self.add_file_handler("yrumee-{}.log".format(int(time.time()))),
            logging.StreamHandler(),
        ]
        self.logger = logging.getLogger()
        self.logger.handlers = handlers
        self.logger.setLevel(logging.INFO)

    async def on_command(self, command: str, payload: str, message: discord.Message):
        name = message.author.display_name
        by = message.author.id

        if command.lower() == "채팅수집동의":
            self.agree_status[by] = True
            await message.author.send(
                "[채팅수집-동의] {}님의 채팅내역 수집 동의가 정상적으로 처리되었습니다.".format(name)
            )
        elif command.lower() == "채팅수집동의내역":
            status = "동의하였습니다" if self.agree_status.get(by, False) else "동의하지 않으셨습니다"
            await message.author.send(
                "[채팅수집-동의내역] {}님은 채팅내역 수집에 {}.".format(name, status)
            )
        elif command.lower() == "채팅수집동의거부":
            self.agree_status[by] = False
            await message.author.send(
                "[채팅수집-동의] {}님의 채팅내역 수집 동의 거부가 정상적으로 처리되었습니다.".format(name)
            )

    async def on_message(self, message: discord.Message) -> bool:
        self.logger.info(
            "[{0.author}][{guild_id}][{author_id}] {0.content}".format(
                message, guild_id=message.guild.id, author_id=message.author.id
            )
        )
        return False
