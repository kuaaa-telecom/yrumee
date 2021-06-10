import discord
import random

from yrumee.modules import Module

class GachaCard:

    def __init__(self):
        self.number = 0
        self.season = ""
        self.rare = ""
        self.name = ""
        self.desc = ""
        self.imgurl = ""

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
        self.cardlist = {"EX":0, "SSR":0, "SR":0, "R":0}

class GachaUser:

    initpoint = 50

    def __init__(self):
        self.UID = 0
        self.name = ""
        self.level = 0
        self.chatcnt = 0
        self.pointexp = 0
        self.levelexp = 0
        self.point = self.initpoint
        self.cardcnt = 0
        self.cardlist = {}
        self.seasonlist = {}

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
    priority = {"EX": 1, "SSR": 2, "SR": 3, "R": 4}
    return priority[card.rare]


class GachaModule(Module):
    '''
    <쿠안 가챠>
    [.가챠 도움말] 가챠 관련 명령어 목록을 표시합니다. (알파 테스트)
    '''

    help_title = "<가챠를 돌려 동료를 모으고 최강의 쿠안 군단을 만들자 ~현실에서는 일반부원인 내가 디코에서는 지도교수?!~>"
    help_list = [("[.계정생성 [닉네임]]", "밤새도록 디코를 하다 트럭에 치였더니 전생한 이세계에서는 내가 쿠아 지도교수?!"),
                ("[.프로필]", "SSS급 지도교수님은 평범한 대학 라이프를 보내고 싶습니다!")
                ("[.포인트]", "제 보유 포인트가 너무 많아 여신님도 곤란한 모양인데요?"),
                ("[.쿠안들]", "우리 쿠안들이 너무 강한 나머지 세계정복도 가능할거 같습니다만."),
                ("[.쿠안 [카드이름]]", "어쩔 수 없네요, 여기서는 제 힘을 조금만 보여주는 수 밖에."),
                ("[.가챠 [타입] [횟수]]", "[타입] -> 일반, [횟수] -> 단챠/연챠(SR 이상 한 장 확정!)"),
                ("[.컬렉션]"), "이번 시즌에도 역시 제가 대활약이네요"]

    season1 = [(1, "EX", "하스 앞에서 낮잠자는 여름이", "여름이(귀엽다)", ""),
                (1, "SSR", "회장 김보경", "202101 KUAAA 회장", ""),
                (1, "SR", "연임하는 관측부장 김수인", "안해요......", ""),
                (1, "SR", "관측위성 서보성", "지금은 지구래요", ""),
                (1, "SR", "생일 스티커를 보고 경악하는 이유정", "이거 몇 개나 붙인거야ㅋㅋㅋㅋ", ""),
                (1, "R", "관측회 없는 관측부장 김수인", "않이 관측회가 없는데요", ""),
                (1, "R", "코드포스 치는 편집부장 최희원", "아니 레이팅 아....", ""),
                (1, "R", "마라탕 먹는 서보성", "마라탕(보성푸드, 맛있다)", ""),
                (1, "R", "체스하는 황덕근", "퀸한테 작별인사 하세요", "")]

    def __init__(self, storage_instance):
        self.GM = storage_instance.get('GM', [699428369808359574])
        self.cardDB = storage_instance.get('cardDB', set())
        self.EXCardDB = storage_instance.get('EXCardDB', set())
        self.SSRCardDB = storage_instance.get('SSRCardDB', set())
        self.SRCardDB = storage_instance.get('SRCardDB', set())
        self.RCardDB = storage_instance.get('RCardDB', set())
        self.users = storage_instance.get('users', {})
        self.cardCnt = storage_instance.get('cardCnt', 1)
        
        if len(self.cardDB) == 0:
            for infolist in self.season1:
                self.addCard(infolist)

    
    def userCardList(self, user: GachaUser):
        cardlist = []
        for card in self.cardDB:
            if user.cardlist[card.number]:
                cardlist.append((card, user.cardlist[card.number]))
        return cardlist
    
    def showCardList(self, title, desc, cardlist):
        embed = discord.Embed(title=title, description=desc, color=0x62c1cc)
        cardlist.sort(key = lambda x : rarePriority(x[0]))
        for card, cnt in cardlist:
            embed.add_field(name=card.rare, value=card.name + "X" + cnt, inline=True)
        return embed

    def showCard(self, card: GachaCard):
        embed = discord.Embed(title=card.name, description=card.rare, color=0x62c1cc)
        embed.set_footer(text=card.desc)
        return embed

    def selectRare(self, gacha_type: str):
        rnd = random.random()
        table = []
        if gacha_type == '일반':
            table = [0.9, 0.09, 0.009, 0.001]
        elif gacha_type == '고급':
            table = [0, 0.9, 0.09, 0.01]
        for i in range(4):
            rnd -= table[i]
            if rnd < 0:
                return i
        return None

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
            return None

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
                best_rare = 10000
                for i in range(9):
                    rare = self.selectRare(gacha_type)
                    gacha_result.append(self.selectCard(rare))
                    best_rare = max(best_rare, rare)
                if best_rare >= 4:
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
        to_level_up = 100 + 10 * (user.level - 1)
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
        embed = discord.Embed(title=user.name, description=user.name+"님의 프로필입니다!", color=0x62c1cc)
        embed.add_field(name="닉네임", value=user.name, inline=True)
        embed.add_field(name="채팅을 친 횟수", value=user.chatcnt, inline=True)
        embed.add_field(name="다음 츄르까지", value=user.pointexp, inline=True)
        embed.add_field(name="다음 레벨까지", value=user.levelexp, inline=True)
        embed.add_field(name="츄르", value=user.point, inline=True)
        embed.add_field(name="쿠안 수", value=len(user.cardlist), inline=True)
        embed.add_field(name="카드 수", value=user.cardcnt, inline=True)
        return embed

    def addCard(self, infolist):
        if infolist[1] == "EX":
            target_DB = self.EXCardDB
        elif infolist[1] == "SSR":
            target_DB = self.SSRCardDB
        elif infolist[1] == "SR":
            target_DB = self.SRCardDB
        elif infolist[1] == "R":
            target_DB = self.RCardDB
        else:
            return False

        self.cardDB.add((self.cardCnt, int(infolist[0]), infolist[1], infolist[2], infolist[3], infolist[4]))
        target_DB.add(self.cardDB[-1])
        self.cardCnt += 1
        return self.cardDB[-1]

    async def on_command(self, command: str, payload: str, message: discord.Message):
        
        '''카드 추가'''
        if command == "관리자" and message.author.id in self.GM:
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
                for helpname, helpdesc in self.help_list:
                    embed.add_field(name=helpname, value=helpdesc, inline=True)
                await message.channel.send("도움말 목록이에요!", embed=embed)
            #가챠 뽑는 로직: skeletonK
            else:
                if not self.users[message.author.id]:
                    await message.channel.send("계정 등록을 먼저 해 주세요!")
                
                payload_list = payload.split()

                if len(payload_list) == 2 and payload_list[0] in ['일반'] and payload_list[1] in ['단챠', '연챠']:
                    cost = self.gachaCost(payload_list[0], payload_list[1])

                    if self.users[message.author.id].point < cost:
                        await message.channel.send("포인트가 부족해요!")
                        return False
                    
                    self.users[message.author.id].point -= cost
                    cardlist = self.gachaProcess(payload_list[0], payload_list[1])

                    for card_number in cardlist:
                        self.users[message.author.id].cardlist[card_number] += 1
                        self.users[message.author.id].cardcnt += 1
                    
                    if len(cardlist) <= 0:
                        return False
                    
                    if len(cardlist) <= 1:
                        embed = self.showCard(cardlist[0])
                    else:
                        embed = self.showCardList("10연차 결과!", "", cardlist)
                    await message.channel.send("", embed)

                else:         
                    await message.channel.send("사용법: .가챠 [타입(일반)] [횟수(단챠, 연챠)]")
        
        elif command == "계정생성":
            if not payload:
                await message.channel.send("사용법: .계정생성 [닉네임]")
                return False
            if self.users[message.author.id]:
                await message.channel.send("이미 등록된 계정이에요!")
                return False
            self.users[message.author.id] = GachaUser(message.author.id, payload)
            await message.channel.send(payload + "님의 계정을 생성했어요!")

        elif command == "프로필":
            if not self.users[message.author.id]:
                await message.channel.send("계정 등록을 먼저 해 주세요!")
                return False
            embed = self.showUserInfo(self.users[message.author.id])
            await message.channel.send("", embed)

        elif command == "포인트":
            if not self.users[message.author.id]:
                await message.channel.send("계정 등록을 먼저 해 주세요!")
                return False
            await message.channel.send("잔여 포인트:" + self.users[message.author.id].point)

        elif command == "쿠안들":
            if not self.users[message.author.id]:
                await message.channel.send("계정 등록을 먼저 해 주세요!")
                return False
            cardlist = self.userCardList(self.users[message.author.id])
            await message.channel.send(self.showCardList(self.users[message.author.id].name, "보유한 쿠안 목록이에요!", cardlist))
        
        elif command == "쿠안":
            target_card = None

            for card in self.cardDB:
                if card.name == payload:
                    target_card = card
                    break
            if not target_card:
                message.channel.send("잘못된 카드 이름이에요!")
                return False
            
            if not self.users[message.author.id].cardlist[target_card.number]:
                message.channel.send("보유하지 않은 카드에요!")
                return False

            await message.channel.send(embed=self.showCard(target_card))
        
        elif command == "컬렉션":
            await message.channel.send("아직 만드는 중이에요!")

    async def on_message(self, message: discord.message):
        self.increaseChatcnt(self.users[message.author.id])