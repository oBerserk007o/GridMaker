from tile import Tile
from typing import List
from operator import itemgetter


def set_connection_type(tile: Tile, connections: int):
    match connections:
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


class MeshMaker:
    def __init__(self, mesh_list):
        self.vertices = []
        self.corners = []
        self.triangles = []
        self.tiles_in_mesh = []
        self.mesh_list = mesh_list

    def find_corners(self) -> None:
        tiles = []

        for pos in self.mesh_list:
            tile = Tile(pos, "")

            tile_connection = [False, False, False, False]
            connections = 0

            if tile.pos_up in self.mesh_list:
                tile_connection[0] = True
                connections += 1
            if tile.pos_right in self.mesh_list:
                tile_connection[1] = True
                connections += 1
            if tile.pos_down in self.mesh_list:
                tile_connection[2] = True
                connections += 1
            if tile.pos_left in self.mesh_list:
                tile_connection[3] = True
                connections += 1

            if connections == 2:
                if not (tile_connection[0] and tile_connection[2]) and not (tile_connection[1] and tile_connection[3]):
                    tiles.append(tile)
                    set_connection_type(tile, 2)
            else:
                tiles.append(tile)
                set_connection_type(tile, connections)

        self.corners = sorted(sorted(tiles, key=lambda tup: tup.pos[1]), key=lambda tup: tup.pos[0])

    def generate_vertices(self) -> None:
        for tile in self.corners:
            tile.generate_vertices()
            for vertex in tile.vertices:
                if vertex not in self.vertices:
                    self.vertices.append(vertex)

    def check_column(self, pos: (int, int)) -> [Tile]:
        column = []
        for tile in self.corners:
            if tile[1] > pos[1] and tile[0] == pos[0]:
                return column
        return column

    def check_row(self, pos: (int, int)) -> [Tile]:
        row = []
        for tile in self.corners:
            if tile[0] > pos[0] and tile[1] == pos[1]:
                return row
        return row

    def generate_triangles(self) -> None:
        for tile in self.corners:
            column = self.check_column(tile.pos)
            row = self.check_row(tile.pos)

            if len(column) > 0:
                selected_tiles = self.select_tiles_from_mesh(tile, column[-1])
                index = 1
                for selected_tile in selected_tiles:
                    if index == len(selected_tiles) - 1:
                        self.make_quad(tile, column[-1], not tile.is_in_mesh, not column[-1].is_in_mesh)
                        for element in selected_tiles[:index]:
                            self.tiles_in_mesh.append(element)
                        tile.is_in_mesh = True
                        column[-1].is_in_mesh = True
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
                index = 1
                for selected_tile in selected_tiles:
                    if index == len(selected_tiles) - 1:
                        self.make_quad(tile, row[-1], not tile.is_in_mesh, not row[-1].is_in_mesh)
                        for element in selected_tiles[:index]:
                            self.tiles_in_mesh.append(element)
                        tile.is_in_mesh = True
                        row[-1].is_in_mesh = True
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

    def select_tiles_from_mesh(self, tile1: Tile, tile2: Tile, first_is_included: bool = True,
                               last_is_included: bool = True) -> List[Tile]:

        if not (tile1[0] == tile2[0] or tile1[1] == tile2[1]):
            return []

        if tile1[0] == tile2[0]:
            x = tile1[0]
            y_min, y_max = min(tile1[1], tile2[1]), max(tile1[1], tile2[1])
            selected_tiles = {tile for tile in self.mesh_list
                              if tile[0] == x and y_min <= tile[1] <= y_max}
        else:
            y = tile1[1]
            x_min, x_max = min(tile1[0], tile2[0]), max(tile1[0], tile2[0])
            selected_tiles = {tile for tile in self.mesh_list
                              if tile[1] == y and x_min <= tile[0] <= x_max}

        if not first_is_included:
            selected_tiles.discard(tile1)
        if not last_is_included:
            selected_tiles.discard(tile2)

        return sorted(selected_tiles, key=itemgetter(0, 1))
