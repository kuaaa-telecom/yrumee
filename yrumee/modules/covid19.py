import aiohttp
import discord

from config import config
from yrumee.modules import Module


class COVID19Module(Module):
    """
[.코로나] [.코로나19] [.covid] 대한민국의 코로나19 현황을 출력합니다. 이 기능은 실시간성이 보장되지 않습니다.
    """
    session = None

    async def on_command(self, command: str, payload: str, message: discord.Message):

        if not self.session:
            self.session = aiohttp.ClientSession()

        if command.lower() in ["코로나", "코로나19", "covid"]:
            total_response = await self.session.get(
                "https://api.corona-19.kr/korea/?serviceKey={}".format(
                    config.covid19_api_token
                )
            )
            today_response = await self.session.get(
                "https://api.corona-19.kr/korea/country/new/?serviceKey={}".format(
                    config.covid19_api_token
                )
            )

            total_json = await total_response.json()
            today_json = await today_response.json()

            if total_json["resultCode"] != "0" or today_json["resultCode"] != "0":
                return False
            else:
                result_message = """[국내 코로나19 발생 현황] 🏥
총 확진자 수: {total_case}
총 완치자 수: {total_recovered}
총 사망자 수: {total_death}

오늘 신규 확진자 수: {today_total_case} (해외 유입: {today_total_case_f}, 지역 발생: {today_total_case_c})
""".format(
                    total_case=total_json["TotalCase"],
                    total_recovered=total_json["TotalRecovered"],
                    total_death=total_json["TotalDeath"],
                    today_total_case=today_json["korea"]["newCase"],
                    today_total_case_f=today_json["korea"]["newFcase"],
                    today_total_case_c=today_json["korea"]["newCcase"],
                )

            await message.channel.send(result_message)
            return True
