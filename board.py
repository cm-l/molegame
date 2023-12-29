# board.py
import pygame
import tile

# Define some constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
ROWS = 32
COLS = 32

# Initialize pygame and create a screen
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kret!")

# Create a board as a 2D list of tiles
board = []
for row in range(ROWS):
    board.append([])
    for col in range(COLS):
        # Randomly assign a type to each tile
        tile_type = tile.Tile.random_type()
        # Create a tile object with the type and position
        board[row].append(tile.Tile(tile_type, row, col))


# A function to draw the board and entities on the screen with camera offset and zoom level
def draw_board(camera, zoom_level, sprites, particles):

    # Draw tiles
    for row in range(ROWS):
        for col in range(COLS):
            # Get the tile object at the current position
            t = board[row][col]
            # Get the color and image corresponding to the tile type
            color = t.get_color()
            image = t.get_image()
            # Calculate the pixel coordinates of the tile with camera offset and zoom level
            x = int(col * TILE_SIZE * zoom_level) - camera.x
            y = int(row * TILE_SIZE * zoom_level) - camera.y
            # Draw a rectangle with the color
            pygame.draw.rect(screen, color, (x, y, int(TILE_SIZE * zoom_level), int(TILE_SIZE * zoom_level)))
            # Draw the image on top of the rectangle
            if image:
                image_size = (int(TILE_SIZE * zoom_level), int(TILE_SIZE * zoom_level))
                screen.blit(pygame.transform.scale(image, image_size), (x, y))

    # Draw particles below entities
    for particle in particles:
        # Apply zoom level to particle sprite
        scaled_rect = pygame.Rect(
            int(particle.rect.x * zoom_level) - camera.x,
            int(particle.rect.y * zoom_level) - camera.y,
            int(particle.rect.width * zoom_level),
            int(particle.rect.height * zoom_level)
        )
        screen.blit(pygame.transform.scale(particle.image, scaled_rect.size), scaled_rect)

    # Draw entities with zoom level
    for sprite in sprites:
        scaled_rect = pygame.Rect(
            int(sprite.rect.x * zoom_level) - camera.x,
            int(sprite.rect.y * zoom_level) - camera.y,
            int(sprite.rect.width * zoom_level),
            int(sprite.rect.height * zoom_level)
        )
        screen.blit(pygame.transform.scale(sprite.image, scaled_rect.size), scaled_rect)



# A function to update the board state
def update_board():
    # TODO: Add your game logic here
    pass
