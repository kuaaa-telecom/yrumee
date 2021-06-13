import random
import re

import discord

from yrumee.modules import Module, gacha_db


class GachaCard:

    def __init__(self, number, season, rare, name, desc, imgurl):
        self.number = number
        self.season = season
        self.rare = rare
        self.name = name
        self.desc = desc
        self.imgurl = imgurl

class GachaSeason:

    def __init__(self):
        self.number = 0
        self.name = ""
        self.totalcards = 0
        self.cardlist = {"EX[:star::star::star::star:]":0, "SSR[:star::star::star:]":0, "SR[:star::star:]":0, "R[:star:]":0}

class GachaUser:

    initpoint = 50

    def __init__(self, UID, name):
        self.UID = UID
        self.name = name
        self.level = 0
        self.chatcnt = 0
        self.pointexp = 0
        self.levelexp = 0
        self.point = self.initpoint
        self.cardcnt = 0
        self.cardlist = {}
        self.seasonlist = {}

def rarePriority(card: GachaCard):
    priority = {"EX[:star::star::star::star:]": 1, "SSR[:star::star::star:]": 2, "SR[:star::star:]": 3, "R[:star:]": 4}
    return priority[card.rare]

class GachaModule(Module):
    '''
    [.가챠 도움말] 가챠 관련 명령어 목록을 표시합니다. (알파 테스트)
    '''

    help_title = "<가챠를 돌려 동료를 모으고 최강의 쿠안 군단을 만들자 ~현실에서는 일반부원인 내가 디코에서는 지도교수?!~>"
    help_list = [("[.계정생성 [닉네임]]", "밤새도록 디코를 하다 트럭에 치였더니 전생한 이세계에서는 내가 쿠아 지도교수?!"),
                ("[.프로필]", "SSS급 지도교수님은 평범한 대학 라이프를 보내고 싶습니다!"),
                ("[.포인트]", "제 보유 포인트가 너무 많아 여신님도 곤란한 모양인데요?"),
                ("[.쿠안들]", "우리 쿠안들이 너무 강한 나머지 세계정복도 가능할거 같습니다만."),
                ("[.쿠안 [카드이름]]", "어쩔 수 없네요, 여기서는 제 힘을 조금만 보여주는 수 밖에."),
                ("[.가챠 [타입] [횟수]]", "[타입] -> 일반, [횟수] -> 단챠/연챠(SR 이상 한 장 확정!)"),
                ("[.컬렉션]", "이번 시즌에도 역시 제가 대활약이네요")]

    def __init__(self, storage_instance):
        self.GM = storage_instance.get('GM', [699428369808359574])
        self.cardDB = storage_instance.get('cardDB', set())
        self.EXCardDB = storage_instance.get('EXCardDB', set())
        self.SSRCardDB = storage_instance.get('SSRCardDB', set())
        self.SRCardDB = storage_instance.get('SRCardDB', set())
        self.RCardDB = storage_instance.get('RCardDB', set())
        self.users = storage_instance.get('users', {})

        if len(self.cardDB) == 0:
            for infolist in gacha_db.season1:
                self.addCard(infolist)

    def userCardList(self, user: GachaUser):
        cardlist = []
        for card in self.cardDB:
            if card.number in user.cardlist:
                cardlist.append((card, user.cardlist[card.number]))
        return cardlist

    def showCardList(self, title, desc, cardlist, user=None):
        embed = discord.Embed(title=title, description=desc, color=0x62c1cc)
        if user:
            for card, cnt in cardlist:
                embed.add_field(name=card.rare, value=card.name + "X" + str(cnt), inline=False)
        else:
            for card in cardlist:
                embed.add_field(name=card.rare, value=card.name, inline=False)
        return embed

    def showCard(self, card: GachaCard):
        embed = discord.Embed(title=card.name, description=card.rare, color=0x62c1cc)
        embed.set_footer(text=card.desc)
        imgurl = card.imgurl
        if imgurl == "":
            imgurl = gacha_db.default_img[rarePriority(card)]
        if imgurl != "":
            embed.set_image(url=imgurl)
        return embed

    def selectRare(self, gacha_type: str):
        rnd = random.random()
        table = []
        if gacha_type == '일반':
            table = [0.9, 0.09, 0.009, 0.001]
        elif gacha_type == '고급':
            table = [0, 0.9, 0.09, 0.01]
        else:
            raise ValueError('invalid gacha_type {}'.format(gacha_type))

        for i in range(4):
            rnd -= table[3 - i]
            if rnd < 0:
                return i + 1
        return 0

    def selectCard(self, rare: int):
        if rare == 4:
            return random.choice(list(self.RCardDB))
        elif rare == 3:
            return random.choice(list(self.SRCardDB))
        elif rare == 2:
            return random.choice(list(self.SSRCardDB))
        elif rare == 1:
            return random.choice(list(self.EXCardDB))
        else:
            raise ValueError('invalid rare value')

    def gachaCost(self, gacha_type: str, gacha_cnt: str):
        normal_cost = 5
        special_cost = 50
        single_cost = normal_cost if gacha_type == '일반' else special_cost
        cost = (1 if gacha_cnt == '단챠' else 10) * single_cost
        return cost

    def gachaProcess(self, gacha_type: str, gacha_cnt: str):
        gacha_result = []

        if gacha_cnt == '단챠':
            rare = self.selectRare(gacha_type)
            gacha_result.append(self.selectCard(rare))

        else:

            if gacha_type == '일반':
                best_rare = 100000
                for i in range(9):
                    rare = self.selectRare(gacha_type)
                    gacha_result.append(self.selectCard(rare))
                    best_rare = max(best_rare, rare)
                if best_rare > 4:
                    rare = self.selectRare('고급')
                    gacha_result.append(self.selectCard(rare))
                else:
                    rare = self.selectRare('일반')
                    gacha_result.append(self.selectCard(rare))

            elif gacha_type == '고급':
                for i in range(10):
                    rare = self.selectRare(gacha_type)
                    gacha_result.append(self.selectCard(rare))

        return gacha_result

    def increaseChatcnt(self, user: GachaUser):
        to_level_up = 100 + 10 * (user.level)
        to_point = 3

        user.chatcnt += 1
        user.pointexp += 1
        user.levelexp += 1

        if user.pointexp >= to_point:
            user.point += 1
            user.pointexp = 0
        if user.levelexp >= to_level_up:
            user.level += 1
            user.levelexp = 0

    def showUserInfo(self, user: GachaUser):
        to_level_up = 100 + 10 * (user.level)
        to_point = 3

        embed = discord.Embed(title=":star:"+user.name, description=user.name+" 님의 프로필입니다!", color=0x62c1cc)
        embed.add_field(name="닉네임", value=user.name + " (lv." + str(user.level) + ")", inline=False)
        embed.add_field(name="채팅을 친 횟수", value=user.chatcnt, inline=True)
        embed.add_field(name="다음 츄르까지", value=to_point-user.pointexp, inline=True)
        embed.add_field(name="다음 레벨까지", value=to_level_up-user.levelexp, inline=True)
        embed.add_field(name="츄르", value=user.point, inline=True)
        embed.add_field(name="쿠안 수", value=len(user.cardlist), inline=True)
        embed.add_field(name="카드 수", value=user.cardcnt, inline=True)

        return embed

    def addCard(self, infolist):
        if infolist[2] == "EX[:star::star::star::star:]":
            target_DB = self.EXCardDB
        elif infolist[2] == "SSR[:star::star::star:]":
            target_DB = self.SSRCardDB
        elif infolist[2] == "SR[:star::star:]":
            target_DB = self.SRCardDB
        elif infolist[2] == "R[:star:]":
            target_DB = self.RCardDB
        else:
            return False

        tempCard = GachaCard(int(infolist[0]), int(infolist[1]), infolist[2], infolist[3], infolist[4], infolist[5])

        self.cardDB.add(tempCard)
        target_DB.add(tempCard)
        return tempCard

    async def on_command(self, command: str, payload: str, message: discord.Message):

        '''카드 추가'''
        # Cannot access member "id" for type "Member" Member "id" is unknown때문에 밖으로 빼둠
        author_id = message.author.id

        if command == "관리자" and author_id in self.GM:

            await message.channel.send("아직 만드는 중이에요!")
            return False

            payload_list = payload.split('/')

            if len(payload_list) != 5:
                await message.channel.send("다시 입력해주세요.")
                return False

            card = self.addCard(payload_list)

            if card:
                await message.channel.send("등록 완료!", embed=self.showCard(card))
            else:
                await message.channel.send("다시 입력해주세요.")

        elif command == "가챠":
            if payload == "도움말":
                embed = discord.Embed(title=self.help_title, color=0x62c1cc)
                for helpdoc in self.help_list:
                    embed.add_field(name=helpdoc[0], value=helpdoc[1], inline=False)
                await message.channel.send("도움말 목록이에요!", embed=embed)
            #가챠 뽑는 로직: skeletonK
            else:
                if not author_id in self.users:
                    await message.channel.send("계정 등록을 먼저 해 주세요!")
                    return False

                payload_list = payload.split()

                if len(payload_list) == 2 and payload_list[0] in ['일반'] and payload_list[1] in ['단챠', '연챠']:
                    cost = self.gachaCost(payload_list[0], payload_list[1])

                    if self.users[author_id].point < cost:
                        await message.channel.send("츄르가 부족해요!")
                        return False

                    self.users[author_id].point -= cost
                    try:
                        cardlist = self.gachaProcess(payload_list[0], payload_list[1])
                    except ValueError as e:
                        print(e)
                        await message.channel.send(".가챠: 오류가 발생하였습니다.")
                    else:
                        for card in cardlist:
                            card_number = card.number
                            if not card_number in self.users[author_id].cardlist:
                                self.users[author_id].cardlist[card_number] = 1
                            else:
                                self.users[author_id].cardlist[card_number] = self.users[author_id].cardlist[card_number] + 1
                            self.users[author_id].cardcnt += 1

                        if len(cardlist) <= 0:
                            return False

                        if len(cardlist) <= 1:
                            embed = self.showCard(cardlist[0])
                        else:
                            embed = self.showCardList("10연차 결과!", "", cardlist)
                        await message.channel.send(embed=embed)
                else:
                    await message.channel.send("사용법: .가챠 [타입(일반)] [횟수(단챠, 연챠)]")

        elif command == "계정생성":
            if not payload:
                await message.channel.send("닉네임을 입력해주세요!")
                return False
            if author_id in self.users:
                await message.channel.send("이미 등록된 계정이에요!")
                return False
            if message.mentions or message.mention_everyone:
                await message.channel.send("건우선배 멈춰")
                return False

            p = re.compile(r'^(\w|[가-힣])+$')

            if not p.match(payload):
                await message.channel.send("닉네임에는 한글, 영어, 숫자, 그리고 언더바만 사용할 수 있어요!")
                return False

            if len(self.users) > 0:
                for user in self.users.values():
                    if user.name == payload:
                        await message.channel.send("중복된 닉네임이에요!")
                        return False

            self.users[author_id] = GachaUser(author_id, message.author.display_name)

            if author_id in self.GM:
                self.users[author_id].point = 99999999999

            await message.channel.send("{}님의 계정을 생성했어요!".format(message.author.display_name))

        elif command == "프로필":
            if not author_id in self.users:
                await message.channel.send("계정 등록을 먼저 해 주세요!")
                return False
            embed = self.showUserInfo(self.users[author_id])
            await message.channel.send(embed=embed)

        elif command == "포인트":
            if not author_id in self.users:
                await message.channel.send("계정 등록을 먼저 해 주세요!")
                return False
            await message.channel.send("잔여 츄르: {}".format(str(self.users[author_id].point)))

        elif command == "쿠안들":
            if not author_id in self.users:
                await message.channel.send("계정 등록을 먼저 해 주세요!")
                return False
            cardlist = self.userCardList(self.users[author_id])
            await message.channel.send(embed=self.showCardList(self.users[author_id].name, "보유한 쿠안 목록이에요!", cardlist, user=self.users[author_id]))

        elif command == "쿠안":
            target_card = None

            await message.channel.send("아직 만드는 중이에요!")
            return False

            for card in self.cardDB:
                if card.name == payload:
                    target_card = card
                    break
            if not target_card:
                await message.channel.send("잘못된 카드 이름이에요!")
                return False

            if author_id not in self.users.cardlist[target_card.number]:
                await message.channel.send("보유하지 않은 카드에요!")
                return False

            await message.channel.send(embed=self.showCard(target_card))

        elif command == "컬렉션":
            await message.channel.send("아직 만드는 중이에요!")

    async def on_message(self, message: discord.Message):
        author_id = message.author.id
        if author_id in self.users:
            self.increaseChatcnt(self.users[author_id])
