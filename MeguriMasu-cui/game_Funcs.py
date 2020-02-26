from Playing import Playing, randomMakeField
from Agent import ActType
import json

################################################################################
def stateLogOfJSON(play: Playing) -> str:
    # 連想配列の作成
    d = {
        "field": play.field.fieldCopy,
        "remaining_turn": play.turnNumber,
        "teamA": {
            "member" : [
                {
                    "name": play.teamA[0].name,
                    "x": play.teamA[0].x,
                    "y": play.teamA[0].y,
                    "tile": play.teamA[0].tileCopy,
                },
                {
                    "name": play.teamA[1].name,
                    "x": play.teamA[1].x,
                    "y": play.teamA[1].y,
                    "tile": play.teamA[1].tileCopy
                }
            ],
            "tile": play.field.teamTile(play.teamA),
            "region": play.field.teamRegion(play.teamA),
            "onlyTileScore": play.field.teamTilePoint(play.teamA),
            "onlyRegionScore": play.field.teamRegionPoint(play.teamA),
            "Score": play.field.teamScore(play.teamA)
        },
        "teamB": {
            "member": [
                {
                    "name": play.teamB[0].name,
                    "x": play.teamB[0].x,
                    "y": play.teamB[0].y,
                    "tile": play.teamB[0].tileCopy
                },
                {
                    "name": play.teamB[1].name,
                    "x": play.teamB[1].x,
                    "y": play.teamB[1].y,
                    "tile": play.teamB[1].tileCopy
                }
            ],
            "tile": play.field.teamTile(play.teamB),
            "region": play.field.teamRegion(play.teamB),
            "onlyTileScore": play.field.teamTilePoint(play.teamB),
            "onlyRegionScore": play.field.teamRegionPoint(play.teamB),
            "Score": play.field.teamScore(play.teamB)
        }
    }
    return json.dumps(d)
################################################################################

################################################################################
def turnStateLogOfJSON(play: Playing) -> str :
    """ (ターンの最後に実行するのが) """
    myTurn = None
    log = []
    for i in play.log[::-1] :
        if myTurn is None :
            myTurn = i["remaining_turn"]
        if i["remaining_turn"] == myTurn :
            log.append(i)

    tileA = []
    team = play.field.teamTile(play.teamA)
    for y in range( len( team ) ) :
        for x in range( len( team[y] ) ) :
            if team[y][x] :
                tileA.append( {"x": x, "y": y} )
    tileB = []
    team = play.field.teamTile(play.teamB)
    for y in range( len( team ) ) :
        for x in range( len( team[y] ) ) :
            if team[y][x] :
                tileB.append( {"x": x, "y": y} )
    turnLog = {
        "action_log": log,
        "tile_teamA": tileA,
        "tile_teamB": tileB
    }
    return json.dumps(turnLog)
################################################################################

################################################################################

def fieldWatch(play: Playing) :
    f = play.field.fieldCopy
    for y in range( len( f ) + 1) :
        if y == 0 :
            for x in range( len( f[0] ) + 1 ) :
                if x == 0 :
                    print("", end="\t")
                else :
                    print(x-1, end="\t")
            print()
        else :
            for x in range( len( f[y-1] ) + 1 ) :
                if x == 0 :
                    print(f"    {y - 1}", end="\t")
                else :
                    OK_A = (x-1, y-1) in [
                        (play.teamA[0].x, play.teamA[0].y),
                        (play.teamA[1].x, play.teamA[1].y)
                    ]
                    OK_B = (x-1, y-1) in [
                        (play.teamB[0].x, play.teamB[0].y),
                        (play.teamB[1].x, play.teamB[1].y)
                    ]
                    if OK_A or OK_B :
                        if play.field.teamTile(play.teamA)[y-1][x-1] :
                            print(f"<{f[y-1][x-1]}:A>", end="\t")
                        elif play.field.teamTile(play.teamB)[y-1][x-1] :
                            print(f"<{f[y-1][x-1]}:B>", end="\t")
                        else :
                            print(f"<{f[y-1][x-1]}: >", end="\t")
                    else :
                        if play.field.teamTile(play.teamA)[y-1][x-1] :
                            print(f"[{f[y-1][x-1]}:A]", end="\t")
                        elif play.field.teamTile(play.teamB)[y-1][x-1] :
                            print(f"[{f[y-1][x-1]}:B]", end="\t")
                        else : print(f"[{f[y-1][x-1]}: ]", end="\t")
            print()
    print()
################################################################################
