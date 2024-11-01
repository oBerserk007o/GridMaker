from tile import Tile


class MeshMaker:
    def __init__(self, mesh_list):
        self.vertices = []
        self.corners = []
        self.triangles = []
        self.mesh_list = mesh_list

    def find_corners(self):
        tiles = []
        tiles_to_remove = []
        for pos in self.mesh_list:
            tiles.append(Tile([], pos, ""))

        for tile in tiles:
            if tile.pos_up in self.mesh_list:
                tile.add_connection(0)
            if tile.pos_right in self.mesh_list:
                tile.add_connection(1)
            if tile.pos_down in self.mesh_list:
                tile.add_connection(2)
            if tile.pos_left in self.mesh_list:
                tile.add_connection(3)

        for tile in tiles:
            if tile.connections == [1, 3] or tile.connections == [0, 2]:
                tiles_to_remove.append(tile)
                continue
            match tile.get_connections_length():
                case 0:
                    tile.connection_type = "lone"
                case 1:
                    tile.connection_type = "end"
                case 2:
                    tile.connection_type = "turn"
                case 3:
                    tile.connection_type = "T"
                case 4:
                    tile.connection_type = "+"
                case _:
                    print("Houston, we have a problem")

        for tile in tiles_to_remove:
            tiles.remove(tile)

        self.corners = sorted(sorted(tiles, key=lambda tup: tup.pos[1]), key=lambda tup: tup.pos[0])

    def generate_vertices(self):
        for tile in self.corners:
            tile.generate_vertices()
            for vertex in tile.vertices:
                if vertex not in self.vertices:
                    self.vertices.append(vertex)

    def check_column(self, pos: (int, int)) -> [Tile]:
        column = []
        for tile in self.corners:
            if tile[1] > pos[1] and tile[0] == pos[0]:
                if 0 in tile.connections:
                    column.append(tile)
                else:
                    return column
        return column

    def check_row(self, pos: (int, int)) -> [Tile]:
        row = []
        for tile in self.corners:
            if tile[0] > pos[0] and tile[1] == pos[1]:
                if 2 in tile.connections:
                    row.append(tile)
                else:
                    return row
        return row

    def generate_triangles(self):
        for tile in self.corners:
            print(tile.pos, tile.is_in_mesh)
            column = self.check_column(tile.pos)
            row = self.check_row(tile.pos)

            if len(column) > 0:
                if not column[-1].is_in_mesh and not tile.is_in_mesh:
                    self.make_quad_column(tile, column[-1])
                    column[-1].is_in_mesh = True
                    tile.is_in_mesh = True
            if len(row) > 0:
                if not row[-1].is_in_mesh and not tile.is_in_mesh:
                    self.make_quad_row(tile, row[-1])
                    row[-1].is_in_mesh = True
                    tile.is_in_mesh = True

    def add_to_triangles(self, tiles: [Tile], indexes: [int]):
        tiles_indexes = [0, 1, 1, 0, 0, 1]
        for i in range(6):
            self.triangles.append(self.vertices.index(tiles[tiles_indexes[i]].vertices[indexes[i]]))

    # vertices position by index
    # 0    1       0    1
    #
    # 3    2       3    2
    #
    #
    # 0    1
    #
    # 3    2
    def make_quad_column(self, tile1: Tile, tile2: Tile, first_is_included=True, second_is_included=True):
        indexes = []

        if first_is_included and second_is_included:
            indexes = [1, 2, 3, 0, 1, 3]
        elif first_is_included and not second_is_included:
            indexes = [1, 1, 0, 0, 1, 0]
        elif not first_is_included and second_is_included:
            indexes = [2, 2, 3, 3, 2, 3]
        elif not first_is_included and not second_is_included:
            indexes = [2, 1, 0, 3, 2, 0]

        self.add_to_triangles([tile1, tile2], indexes)

    def make_quad_row(self, tile1: Tile, tile2: Tile, first_is_included=True, second_is_included=True):
        indexes = []

        if first_is_included and second_is_included:
            indexes = [0, 1, 2, 3, 0, 2]
        elif first_is_included and not second_is_included:
            indexes = [0, 0, 3, 3, 0, 3]
        elif not first_is_included and second_is_included:
            indexes = [1, 1, 2, 2, 1, 2]
        elif not first_is_included and not second_is_included:
            indexes = [1, 0, 3, 2, 1, 3]

        self.add_to_triangles([tile1, tile2], indexes)
