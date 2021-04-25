import random
import discord

from yrumee.modules import Module


class TeraformingModule(Module):
    """
[.테포마] 여름이가 추천하는 테포마 세팅을 출력합니다.
    """

    def __init__(self, storage_instance):
        self.expansion_list = storage_instance.get('expansion_list', ["비너스", "서곡", "개척기지", "격동"])
        self.map_list = sotrage_instance.get('map_list', ["타르시스", "헬라스", "엘리시움"])

    async def on_command(self, command: str, payload: str, message: discord.Message):
        if command == "테포마":
            expansion_num = random.randint(0, 4)
            expansion = ""
            if expansion_num == 0:
                expansion = "기본"
            else:
                expansion = sorted(random.sample(range(4), expansion_num)
                expansion = " ".join([expansion_list[x] for x in expansion])

            map_num = random.randint(0, 2)
            map_num = map_list[map_num]

            await message.channel.send("여름이의 확장팩 추천: {}".format(expansion))
            await message.channel.send("여름이의 맵 추천: {}".format(map_num))
