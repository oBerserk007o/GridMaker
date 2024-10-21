import pygame
import sys
from meshMaker import meshMaker

# initialize it
pygame.init()

# configurations
unit = 30
blockWidthNumber = 24
blockHeightNumber = 24
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
currentTiles = []


def drawSquare(xPos, yPos, colour, message, textColour, size):
    rectangle = pygame.Rect(xPos * unit, yPos * unit, unit, unit)
    pygame.draw.rect(display, colour, rectangle)
    writeSquare(xPos, yPos, message, textColour, size)


def writeSquare(xPos, yPos, message, textColour, size):
    textMessage = pygame.font.Font('comfortaa.ttf', size)
    txtSurface = textMessage.render(message, True, textColour)
    txtRect = txtSurface.get_rect(center=((xPos * unit) + unit / 2, (yPos * unit) + unit / 2))
    display.blit(txtSurface, txtRect)


for x in range(int(blockWidthNumber)):
    for y in range(int(blockHeightNumber)):
        drawSquare(x, y, DARK_GREEN if (x + y) % 2 == 0 else LIGHT_GREEN,
                   f"{x}, {y}", GREY, 2 * int(30 / len(f"{x}, {y}")))
pygame.display.flip()


# forever loop
while True:
    # frame clock ticking
    clock.tick(fps)

    if len(newItemsInMesh) != 0:
        x = newItemsInMesh[0][0]
        y = newItemsInMesh[0][1]
        drawSquare(x, y, BLACK, f"{x}, {y}", WHITE, 2 * int(30 / len(f"{x}, {y}")))
        newItemsInMesh.pop(0)

    if len(deletedItemsInMesh) != 0:
        x = deletedItemsInMesh[0][0]
        y = deletedItemsInMesh[0][1]
        drawSquare(x, y, DARK_GREEN if (x + y) % 2 == 0 else LIGHT_GREEN,
                   f"{x}, {y}", GREY, 2 * int(30 / len(f"{x}, {y}")))
        deletedItemsInMesh.pop(0)

    pygame.display.flip()

    if pygame.mouse.get_pressed(3)[0]:
        clickPos = pygame.mouse.get_pos()
        clickedBlock = (round((clickPos[0] - unit / 2) / unit), round((clickPos[1] - unit / 2) / unit))
        if clickedBlock not in mesh:
            mesh.append(clickedBlock)
            newItemsInMesh.append(clickedBlock)

    if pygame.mouse.get_pressed(3)[2]:
        clickPos = pygame.mouse.get_pos()
        clickedBlock = (round((clickPos[0] - unit / 2) / unit), round((clickPos[1] - unit / 2) / unit))
        if clickedBlock in mesh:
            mesh.pop(mesh.index(clickedBlock))
            deletedItemsInMesh.append(clickedBlock)

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            tiles = meshMaker(mesh, blockWidthNumber, blockHeightNumber)

            for tile in currentTiles:
                x = tile.pos[0]
                y = tile.pos[1]
                drawSquare(x, y, BLACK, f"{x}, {y}", WHITE, 2 * int(30 / len(f"{x}, {y}")))

            for tile in tiles:
                if tile not in currentTiles:
                    drawSquare(tile.pos[0], tile.pos[1], WHITE, tile.connectionType, BLACK, 10)
            currentTiles = tiles.copy()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
