import pygame
import sys

# initialize it
pygame.init()

# configurations
unit = 40
blockWidthNumber = 12
blockHeightNumber = 12
blockNumber = blockHeightNumber*blockWidthNumber
fps = 30
windowHeight = blockHeightNumber * unit
windowWidth = blockWidthNumber * unit

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
display = pygame.display.set_mode((windowWidth, windowHeight))

# creating our frame regulator
clock = pygame.time.Clock()

# position of the player
pos = pygame.Vector2(0, display.get_height() - unit)
pos_block = pygame.Vector2(0, blockHeightNumber - 1)
length = 3
mesh = []
newItemsInMesh = []
deletedItemsInMesh = []

def draw_grid():
    for x in range(int(blockWidthNumber)):
        for y in range(int(blockHeightNumber)):
            rect = pygame.Rect(x * unit, y * unit, unit, unit)
            pygame.draw.rect(display, DARK_GREEN if (x + y) % 2 == 0 else LIGHT_GREEN, rect)

            # for showing positions of each cell
            text = pygame.font.Font('comfortaa.ttf', 15)
            textSurface = text.render(f"{x}, {y}", True, GREY)
            textRect = textSurface.get_rect(center=((x * unit) + unit / 2, (y * unit) + unit / 2))
            display.blit(textSurface, textRect)
    pygame.display.flip()

draw_grid()

# forever loop
while True:
    # frame clock ticking
    clock.tick(fps)

    if len(newItemsInMesh) != 0:
        x = newItemsInMesh[0][0]
        y = newItemsInMesh[0][1]
        rect = pygame.Rect(x * unit, y * unit, unit, unit)
        pygame.draw.rect(display, BLACK, rect)

        text = pygame.font.Font('comfortaa.ttf', 15)
        textSurface = text.render(f"{x}, {y}", True, WHITE)
        textRect = textSurface.get_rect(center=((x * unit) + unit / 2, (y * unit) + unit / 2))
        display.blit(textSurface, textRect)
        newItemsInMesh.pop(0)

    if len(deletedItemsInMesh) != 0:
        x = deletedItemsInMesh[0][0]
        y = deletedItemsInMesh[0][1]
        rect = pygame.Rect(x * unit, y * unit, unit, unit)
        pygame.draw.rect(display, DARK_GREEN if (x + y) % 2 == 0 else LIGHT_GREEN, rect)

        text = pygame.font.Font('comfortaa.ttf', 15)
        textSurface = text.render(f"{x}, {y}", True, GREY)
        textRect = textSurface.get_rect(center=((x * unit) + unit / 2, (y * unit) + unit / 2))
        display.blit(textSurface, textRect)
        deletedItemsInMesh.pop(0)

    pygame.display.flip()

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            click_pos = pygame.mouse.get_pos()
            clicked_block = (round((click_pos[0] - unit / 2) / unit), round((click_pos[1] - unit / 2) / unit))
            if clicked_block not in mesh:
                mesh.append(clicked_block)
                newItemsInMesh.append(clicked_block)
            else:
                mesh.pop(mesh.index(clicked_block))
                deletedItemsInMesh.append(clicked_block)

            print(click_pos, clicked_block, mesh)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
