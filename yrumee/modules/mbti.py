import json

import discord

from yrumee.ext.pyjosa import replace_josa
from yrumee.modules import Module


class MBTIModule(Module):
    mbti = {}

    @classmethod
    def is_mbti_format(cls, payload):
        mbti_payload = payload.upper()
        return (
            mbti_payload[0] in ["I", "E"]
            and mbti_payload[1] in ["S", "N"]
            and mbti_payload[2] in ["T", "F"]
            and mbti_payload[3] in ["J", "P"]
        )

    async def on_command(self, command: str, payload: str, message: discord.Message):
        if self.is_mbti_format(command):
            mbti_type = command.upper()
            await message.channel.send(
                "[MBTI] \n{}인 사람: {}".format(
                    mbti_type,
                    ", ".join([k for k, v in self.mbti.items() if v == mbti_type]),
                )
            )
        elif command.lower() == "mbti":
            register_mode = False
            if len(payload) == 4 and self.is_mbti_format(payload):
                register_mode = True

            if not payload:
                await message.channel.send(
                    "[MBTI] \n1. 자신의 MBTI 등록하기 `.mbti ESFJ`\n2. 다른 사람의 MBTI 확인하기 `.mbti 표대현`"
                )
            elif register_mode:
                self.mbti[message.author.display_name.split("_")[0]] = payload.upper()
                await message.channel.send("[MBTI] 등록 완료!")
            else:
                who = payload.split("_")[0]
                mbti = self.mbti.get(who)
                if mbti:
                    await message.channel.send("{}님의 MBTI는 {}입니다.".format(who, mbti))
                else:
                    await message.channel.send("{}님은 등록되지 않은 사람입니다.".format(who))

        elif command.lower() == "mbti_json":
            await message.channel.send("```{}```".format(json.dumps(self.mbti)))

        elif command.lower() == "mbti_load_json":
            try:
                self.mbti = json.loads(payload)
            except:
                pass
