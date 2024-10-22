from tile import Tile


def mesh_maker(corners_list: [(int, int)]):
    
    return


def find_corners(mesh_list: [(int, int)]):
    tiles = []
    tiles_to_remove = []
    for pos in mesh_list:
        tiles.append(Tile([], pos, ""))
    for tile in tiles:
        if tile.pos_up in mesh_list:
            tile.add_connection(0)
        if tile.pos_right in mesh_list:
            tile.add_connection(1)
        if tile.pos_down in mesh_list:
            tile.add_connection(2)
        if tile.pos_left in mesh_list:
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
    tiles = sorted(tiles, key=lambda tup: tup.pos[0])
    return tiles

