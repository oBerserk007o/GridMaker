from math import sqrt
from tile import Tile


def meshMaker(meshList: [(int, int)], width: int, height: int):
    mesh = meshListToMesh(meshList, width, height)
    return mesh


def findCorners(meshList: [(int, int)], width: int, height: int):
    tiles = []
    for pos in meshList:
        tiles.append(Tile([], pos))
    for tile in tiles:
        if tile.posUp in meshList:
            tile.addConnection(0)
        elif tile.posRight in meshList:
            tile.addConnection(1)
        elif tile.posDown in meshList:
            tile.addConnection(2)
        elif tile.posLeft in meshList:
            tile.addConnection(3)



def meshListToMesh(meshList: [(int, int)], width: int, height: int):
    return 0


def distanceCorners(meshList: [(int, int)], width: int, height: int):
    distances = [distance(pos) for pos in meshList]
    topLeftEdge = meshList[distances.index(min(distances))]
    distances = [distance(pos, (width, 0)) for pos in meshList]
    topRightEdge = meshList[distances.index(min(distances))]
    distances = [distance(pos, (0, height)) for pos in meshList]
    bottomLeftEdge = meshList[distances.index(min(distances))]
    distances = [distance(pos, (width, height)) for pos in meshList]
    bottomRightEdge = meshList[distances.index(min(distances))]

    return [topLeftEdge, topRightEdge, bottomLeftEdge, bottomRightEdge]


def distance(pos: (int, int), origin=(0, 0)):
    return sqrt((pos[0] - origin[0]) ** 2 + (pos[1] - origin[1]) ** 2)
