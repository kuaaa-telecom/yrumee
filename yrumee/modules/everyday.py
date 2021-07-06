import datetime
import time

import discord

from yrumee.modules import Module


class EverydayModule(Module):
    """
    [.날짜켜기] 여름이가 매일 오전 12시 정각에 날짜와 요일을 알려줍니다.
    [.날짜끄기] 여름이가 매일 오전 12시 정각에 날짜와 요일을 알려주지 않습니다.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dow = self.storage_instance.get("dow", ["월", "화", "수", "목", "금", "토", "일"])
        # TODO: storage 활용
        self.is_active = False
        self.target_channel_id = ""

    # 기능 on/off
    async def on_command(self, command: str, payload: str, message: discord.Message):
        if command == "날짜켜기":
            if self.is_active is False:
                self.is_active = True
                self.target_channel_id = message.channel.id
                await message.channel.send("내일부터 날짜와 요일을 알려준다냥.")
        elif command == "날짜끄기":
            if self.is_active is True:
                self.is_active = False
                self.target_channel_id = message.channel.id
                await message.channel.send("내일부터 날짜와 요일을 알려주지 않는다냥.")

    async def on_timer_elapse(self, datetime):
        if not (datetime.hour == 0 and datetime.minute == 0):
            return False

        dow_dic = {
            0: "등교랑 출근 힘내라냥!",
            1: "지치지 말고 차분하게 하루를 보내자냥!",
            2: "벌써 한 주의 중간이다냥!",
            3: "곧 주말이다냥! 파이팅이다냥!",
            4: "불금! 내일은 주말이다냥!",
            5: "오늘 하루 여유롭게 푹 쉬라냥!",
            6: "남은 주말을 즐기자냥!",
        }
        if self.is_active == True:
            channel = self.server and self.server.get_channel(self.target_channel_id)
            if channel is not None:
                await channel.send(
                    "오늘은 {0}월 {1}일 {2}요일이다냥!".format(
                        datetime.month,
                        datetime.day,
                        self.dow[datetime.today().weekday()],
                    )
                )
                await channel.send(dow_dic.get(datetime.today().weekday()))
                return True
        return False
