from Playing import Playing, randomMakeField
from Agent import ActType
from game_Funcs import *


def main() :
    playing = Playing(**randomMakeField())
    maxTurn = playing.turnNumber

    print(f"""[ 巡ります CUIゲーム説明 ]

    [ コマンド ]
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
    \t強制終了: exit
    \tコマンド確認: help

    [ 初期設定 ]

    ターン数: {maxTurn}

    チームA:
    \t{playing.teamA[0].name} (x: {playing.teamA[0].x}, y: {playing.teamA[0].y})
    \t{playing.teamA[1].name} (x: {playing.teamA[1].x}, y: {playing.teamA[1].y})

    チームB:
    \t{playing.teamB[0].name} (x: {playing.teamB[0].x}, y: {playing.teamB[0].y})
    \t{playing.teamB[1].name} (x: {playing.teamB[1].x}, y: {playing.teamB[1].y})

    フィールド :
    [見かた] [ ポイント : タイルの所有権 ] 囲いが < > の場合はエージェントの位置を示す
    """)

    fieldWatch(playing)

    print("\n - - Let's play "+ ("- - "*20)+"\n")

    # ここからゲーム本番
    while playing.isPlayingGame() :
        nowTurn = maxTurn - playing.turnNumber + 1

        agentArr = \
        (playing.teamA+playing.teamB)[0::2]+\
        (playing.teamA+playing.teamB)[1::2]
        for agent in agentArr :

            # 入力させる
            while True :
                act = ""
                try :
                    act = input(f"{nowTurn} ) [ {agent.name} ]動作を入力 >> ")
                    if act == "help" :
                        print("""
                        [ コマンド ]
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
                        \t強制終了: exit
                        \tコマンド確認: help
                        """)
                        continue
                    elif act == "exit" :
                        return 0 # exit
                    else :
                        act = ActType( int(act) )
                except :
                    print("\n正しい値を入力してください\n")
                    continue
                break

            eTeam = playing.teamA if agent in playing.teamB else playing.teamB

            # 削除の場合
            if act == ActType.TILE_REMOVE :
                while True :
                    try :
                        rmActX = int( input(f"{nowTurn} ) [ {agent.name} ]削除マス X を入力 >> ") )
                        rmActY = int( input(f"{nowTurn} ) [ {agent.name} ]削除マス Y を入力 >> ") )
                        t1 = \
                        (rmActX < 0 or rmActY < 0) or \
                        (rmActX >= len(eTeam[0].tile[0])) or \
                        (rmActY >= len(eTeam[0].tile))
                        t2 = \
                        (rmActX < 0 or rmActY < 0) or \
                        (rmActX >= len(eTeam[1].tile[0])) or \
                        (rmActY >= len(eTeam[1].tile))
                        if t1 or t2 :
                            print("\n値の場所に相手のタイルはありません\n")
                            continue
                        playing.act(agent, act, eTeam, rmActX, rmActY)
                    except :
                        print("\n正しい値を入力してください\n")
                        continue
                    break
            # それ以外
            else :
                playing.act(agent, act, eTeam)

        print(f"""
        {nowTurn}/{maxTurn} ターン目

        チームA:
        \t{playing.teamA[0].name} (x: {playing.teamA[0].x}, y: {playing.teamA[0].y})
        \t{playing.teamA[1].name} (x: {playing.teamA[1].x}, y: {playing.teamA[1].y})

        チームB:
        \t{playing.teamB[0].name} (x: {playing.teamB[0].x}, y: {playing.teamB[0].y})
        \t{playing.teamB[1].name} (x: {playing.teamB[1].x}, y: {playing.teamB[1].y})
        """)
        fieldWatch(playing)
        playing.turnEnd()

    # 終了
    print(f"""
    [ バトル終了 ]

    [ スコア ]
    \tteamA: {playing.field.teamScore(playing.teamA)}点
    \tteamB: {playing.field.teamScore(playing.teamB)}点

    [ フィールド ]

    """)
    fieldWatch(playing)





if __name__ == "__main__" :
    main()
