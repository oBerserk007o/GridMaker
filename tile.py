class Tile:
    # direction values for intersections:
    # 0: ┗, 1: ┏, 2: ┓, 3: ┛
    # 0: ┣, 1: ┳, 2: ┫, 3: ┻
    # 0: ╋, 1: ╋, 2: ╋, 3: ╋
    # 0: Up, 1: Right, 2: Down, 3: Left

    def __init__(self, connections: [int], pos: (int, int), connectionType: str):
        self.connections = connections
        self.pos = pos
        self.posUp = (self.pos[0], self.pos[1] + 1)
        self.posDown = (self.pos[0], self.pos[1] - 1)
        self.posLeft = (self.pos[0] - 1, self.pos[1])
        self.posRight = (self.pos[0] + 1, self.pos[1])
        self.connectionType = connectionType


    def addConnection(self, connection: int):
        self.connections.append(connection)
        self.connections = sorted(self.connections)
