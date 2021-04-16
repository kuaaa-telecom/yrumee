
import random
import discord
from datetime import datetime

from yrumee.modules import Module


class WhatToEatModule(Module):
    """
[.점심] 점심에 먹을만한 식사의 종류 혹은 밥집을 추가합니다.
[.저녁] 저녁에 먹을만한 식사의 종류 혹은 밥집을 추가합니다.
[.야식] 야식으로 먹을만한 식사의 종류 혹은 밥집을 추가합니다.
[.오늘뭐먹지] [.뭐먹] 오늘 뭐를 먹을지 여름이에게 물어봅니다.
    """
    def __init__(self, storage_instance):
        self.lunch = storage_instance.get('lunch', [])
        self.dinner = storage_instance.get('dinner', [])
        self.yasik = storage_instance.get('yasik', [])

    async def on_command(self, command: str, payload: str, message: discord.Message):

        if command in ["점심", "저녁", "야식"]:
            if not payload:
                await message.channel.send("사용법: .{0} {0}에-먹을만한-음식".format(command))
            else:
                if command == "점심":
                    self.lunch.append(payload)
                elif command == "저녁":
                    self.dinner.append(payload)
                elif command == "야식":
                    self.yasik.append(payload)
                await message.channel.send("등록 완료!")

        elif command in ["뭐먹", "오늘뭐먹지"]:
            current_hour = datetime.now().hour
            is_yasik = current_hour >= 22 or current_hour <= 5
            is_dinner = not is_yasik or current_hour >= 17

            if is_yasik:
                target_food_list = self.yasik
            elif is_dinner:
                target_food_list = self.dinner
            else:
                target_food_list = self.lunch

            if len(target_food_list) == 0:
                food = "굶어라!"
            else:
                food = random.choice(target_food_list)

            await message.channel.send(food)
