from tile import Tile


class MeshMaker:
    def __init__(self, mesh_list):
        self.vertices = []
        self.corners = []
        self.triangles = []
        self.tiles_in_mesh = []
        self.mesh_list = mesh_list

    def find_corners(self) -> None:
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

    def generate_vertices(self) -> None:
        for tile in self.corners:
            tile.generate_vertices()
            for vertex in tile.vertices:
                if vertex not in self.vertices:
                    self.vertices.append(vertex)

    # TODO make this function more efficient
    def check_column(self, pos: (int, int)) -> [Tile]:
        column = []
        for tile in self.corners:
            if tile[1] > pos[1] and tile[0] == pos[0]:
                if 0 in tile.connections:
                    column.append(tile)
                else:
                    return column
        return column

    # TODO make this function more efficient
    def check_row(self, pos: (int, int)) -> [Tile]:
        row = []
        for tile in self.corners:
            if tile[0] > pos[0] and tile[1] == pos[1]:
                if 3 in tile.connections:
                    row.append(tile)
                else:
                    return row
        return row

    def generate_triangles(self) -> None:
        for tile in self.corners:
            print(tile.pos, tile.is_in_mesh)
            column = self.check_column(tile.pos)
            row = self.check_row(tile.pos)

            if len(column) > 0:
                selected_tiles = self.select_tiles_from_mesh(tile, column[-1])
                print(selected_tiles, "column")
                index = 1
                for selected_tile in selected_tiles:
                    if index == len(selected_tiles) - 1:
                        self.make_quad(tile, column[-1], not tile.is_in_mesh, not column[-1].is_in_mesh)
                        for element in selected_tiles[:index]:
                            self.tiles_in_mesh.append(element)
                        tile.is_in_mesh = True
                        column[-1].is_in_mesh = True
                        print("Made column quad from end to end")
                        break
                    elif selected_tile in self.tiles_in_mesh:
                        found_corner = False
                        for corner in self.corners:
                            if corner.pos == selected_tile:
                                self.make_quad(tile, corner, not tile.is_in_mesh, False)
                                for element in selected_tiles[:index]:  # 4 nested for loops, new record
                                    self.tiles_in_mesh.append(element)
                                tile.is_in_mesh = True
                                found_corner = True
                        if not found_corner:
                            index += 1
                        break
                    else:
                        index += 1

            if len(row) > 0:
                selected_tiles = self.select_tiles_from_mesh(tile, row[-1])
                print(selected_tiles, "row")
                index = 1
                for selected_tile in selected_tiles:
                    if index == len(selected_tiles) - 1:
                        self.make_quad(tile, row[-1], not tile.is_in_mesh, not row[-1].is_in_mesh)
                        for element in selected_tiles[:index]:
                            self.tiles_in_mesh.append(element)
                        tile.is_in_mesh = True
                        row[-1].is_in_mesh = True
                        print("Made row quad from end to end")
                        break
                    elif selected_tile in self.tiles_in_mesh:
                        found_corner = False
                        for corner in self.corners:
                            if corner.pos == selected_tile:
                                self.make_quad(tile, corner, not tile.is_in_mesh, False)
                                tile.is_in_mesh = True
                                for element in selected_tiles[:index]:
                                    self.tiles_in_mesh.append(element)
                                found_corner = True
                        if not found_corner:
                            index += 1
                        break
                    else:
                        index += 1

            if len(row) == 0 and len(column) == 0 and not tile in self.tiles_in_mesh:
                self.make_quad(tile, tile)
                self.tiles_in_mesh.append(tile.pos)
        print(self.tiles_in_mesh)

    def add_to_triangles(self, tiles: [Tile], indexes: [int]) -> None:
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
    def make_quad(self, tile1: Tile, tile2: Tile, first_is_included=True, last_is_included=True) -> None:
        indexes = []

        if tile1[1] == tile2[1]:
            if first_is_included and last_is_included:
                indexes = [0, 1, 2, 3, 0, 2]
            elif first_is_included and not last_is_included:
                indexes = [0, 0, 3, 3, 0, 3]
            elif not first_is_included and last_is_included:
                indexes = [1, 1, 2, 2, 1, 2]
            elif not first_is_included and not last_is_included:
                indexes = [1, 0, 3, 2, 1, 3]
            self.add_to_triangles([tile1, tile2], indexes)
        elif tile1[0] == tile2[0]:
            if first_is_included and last_is_included:
                indexes = [1, 2, 3, 0, 1, 3]
            elif first_is_included and not last_is_included:
                indexes = [1, 1, 0, 0, 1, 0]
            elif not first_is_included and last_is_included:
                indexes = [2, 2, 3, 3, 2, 3]
            elif not first_is_included and not last_is_included:
                indexes = [2, 1, 0, 3, 2, 0]
            self.add_to_triangles([tile1, tile2], indexes)
        else:
            return

    # TODO make this function more efficient
    def select_tiles_from_mesh(self, tile1: Tile, tile2: Tile, first_is_included=True, last_is_included=True) -> [Tile]:
        selected_tiles = []
        if tile1[0] == tile2[0]:
            for tile in self.mesh_list:
                if tile[0] == tile1[0] and tile[1] <= tile2[1]:
                    selected_tiles.append(tile)
            if not first_is_included:
                selected_tiles.remove(tile1)
            if not last_is_included:
                selected_tiles.remove(tile2)
        elif tile1[1] == tile2[1]:
            for tile in self.mesh_list:
                if tile[1] == tile1[1] and tile[0] >= tile1[0]:
                    selected_tiles.append(tile)
            if not first_is_included:
                selected_tiles.remove(tile1)
            if not last_is_included:
                selected_tiles.remove(tile2)
        else:
            return
        return selected_tiles
