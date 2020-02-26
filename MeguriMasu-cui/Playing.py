from Agent import Agent, ActType, List, Optional, Dict, Union, fieldType, tilePlaceType, regionPlaceType, teamType
from Field import Field
import random


class Playing:

##### 初期化関連  ################################################################
    def __init__(self, fieldSet: fieldType,
                 setStartX: int,
                 setStartY: int,
                 turn: int
                 ):
        self.field = Field(fieldSet) ; row = self.field.row ; columu = self.field.columu
        self.teamA: teamType = [Agent("agentA", setStartX, setStartY, row, columu), Agent("agentB", (row-1-setStartX), (columu-1-setStartY), row, columu)]  # チームAのエージェントリスト
        self.teamB: teamType = [Agent("agentC", setStartX, (columu-1-setStartY), row, columu), Agent("agentD", (row-1-setStartX), setStartY, row, columu)]  # チームBのエージェントリスト
        self.turnNumber = turn  # ターン数
        self.log = []  # とりあえずログ、型は要相談

##### 動作関連  #################################################################

    def act(self,
            agent,
            actType: ActType,
            eTeam: teamType = None,
            removeX: Optional[ int ] = None,
            removeY: Optional[ int ] = None
            ):
        """一体ずつactまたはremoveTileを実行"""

        mTeam = self.teamA if agent in self.teamA else self.teamB  # このエージェントの所属している自分のチーム
        partner = list(filter(lambda x: x.name != agent.name, mTeam))[0]  # 自分のチームのもう一人のエージェント（相方)

        if actType == ActType.TILE_REMOVE and removeX and removeY:
            agent.removeTile(eTeam, removeX, removeY)
        else:
            agent.act(actType, eTeam, partner)

        # ログをとる
        teamStr = ""
        if id(eTeam) == id(self.teamA) :
            teamStr = "teamA"
        elif id(eTeam) == id(self.teamB) :
            teamStr = "teamB"
        else :
            teamStr = "undefined"
        self.log.append({
            "remaining_turn": self.turnNumber,
            "agent_name": agent.name,
            "agent_team": teamStr,
            "x": agent.x,
            "y": agent.y,
            "removeX": removeX,
            "removeY": removeY
        })

###### 終了判定  ##########################################################################

    def isPlayingGame(self) -> bool:
        """ ゲームが終わっていないかの判定 """

        if self.turnNumber > 0:
            return True  # 終わっていないならTrue
        else:
            return False  # 終わったならFalse
###### ターン終了宣言  ##########################################################################
    def turnEnd(self) :
        self.turnNumber -= 1

###### Playingクラスの初期値を生成  ##########################################################################

def randomMakeField() -> Dict[str, Union[ int, fieldType, teamType ]] :
    """ gameStartの引数を生成するためのDictを生成 """

    turnSet = 120 - (10 * random.randint(0, 6))  # ターン数 60~120 10飛ばし
    row = random.randint(6, 12) ; columu = random.randint(6, 12)  # 行(6~12)と列(6~12)
    fieldSet = [[int(random.triangular(-16, 16, 8)) for j in range(row)] for i in range(columu)]  # スコアボード
    startX = 1; startY = 1  # エージェントA(左上)の初期位置　*対称なので左上さえ決まればほかのも自動的に決まる

    d = {"fieldSet": fieldSet, "setStartX": startX, "setStartY": startY, "turn": turnSet}

    return d
