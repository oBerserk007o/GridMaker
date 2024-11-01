import pygame
import sys

from pygame import gfxdraw

from mesh_maker import MeshMaker

# initialize it
pygame.init()

# configurations
unit = 35
tile_width_number = 20
tile_height_number = 20
tile_number = tile_height_number*tile_width_number
fps = 30
window_height = tile_height_number * unit
window_width = tile_width_number * unit

# title
pygame.display.set_caption("Grid Maker")

# colours (yes, I'm canadian, I put u's in words)
DARK_GREEN = (40, 173, 49)
LIGHT_GREEN = (79, 238, 90)
RED = (191, 25, 25)
BLUE = (52, 91, 235)
LIGHT_BLUE = (66, 200, 245)
GREY = (43, 43, 43)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# creating window
display = pygame.display.set_mode((window_width, window_height))

# creating our frame regulator
clock = pygame.time.Clock()

# position of the player
pos = pygame.Vector2(0, display.get_height() - unit)
pos_tile = pygame.Vector2(0, tile_height_number - 1)
length = 3
mesh = []
new_items_in_mesh = []
deleted_items_in_mesh = []
current_tiles = []


def draw_square(x_pos, y_pos, colour, message, text_colour, size):
    rectangle = pygame.Rect(x_pos * unit, y_pos * unit, unit, unit)
    pygame.draw.rect(display, colour, rectangle)
    write_square(x_pos, y_pos, message, text_colour, size)


def write_square(x_pos, y_pos, message, text_colour, size):
    text_message = pygame.font.Font('comfortaa.ttf', size)
    txt_surface = text_message.render(message, True, text_colour)
    txt_rect = txt_surface.get_rect(center=((x_pos * unit) + unit / 2, (y_pos * unit) + unit / 2))
    display.blit(txt_surface, txt_rect)


def draw_circle(x_pos, y_pos, colour, radius=int(3 * unit / 8)):
    gfxdraw.filled_circle(display, int(x_pos * unit + unit / 2),
                          int(y_pos * unit + unit / 2), radius, colour)
    gfxdraw.aacircle(display, int(x_pos * unit + unit / 2),
                     int(y_pos * unit + unit / 2), radius, colour)


for x in range(int(tile_width_number)):
    for y in range(int(tile_height_number)):
        draw_square(x, y, DARK_GREEN if (x + y) % 2 == 0 else LIGHT_GREEN,
                   f"{x}, {y}", GREY, 2 * int(30 / len(f"{x}, {y}")))
pygame.display.flip()


# forever loop
while True:
    # frame clock ticking
    clock.tick(fps)

    if len(new_items_in_mesh) != 0:
        x = new_items_in_mesh[0][0]
        y = new_items_in_mesh[0][1]
        draw_square(x, y, BLACK, f"{x}, {y}", WHITE, 2 * int(30 / len(f"{x}, {y}")))
        new_items_in_mesh.pop(0)

    if len(deleted_items_in_mesh) != 0:
        x = deleted_items_in_mesh[0][0]
        y = deleted_items_in_mesh[0][1]
        draw_square(x, y, DARK_GREEN if (x + y) % 2 == 0 else LIGHT_GREEN,
                   f"{x}, {y}", GREY, 2 * int(30 / len(f"{x}, {y}")))
        deleted_items_in_mesh.pop(0)

    pygame.display.flip()

    if pygame.mouse.get_pressed(3)[0]:
        click_pos = pygame.mouse.get_pos()
        clicked_tile = (round((click_pos[0] - unit / 2) / unit), round((click_pos[1] - unit / 2) / unit))
        if clicked_tile not in mesh:
            mesh.append(clicked_tile)
            new_items_in_mesh.append(clicked_tile)

    if pygame.mouse.get_pressed(3)[2]:
        click_pos = pygame.mouse.get_pos()
        clicked_tile = (round((click_pos[0] - unit / 2) / unit), round((click_pos[1] - unit / 2) / unit))
        if clicked_tile in mesh:
            mesh.pop(mesh.index(clicked_tile))
            deleted_items_in_mesh.append(clicked_tile)

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            mesh_maker = MeshMaker(mesh)

            mesh_maker.find_corners()
            corners = mesh_maker.corners

            mesh_maker.generate_vertices()
            vertices = mesh_maker.vertices

            mesh_maker.generate_triangles()
            triangles = mesh_maker.triangles

            for tile in current_tiles:
                x = tile[0]
                y = tile[1]
                draw_square(x, y, BLACK, f"{x}, {y}", WHITE, 2 * int(30 / len(f"{x}, {y}")))

            for tile in corners:
                if tile not in current_tiles:
                    draw_square(tile[0], tile[1], LIGHT_BLUE, tile.connection_type, BLACK, 12)
            current_tiles = corners.copy()

            j = 0
            for vertex in vertices:
                draw_circle(vertex[0], vertex[1], BLUE, int(unit / 7))
                write_square(vertex[0], vertex[1], str(j), BLACK, int(unit / 3))
                j += 1

            print(triangles)


        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
