import datetime
import time

import discord

from yrumee.modules import Module

class EverydayModule(Module):
    """
    [.날짜켜기] 여름이가 매일 오전 12시 정각에 날짜와 요일을 알려줍니다.
    [.날짜끄기] 여름이가 매일 오전 12시 정각에 날짜와 요일을 알려주지 않습니다.
    """
    is_active = False

    #기능 on/off
    async def on_command(self, command: str, message: discord.Message):
        if command == "날짜켜기":
            if self.is_active is False:
                await message.channel.send("내일부터 날짜와 요일을 알려준다냥.")
                self.is_active = True
        elif command == "날짜끄기":
            if self.is_active is True:
                await message.channel.send("내일부터 날짜와 요일을 알려주지 않는다냥.")
                self.is_active = False


    def __init__(self, storage_instance):
        self.dow = storage_instance.get("dow", ["월", "화", "수", "목", "금", "토", "일"])

    async def on_time(self, now=time.localtime()):
        dow_dic = {0:'등교랑 출근 힘내라냥!', 1:'서두르지 말고 천천히 하라냥!', 2:'벌써 한 주의 중간이다냥!', 3:'곧 주말이다냥! 파이팅이다냥!', 4:'불금! 내일은 주말이다냥!', 5:'오늘 하루 여유롭게 푹 쉬라냥!', 6:'슬슬 다음 주를 준비하자냥!'}
        if is_active == True and now.tm_hour == 00 and now.tm_min == 00 and now.tm_sec == 00:
                await message.channel.send("오늘은 {0}월 {1}일 {2}요일이다냥!" .format(now.tm_month, now.tm_mday, dow[datetime.datetime.today().weekday()]))
                await message.channel.send(dow_dic.get(datetime.datetime.today().weekday()))
