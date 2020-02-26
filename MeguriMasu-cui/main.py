from Playing import Playing, randomMakeField
from Agent import ActType
from game_Funcs import *


def watchField(arr2D) :
    for i in arr2D :
        for j in i :
            print( f"{j}", end="\t" )
        print()
    print()

def watchTile(arr2D) :
    for i in arr2D :
        for j in i :
            if j :
                print("■", end=" ")
            else :
                print("□", end=" ")
        print()
    print()

# 基本的にこれで実行できる
# 結果は他の関数で参照
playing = Playing(**randomMakeField())

""" セットアップが正常か """
print( "############################################################" )

print( "フィールド\n" )
print( f"フィールド幅 列: {playing.field.row}\t行: {playing.field.columu}\n" )

watchField(playing.field.fieldCopy)
# FIXME: ランダムが+に偏っていない(PDF参照)


print( "\n初期スポーン位置\n" )
print( f"name(teamA_0): {playing.teamA[0].name}" )
watchTile(playing.teamA[0].tileCopy)
print()
print( f"name(teamA_1): {playing.teamA[1].name}" )
watchTile(playing.teamA[1].tileCopy)
print()
print( f"name(teamB_0): {playing.teamB[0].name}" )
watchTile(playing.teamB[0].tileCopy)
print()
print( f"name(teamB_1): {playing.teamB[1].name}" )
watchTile(playing.teamB[1].tileCopy)

print()
print( f"ターン数: {playing.turnNumber}" )

print( "\n############################################################\n" )


while playing.isPlayingGame():
##### ターン数が0になるまで繰り返す ###################################################################

    for agent in (playing.teamA + playing.teamB)[0::2] + (playing.teamA + playing.teamB)[1::2]:
    ##### agentひとりひとりのactを呼び出す  ###################################################################
        print("""[動作一覧]
        \t何もしない: 0
        \t動く(右): 1
        \t動く(右下): 2
        \t動く(下): 3
        \t動く(左下): 4
        \t動く(左): 5
        \t動く(左上): 6
        \t動く(上): 7
        \t動く(右上): 8
        \t削除: 9
        """)
        print("今の位置")
        watchTile(agent.tileCopy)
        act = ActType(int(input(f"(入力){agent.name}の動作: ")))  # agentにさせたい動作
        team = playing.teamA if agent in playing.teamB else playing.teamB  # 相手のチーム (動作の時とタイル除去のときに必要)

        if act == ActType.TILE_REMOVE:
        ##### 動作がタイル除去の場合  ###################################################################

            removeX = int(input("(入力)タイルのｘ座標: ")) ; removeY = int(input("(入力)タイルのｘ座標: ")) #除去したいタイルの座標

            playing.act(agent, act, team, removeX, removeY)
        else:
        ##### それ以外の場合  ###################################################################

            playing.act(agent, act, team)

    print(lightStateLogOfJSON(playing))
    playing.turnNumber -= 1

    # watchTile(playing.field.teamTile(playing.teamA))  # チームAのタイルの表示
    # watchTile(playing.field.teamTile(playing.teamB))  # チームBのタイルの表示
    # print(playing.field.teamTilePoint(playing.teamA)) #チームAのタイルポイント
    # print(playing.field.teamTilePoint(playing.teamB)) #チームBのタイルポイント
    # watchTile(playing.field.teamRegion(playing.teamA))  # チームAの領域の表示
    # watchTile(playing.field.teamRegion(playing.teamB))  # チームBの領域の表示
