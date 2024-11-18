class Tile:
    # direction values for intersections:
    # 0: ┗, 1: ┏, 2: ┓, 3: ┛
    # 0: ┣, 1: ┳, 2: ┫, 3: ┻
    # 0: ╋, 1: ╋, 2: ╋, 3: ╋
    # 0: Up, 1: Right, 2: Down, 3: Left

    def __init__(self, connections: [int], pos: (int, int), connection_type: str, is_in_mesh=False):
        self.connections = connections
        self.pos = pos
        self.pos_up = (self.pos[0], self.pos[1] - 1)
        self.pos_down = (self.pos[0], self.pos[1] + 1)
        self.pos_left = (self.pos[0] - 1, self.pos[1])
        self.pos_right = (self.pos[0] + 1, self.pos[1])
        self.connection_type = connection_type
        self.is_in_mesh = is_in_mesh
        self.vertices = []

    def add_connection(self, connection: int):
        self.connections.append(connection)
        self.connections = sorted(self.connections)

    def get_connections_length(self):
        return len(self.connections)

    # vertices position by index
    # 0    1
    #
    # 3    2
    def generate_vertices(self):
        self.vertices.append((self.pos[0] - 0.5, self.pos[1] - 0.5))  # TL
        self.vertices.append((self.pos[0] + 0.5, self.pos[1] - 0.5))  # TR
        self.vertices.append((self.pos[0] + 0.5, self.pos[1] + 0.5))  # BR
        self.vertices.append((self.pos[0] - 0.5, self.pos[1] + 0.5))  # BL

    def __getitem__(self, item):
        return self.pos[item]
