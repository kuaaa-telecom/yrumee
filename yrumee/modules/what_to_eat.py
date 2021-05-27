import random
from datetime import datetime

import discord

from yrumee.modules import Module


class WhatToEatModule(Module):
    """
    [.다이어트] 다이어트 중인 사람 목록에 자신을 추가합니다.
    [.요요] 다이어트 중인 사람 목록에서 자신을 제거합니다.

    [.아침] 아침에 먹을만한 식사의 종류 혹은 밥집을 추가합니다.
    [.점심] 점심에 먹을만한 식사의 종류 혹은 밥집을 추가합니다.
    [.저녁] 저녁에 먹을만한 식사의 종류 혹은 밥집을 추가합니다.
    [.야식] 야식으로 먹을만한 식사의 종류 혹은 밥집을 추가합니다.
    [.오늘뭐먹지] [.뭐먹] 오늘 뭐를 먹을지 여름이에게 물어봅니다.
    [.뱃속] 들어있는 음식 리스트를 반환합니다.
    """

    def __init__(self, storage_instance):
        self.breakfast = storage_instance.get("breakfast", set())
        self.lunch = storage_instance.get("lunch", set())
        self.dinner = storage_instance.get("dinner", set())
        self.yasik = storage_instance.get("yasik", set())
        self.diet = storage_instance.get("diet", {"브로콜리", "닭가슴살", "굶어라냥!"})
        self.on_diet = storage_instance.get("on_diet", set())

    async def on_command(self, command: str, payload: str, message: discord.Message):

        if command in ["아침", "점심", "저녁", "야식"]:
            if not payload:
                await message.channel.send("사용법: .{0} {0}에-먹을만한-음식".format(command))
            else:
                if command == "아침":
                    target_food_list = self.breakfast
                elif command == "점심":
                    target_food_list = self.lunch
                elif command == "저녁":
                    target_food_list = self.dinner
                elif command == "야식":
                    target_food_list = self.yasik
                else:
                    target_food_list = set()

                target_food_list.add(payload)

                await message.channel.send("등록 완료!")

        elif command in ["뭐먹", "오늘뭐먹지"]:
            who = message.author.display_name.split("_")[0]
            current_hour = datetime.now().hour

            is_breakfast = 5 <= current_hour and current_hour < 11
            is_lunch = 11 <= current_hour and current_hour < 17
            is_dinner = 17 <= current_hour and current_hour < 22

            if who in self.on_diet:
                target_food_list = self.diet
            elif is_breakfast:
                target_food_list = self.breakfast
            elif is_lunch:
                target_food_list = self.lunch
            elif is_dinner:
                target_food_list = self.dinner
            else:
                target_food_list = self.yasik

            if len(target_food_list) == 0:
                food = "굶어라냥!"
            else:
                food = random.choice(list(target_food_list))

            await message.channel.send(food)

            if len(target_food_list) > 50:
                target_food_list.remove(food)

        elif command == "다이어트":
            self.on_diet.add(message.author.display_name.split("_")[0])
            await message.channel.send("등록 완료!")

        elif command == "요요":
            self.on_diet.discard(message.author.display_name.split("_")[0])
            await message.channel.send("해제 완료!")
        
        elif command == "뱃속":
            payload = f"아침: {self.breakfast}\n점심: {self.lunch}\n저녁: {self.dinner}\n야식: {self.yasik}\n다이어트: {self.diet}"
            chunks = [payload[i:i+1000] for i in range(0, len(payload), 1000)]
            for chunk in chunks:
                await message.channel.send(chunk)

