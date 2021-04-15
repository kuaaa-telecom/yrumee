import discord

from yrumee.modules import Module


class MBTIQuizModule(Module):
    """
[.mbtiquiz] [.mbti퀴즈] 이 도움말을 출력합니다.
[.mbtiquiz 시작] 새로운 MBTI 퀴즈를 시작합니다.
[.mbtiquiz 랭킹] MBTI 퀴즈의 현재 점수 / 랭킹을 출력합니다.
[.mbtiquiz 채점] [.채점] MBTI 퀴즈를 채점합니다. 이 기능은 MBTI 퀴즈가 시작되었을 때만 동작합니다.
[MBTI-퀴즈!]
채팅 내역의 일부를 읽은 후, 채팅을 한 사람들의 MBTI를 맞춰보는 퀴즈입니다.
새로운 퀴즈를 시작하면, 채팅은 다음과 같이 주어집니다.

```
[A] 오늘 집가면 고양이 있겠다
[B] 나만 고양이 없어... ㅠㅠ
[A] 고양이 좋아
[C] 나두나두
[B] 고양이 키우고 싶다
```

- 대화는 2명 이상 4명 이하가 참여한, 5줄 이상 15줄 이하 중 랜덤하게 주어집니다.
- 대화내역의 사람들은 모두 알파벳(익명)으로 표시됩니다.
- 각각의 알파벳의 MBTI를 맞춘 후, 퀴즈를 출제한 사람이 채점 명령을 입력하면 여름이가 채점을 합니다.
- MBTI의 각 알파벳 중 하나를 맞추는 경우 25점이 부여되고, 모두 맞춘 경우에는 총 100점이 부여됩니다.
- 대화내역 중 `채팅 내역 수집 동의`를 하지 않은 사람의 대화는 포함되지 않습니다.
- 여름이 또는 소라쿠다가 중간에 껴있는 대화는 포함되지 않습니다.
    """

    def __init__(self, storage_instance):
        self.rank = storage_instance.get('mbti_quiz_rank', {})

    async def on_command(self, command: str, payload: str, message: discord.Message):

        if command.lower() == "mbtiquiz":
            await message.channel.send("[MBTI-퀴즈] 아직 만들고 있어요!")
        elif command.lower() == "채점":
            await message.channel.send("[MBTI-퀴즈] 아직 만들고 있어요!")
