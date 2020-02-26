from typing import List, Optional, Dict, Union
from enum import IntEnum


class ActType(IntEnum):
    """ 動作を選ぶ際のENUM """

    WAIT = 0
    MOVE_RIGHT = 1
    MOVE_BOTTOM_RIGHT = 2
    MOVE_UNDER = 3
    MOVE_BOTTOM_LEFT = 4
    MOVE_LEFT = 5
    MOVE_UPPER_LEFT = 6
    MOVE_UP = 7
    MOVE_UPPER_RIGHT = 8
    TILE_REMOVE = 9


class Agent:
    """ エージェントのクラス """

##### 初期化関連  ################################################################
    def __init__(self, name: str,
                 startX: int,
                 startY: int,
                 row: int,
                 columu: int):
        """ とりあえず初期化 """
        self.name = name  # エージェントの名前
        self.x: int = startX  # 配列上での場所(配列は0スタート)
        self.y: int = startY  # 配列上での場所(配列は0スタート)
        self.tile: tilePlaceType = \
            [[False for _ in range(row)] for i in range(columu)]  # タイルの配列
        self.tile[startY][startX] = True  # 初期位置にタイルを置く

##### property  #################################################################
    @property
    def tileCopy(self):
        """ タイルの配列のコピーを返す　"""

        return self.tile.copy()

##### 動作関連  #################################################################

    def act(self, actType: ActType, eTeam, partner):
        """ 動作させる関数"""

        rollX = self.x ; rollY = self.y  # 移動前のエージェントの座標(移動先が行けない場所だった場合、この座標に戻す)

        # 動作ごとに座標を更新
        if actType == ActType.WAIT:
            pass
        elif actType == ActType.MOVE_RIGHT:
            self.x += 1
        elif actType == ActType.MOVE_BOTTOM_RIGHT:
            self.x += 1 ; self.y += 1
        elif actType == ActType.MOVE_UNDER:
            self.y += 1
        elif actType == ActType.MOVE_BOTTOM_LEFT:
            self.x -= 1 ; self.y += 1
        elif actType == ActType.MOVE_LEFT:
            self.x -= 1
        elif actType == ActType.MOVE_UPPER_LEFT:
            self.x -= 1 ; self.y -= 1
        elif actType == ActType.MOVE_UP:
            self.y -= 1

        # 移動先が配列の範囲外なら座標を移動前に戻す
        if (self.x < 0 or self.y < 0) or (self.x >= len(self.tile[0])) or (self.y >= len(self.tile)):
            self.x = rollX ; self.y = rollY
            return

        # 移動先に相手チームの人がいるなら座標を移動前に戻す
        if ((self.x, self.y) == (eTeam[0].x, eTeam[0].y)) or ((self.x, self.y) == (eTeam[1].x, eTeam[1].y)):
            self.x = rollX ; self.y = rollY
            return

        # 移動先に自分チームの人(partner)がいるなら座標を移動前に戻す
        if (self.x, self.y) == (partner.x, partner.y):
            self.x = rollX ; self.y = rollY
            return

        # 移動先に相手チームのタイルがあるなら座標を移動前に戻す
        if (eTeam[0].tile[self.y][self.x]) or (eTeam[1].tile[self.y][self.x]):
            self.x = rollX ; self.y = rollY
            return

        self.tile[self.y][self.x] = True  # 問題なければ移動先にタイルをセットする

    def removeTile(self, eTeam, removeX: int, removeY: int):
        """タイルの削除"""

        # 削除先が配列の範囲外なら何もしない
        if (removeX < 0 or removeY < 0) or (removeX >= len(eTeam[0].tile[0])) or (removeY >= len(eTeam[0].tile)):
            return
        if (removeX < 0 or removeY < 0) or (removeX >= len(eTeam[1].tile[0])) or (removeY >= len(eTeam[1].tile)):
            return

        # 削除先に相手チームの人がいるなら何もしない
        if (removeX, removeY) == (eTeam[0].x, eTeam[0].y) or (removeX, removeY) == (eTeam[1].x, eTeam[1].y):
            return

        # 問題なければタイルを削除する
        eTeam[0].tile[removeY][removeX] = False ; eTeam[1].tile[removeY][removeX] = False


##### 型定義  ###################################################################
fieldType = List[List[int]]
tilePlaceType = List[List[bool]]
regionPlaceType = List[List[bool]]
teamType = List[Agent]
