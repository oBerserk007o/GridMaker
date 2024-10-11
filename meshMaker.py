def meshMaker(meshList: [(int, int)], width: int, height: int):
    mesh = meshListToMesh(meshList, width, height)
    return mesh

def meshListToMesh(meshList: [(int, int)], width: int, height: int):
    topLeftEdge = (width, height)
    topRightEdge = (0, height)
    bottomLeftEdge = (width, 0)
    bottomRightEdge = (0, 0)

    for pos in meshList:
        if (pos[0] + pos[1]) < (topLeftEdge[0] + topLeftEdge[1]):
                topLeftEdge = pos
        if (pos[0] + pos[1]) > (bottomRightEdge[0] + bottomRightEdge[1]):
                bottomRightEdge = pos
        if (pos[0] - pos[1]) < (topRightEdge[0] + topRightEdge[1]):
                topRightEdge = pos
        if (pos[1] - pos[0]) < (bottomLeftEdge[0] + bottomLeftEdge[1]):
                bottomLeftEdge = pos

    return [topLeftEdge, topRightEdge, bottomLeftEdge, bottomRightEdge]