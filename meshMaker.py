from math import sqrt
from tile import Tile


def meshMaker(meshList: [(int, int)]):
    mesh = findCorners(meshList)
    return mesh


def findCorners(meshList: [(int, int)]):
    tiles = []
    tilesToRemove = []
    for pos in meshList:
        tiles.append(Tile([], pos, ""))
    for tile in tiles:
        if tile.posUp in meshList:
            tile.addConnection(0)
        if tile.posRight in meshList:
            tile.addConnection(1)
        if tile.posDown in meshList:
            tile.addConnection(2)
        if tile.posLeft in meshList:
            tile.addConnection(3)
    for tile in tiles:
        if tile.connections == [1, 3] or tile.connections == [0, 2]:
            tilesToRemove.append(tile)
            continue
        match tile.getConnectionsLength():
            case 0:
                tile.connectionType = "lone"
            case 1:
                tile.connectionType = "end"
            case 2:
                tile.connectionType = "turn"
            case 3:
                tile.connectionType = "T"
            case 4:
                tile.connectionType = "+"
            case _:
                print("Houston, we have a problem")
    for tile in tilesToRemove:
        tiles.remove(tile)
    return tiles

