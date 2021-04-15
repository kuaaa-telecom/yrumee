from collections import defaultdict

import discord
import random

from khaiii import KhaiiiApi
from yrumee.modules import Module


class SoraModule(Module):

    contents = [
        "그걸 말이라고 하냥!?",
        "당연하다냥!",
        "안 된다냥..",
        "언젠가는 될 거다냥!",
        "다시 한번 물어봐냥!",
        "된다냥!",
    ]

    predefined_content = {
        "당첨": ["그럴 수도 있을 것 같다냥!", "그게 된다고 생각하냥?"],
        "먹다": ["그래도 되긴 하지만... 살이 찌지 않을까냥?", "맛있겠다냥!!!ㅜ"],
        "맛있": ["맛있겠다냥!!!ㅜ", "난 싫다냥!", "그건 좋다냥!"],
        "하다": ["괜찮다냥!"],
        "사다": ["돈이 없다냥!"],
        "호불호": ["좋다냥!", "싫다냥!", "완전 좋다냥!!", "완전 싫다냥!!!"],
    }

    required_morph_types = "NVMJEXS"

    tags = [
        (
            "가",
            "VV",
            "가다",
        ),
        (
            "싶",
            "VX",
            "싶다",
        ),
        (
            "먹",
            "VV",
            "먹다",
        ),
        (
            "당첨",
            "NNG",
            "당첨",
        ),
        (
            "쫒",
            "NNG",
            "당첨",
        ),
        (
            "하",
            "VX",
            "하다",
        ),
        (
            "사",
            "NNG",
            "사다",
        ),
        (
            "맛있",
            "VA",
            "맛있다",
        ),
        (
            "좋아",
            "IC",
            "호불호",
        ),
        (
            "좋아하",
            "VV",
            "호불호",
        ),
        (
            "싫어",
            "IC",
            "호불호",
        ),
        (
            "싫어하",
            "VV",
            "호불호",
        )
    ]

    api = KhaiiiApi()

    @classmethod
    def if_match_tag(cls, morph):
        for tag in cls.tags:
            if morph.lex == tag[0] and morph.tag == tag[1]:
                return tag
        return None

    async def on_message(self, message: discord.Message) -> bool:

        if message.content.startswith("여름아") and message.content.endswith("?"):
            ss = self.api.analyze(message.content.lstrip("여름아"))
            contexts = [
                # (required_morph_type, '가다'),
            ]

            for required_morph_type in self.required_morph_types:
                for s in ss:
                    for morph in s.morphs:
                        match = self.if_match_tag(morph)
                        if match is None:
                            continue
                        lex, tag, match = match
                        if match and required_morph_type in tag:
                            contexts.append(
                                (
                                    required_morph_type,
                                    match,
                                )
                            )
                            break

            print((message.content, ' '.join([str(s) for s in ss]), contexts))

            choices = [c[1] for c in contexts]
            key = random.choice(choices) if len(choices) > 0 else ''
            content = random.choice(
                self.predefined_content.get(key, self.contents)
            )
            await message.channel.send("<@{}> {}".format(message.author.id, content))

        return False
