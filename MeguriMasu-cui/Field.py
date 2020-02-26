from Agent import *
import numpy as np
import sys
sys.setrecursionlimit(10000)


checked: List[List[bool]]  # チェックのための配列
preChecked = None  # 移動中に使うメモ配列
memoRegionMap = []  # 作成中のマップ


class Field:

##### 初期化関連  ################################################################
    def __init__(self, field: fieldType):
        self._field: fieldType = field  # フィールド(初期化必須)

##### property  ################################################################
    @property
    def fieldCopy(self) -> fieldType:
        """ スコアボードのコピーを返す　"""
        return self._field.copy()

    @property
    def row(self):
        """フィールドの列数を返す"""

        return len(self._field[0])

    @property
    def columu(self):
        """ フィールドの行数を返す """

        return len(self._field)

##### タイルに関する計算  ################################################################

    def teamTile(self, team: teamType) -> tilePlaceType:
        """ チームのタイルを合わせた配列を返す　チームのタイルの論理和 """

        return [max(t) for t in zip(team[0].tile, team[1].tile)]

    def teamRegion(self, team: teamType) -> regionPlaceType:
        """ タイルの配置を元に領域の場所を求める """

        global checked
        global memoRegionMap

        m: tilePlaceType = self.teamTile(team)  # タイルが置かれている場所の配列
        result: regionPlaceType = []  # 実際に返す確定した領域の配列
        checked = [[False for j in i] for i in m]
        memoRegionMap = [[False for j in i] for i in m]

        def innerRegion(m: tilePlaceType, x: int, y: int) -> bool:
            global preChecked
            global checked
            global memoRegionMap

            # return この場所の領域
            isOneTime = False

            # 今の場所をメモ
            if preChecked is None:
                preChecked = [[False for j in i] for i in m]
                isOneTime = True
            preChecked[y][x] = True

            # とりあえず絞る
            if not searchRegion(m, x, y):
                if isOneTime:
                    checked[y][x] = True
                    preChecked = None
                return False

            # 自分がチェック済ならそのまま
            if searchChecked(checked, x, y):
                if isOneTime:
                    checked[y][x] = True
                    preChecked = None
                return m[y][x]

            # 隣のマスがチェック済か?
            # 左
            left_checked = searchChecked(checked, x - 1, y) and (not searchTile(m, x - 1, y))
            if left_checked:
                if isOneTime:
                    checked[y][x] = True
                    preChecked = None
                return memoRegionMap[y][x - 1]
            # 右
            right_checked = searchChecked(checked, x + 1, y) and (not searchTile(m, x + 1, y))
            if right_checked:
                if isOneTime:
                    checked[y][x] = True
                    preChecked = None
                return memoRegionMap[y][x + 1]
            # 上
            up_checked = searchChecked(checked, x, y - 1) and (not searchTile(m, x, y - 1))
            if up_checked:
                if isOneTime:
                    checked[y][x] = True
                    preChecked = None
                return memoRegionMap[y - 1][x]
            # 下
            bot_checked = searchChecked(checked, x, y + 1) and (not searchTile(m, x, y + 1))
            if bot_checked:
                if isOneTime:
                    checked[y][x] = True
                    preChecked = None
                return memoRegionMap[y + 1][x]

            # 隣のマスで同じ処理
            left_ans = True
            right_ans = True
            top_ans = True
            bot_ans = True
            # 左
            if not (searchChecked(preChecked, x - 1, y) or searchTile(m, x - 1, y)):
                left_ans = innerRegion(m, x - 1, y)
            # 右
            if not (searchChecked(preChecked, x + 1, y) or searchTile(m, x + 1, y)):
                right_ans = innerRegion(m, x + 1, y)
            # 上
            if not (searchChecked(preChecked, x, y - 1) or searchTile(m, x, y - 1)):
                top_ans = innerRegion(m, x, y - 1)
            # 下
            if not (searchChecked(preChecked, x, y + 1) or searchTile(m, x, y + 1)):
                bot_ans = innerRegion(m, x, y + 1)

            all_ans = left_ans and right_ans and top_ans and bot_ans

            # 完全に囲まれているなら True
            if isOneTime:
                checked[y][x] = True
                preChecked = None
            return all_ans

        def searchTile(m: tilePlaceType, x: int, y: int) -> bool:
            if not ((0 <= y < len(m)) and (0 <= x < len(m[0]))):
                return False
            return m[y][x]

        def searchChecked(c, x: int, y: int) -> bool:
            """ チェック済みか """

            if not ((0 <= y < len(c)) and (0 <= x < len(c[0]))):
                return False
            return c[y][x]

        def searchRegion(m: tilePlaceType, x: int, y: int) -> bool:
            """ 領域の可能性のあるマス(上下左右の延長線上にタイルがない かつ 今の場所がタイルではないマス) """

            flag = True
            # とりあえずタイルなら
            if m[y][x]:
                return False
            # 右
            if flag:
                counter = x
                while counter < len(m[0]):
                    if m[y][counter]:  # もしタイルがあるなら
                        break
                    counter += 1
                if counter == len(m[0]):  # 端まで行った
                    flag = False
            # 左
            if flag:
                counter = x
                while counter >= 0:
                    if m[y][counter]:  # もしタイルがあるなら
                        break
                    counter -= 1
                if counter == -1:  # 端まで行った
                    flag = False
            # 下
            if flag:
                counter = y
                while counter < len(m):
                    if m[counter][x]:
                        break
                    counter += 1
                if counter == len(m):
                    flag = False
            # 上
            if flag:
                counter = y
                while counter >= 0:
                    if m[counter][x]:
                        break
                    counter -= 1
                if counter == -1:
                    flag = False
            return flag

        for y in range(len(m)):
            innner_result = []
            for x in range(len(m[y])):
                re = innerRegion(m, x, y)
                innner_result.append(re)
                memoRegionMap[y][x] = re
            result.append(innner_result)
        memoRegionMap = []

        return result

##### 得点計算  ################################################################

    def teamTilePoint(self, team: teamType) -> int:
        """ チームのタイルポイントを返す """

        point = 0
        teamTile = self.teamTile(team)
        for y in range(len(teamTile)):
            for x in range(len(teamTile[0])):
                if teamTile[y][x]:
                    point += self._field[y][x]

        return point

    def teamRegionPoint(self, team: teamType) -> int:
        """ チームの領域ポイントを返す"""

        point = 0
        teamRegion = self.teamRegion(team)
        for y in range(len(teamRegion)):
            for x in range(len(teamRegion[0])):
                if teamRegion[y][x]:
                    point += abs(self._field[y][x])

        return point

    def teamScore(self, team: teamType) -> int:
        """ チームの点数を返す (タイルポイント+領域ポイント)"""

        return self.teamTilePoint(team) + self.teamRegionPoint(team)
