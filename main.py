# main.py
import pygame
import board
import entity

# Define some constants
FPS = 60
BLACK = (0, 0, 0)
PLAYER_SPEED = 1

# Create a clock object to control the game's frame rate
clock = pygame.time.Clock()

# Create a boolean variable to control the game loop
running = True

# Create a player object and add it to a sprite group
player = entity.Player((board.TILE_SIZE/2, board.TILE_SIZE/2), PLAYER_SPEED)
sprites = pygame.sprite.Group()
sprites.add(player)

# Timing movements
last_move_time = pygame.time.get_ticks()

# Add variables to track target position and movement speed
target_x = player.rect.x
target_y = player.rect.y
movement_speed = 16  # Adjust this value for your desired movement speed

# Add a zoom level variable
zoom_level = 4.0  # 1.0 means no zoom, adjust as needed

# Set up the camera with a zoom level
camera = pygame.Rect(0, 0, int(board.SCREEN_WIDTH / zoom_level), int(board.SCREEN_HEIGHT / zoom_level))

# The main game loop
while running:
    # Limit the frame rate to FPS
    clock.tick(FPS)

    # Handle events
    for event in pygame.event.get():
        # If the user clicks the close button, exit the loop
        if event.type == pygame.QUIT:
            running = False
        # Zooming in and out!
        elif event.type == pygame.MOUSEWHEEL:
            # Adjust zoom level based on mouse wheel movement
            zoom_change = event.y  # event.y will be positive for zoom in, negative for zoom out
            zoom_level = max(1.0, min(4.0, zoom_level + 0.1 * zoom_change))

    # Get the key pressed by the user
    key_pressed = pygame.key.get_pressed()
    # Get the current position and tile of the player
    x, y = player.rect.center
    row, col = y // board.TILE_SIZE, x // board.TILE_SIZE
    tile = board.board[row][col]

    # Move the player according to the key pressed with a cooldown
    current_time = pygame.time.get_ticks()
    cooldown_time = 225  # Key press cooldown

    # Move the player according to the key pressed
    if key_pressed[pygame.K_LEFT] and current_time - last_move_time > cooldown_time:
        # Calculate the next position
        next_col = col - 1
        if next_col >= 0 and board.board[row][next_col].type == 1:
            # Set the target position for smooth interpolation
            target_x = next_col * board.TILE_SIZE
            last_move_time = current_time

    if key_pressed[pygame.K_RIGHT] and current_time - last_move_time > cooldown_time:
        # Calculate the next position
        next_col = col + 1
        if next_col < board.COLS and board.board[row][next_col].type == 1:
            # Set the target position for smooth interpolation
            target_x = next_col * board.TILE_SIZE  # Tiny offset to account for sprite centering
            last_move_time = current_time

    if key_pressed[pygame.K_UP] and current_time - last_move_time > cooldown_time:
        # Calculate the next position
        next_row = row - 1
        if next_row >= 0 and board.board[next_row][col].type == 1:
            # Set the target position for smooth interpolation
            target_y = next_row * board.TILE_SIZE
            last_move_time = current_time

    if key_pressed[pygame.K_DOWN] and current_time - last_move_time > cooldown_time:
        # Calculate the next position
        next_row = row + 1
        if next_row < board.ROWS and board.board[next_row][col].type == 1:
            # Set the target position for smooth interpolation
            target_y = next_row * board.TILE_SIZE
            last_move_time = current_time

    # Smoothly interpolate the player's position
    player.rect.x += int((target_x - player.rect.x) * movement_speed / board.TILE_SIZE)
    player.rect.y += int((target_y - player.rect.y) * movement_speed / board.TILE_SIZE)

    # Update the camera to follow the player with zoom level
    camera.x = int(player.rect.x * zoom_level - (board.SCREEN_WIDTH // 2))
    camera.y = int(player.rect.y * zoom_level - (board.SCREEN_HEIGHT // 2))

    # Ensure the camera doesn't go beyond the game boundaries
    max_x = int(board.TILE_SIZE * board.COLS * zoom_level - board.SCREEN_WIDTH)
    max_y = int(board.TILE_SIZE * board.ROWS * zoom_level - board.SCREEN_HEIGHT)
    camera.x = max(0, min(camera.x, max_x))
    camera.y = max(0, min(camera.y, max_y))

    # Fill the screen with black
    board.screen.fill(BLACK)

    # Draw the board on the screen with the camera offset
    board.draw_board(camera, zoom_level, sprites)

    # Update the sprites
    # sprites.update()
    # Draw the sprites on the screen
    # sprites.draw(board.screen)
    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
