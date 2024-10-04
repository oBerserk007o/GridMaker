import random
import pygame
import sys

# initialize it
pygame.init()

# configurations
unit = 40
block_width_number = 12
block_height_number = 12
block_number = block_height_number*block_width_number
fps = 15
window_height = block_height_number * unit
window_width = block_width_number * unit

# title
pygame.display.set_caption("Grid Maker")

# colours (yes, I'm canadian, I put u's in words)
DARK_GREEN = (40, 173, 49)
LIGHT_GREEN = (79, 238, 90)
RED = (191, 25, 25)
BLUE = (52, 91, 235)

# creating window
display = pygame.display.set_mode((window_width, window_height))

# creating our frame regulator
clock = pygame.time.Clock()

# position of the player
pos = pygame.Vector2(0, display.get_height() - unit)
pos_block = pygame.Vector2(0, block_height_number - 1)
length = 3
mesh = []
new_items_in_mesh = []


def draw_grid():
    for x in range(int(block_width_number)):
        for y in range(int(block_height_number)):
            rect = pygame.Rect(x * unit, y * unit, unit, unit)
            pygame.draw.rect(display, BLUE if (x, y) in mesh
            else (DARK_GREEN if (x + y) % 2 == 0 else LIGHT_GREEN), rect)


            # for showing positions of each cell
            text = pygame.font.Font('comfortaa.ttf', 15)
            text_surface = text.render(f"{x}, {y}", True, RED)
            text_rect = text_surface.get_rect(center=((x * unit) + unit / 2, (y * unit) + unit / 2))
            display.blit(text_surface, text_rect)
    pygame.display.flip()

draw_grid()

# forever loop
while True:
    # frame clock ticking
    clock.tick(fps)

    if len(new_items_in_mesh) != 0:
        x = new_items_in_mesh[0][0]
        y = new_items_in_mesh[0][1]
        rect = pygame.Rect(x * unit, y * unit, unit, unit)
        pygame.draw.rect(display, BLUE, rect)

        text = pygame.font.Font('comfortaa.ttf', 15)
        text_surface = text.render(f"{x}, {y}", True, RED)
        text_rect = text_surface.get_rect(center=((x * unit) + unit / 2, (y * unit) + unit / 2))
        display.blit(text_surface, text_rect)
        new_items_in_mesh.pop(0)

    pygame.display.flip()

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            click_pos = pygame.mouse.get_pos()
            clicked_block = (round((click_pos[0] - unit / 2) / unit), round((click_pos[1] - unit / 2) / unit))
            if clicked_block not in mesh:
                mesh.append(clicked_block)
                new_items_in_mesh.append(clicked_block)
            print(click_pos, clicked_block, mesh)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
