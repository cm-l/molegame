# main.py
import math
import random

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
player = entity.Player((board.TILE_SIZE / 2, board.TILE_SIZE / 2), PLAYER_SPEED)
sprites = pygame.sprite.Group()
sprites.add(player)

# TODO porządnie to
some_boulder = entity.Boulder((48, 16), 1.25)
sprites.add(some_boulder)
other_boulder = entity.Boulder((48, 80), 1.25)
sprites.add(other_boulder)


# Timing movements
last_move_time = pygame.time.get_ticks()

# Add variables to track target position and movement speed
target_x = player.rect.x
target_y = player.rect.y
movement_speed = 16  # Adjust this value for your desired movement speed

# Add a zoom level variable
zoom_level = 1.64  # 1.0 means no zoom, adjust as needed

# Set up the camera with a zoom level
camera = pygame.Rect(0, 0, int(board.SCREEN_WIDTH / zoom_level), int(board.SCREEN_HEIGHT / zoom_level))


# Particle class for visual effects
class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, particle_image):
        super().__init__()
        self.image = particle_image
        self.rect = self.image.get_rect(center=(x, y))
        self.lifetime = 3 * 60  # Adjust the lifetime of particles
        self.speed = random.uniform(1, 2.4)  # Use uniform for more variability
        self.angle = random.uniform(0, 360)  # Random angle
        self.rotation = random.uniform(0, 360)  # Random rotation

        # Random shade
        self.image = pygame.transform.rotate(self.image, self.rotation)

        self.shade = random.randint(66, 255)  # Adjust the shade range
        self.image.fill((self.shade, self.shade, self.shade), special_flags=pygame.BLEND_RGBA_MULT)

    def update(self):
        self.lifetime -= 1
        if self.lifetime > 0:
            self.rect.x += self.speed * math.cos(self.angle)
            self.rect.y += self.speed * math.sin(self.angle)
            self.speed *= 0.95  # Particle slowing down over time

            # Fade the particle gradually
            alpha = int((self.lifetime / 180) * 255)  # Gradual alpha reduction over 3 seconds
            self.image.set_alpha(alpha)
        else:
            self.kill()


# Particle group
particles = pygame.sprite.Group()
sprites.add(particles)
# TODO posprzątać
particleimage = pygame.image.load("img/particles/particle.png")
dirt_digging_sound = pygame.mixer.Sound("sfx/dig.wav")

# The main game loop
while running:
    # Limit the frame rate to FPS
    clock.tick(FPS)

    # Get the current position of the mouse cursor
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Calculate the row and column of the tile the cursor is over
    hover_row = mouse_y // board.TILE_SIZE
    hover_col = mouse_x // board.TILE_SIZE

    # Display debugging information about the hovered tile
    print(f"Hovered Tile - Row: {hover_row}, Column: {hover_col}")

    # Check if the hovered position is within the board boundaries
    if 0 <= hover_row < board.ROWS and 0 <= hover_col < board.COLS:
        hover_tile = board.board[hover_row][hover_col]
        print(f"Type: {hover_tile.type}")
        print(f"Entity: {hover_tile.entity}")

    # Handle events
    for event in pygame.event.get():
        # If the user clicks the close button, exit the loop
        if event.type == pygame.QUIT:
            running = False
        # Zooming in and out!
        elif event.type == pygame.MOUSEWHEEL:
            # Adjust zoom level based on mouse wheel movement
            zoom_change = event.y  # event.y will be positive for zoom in, negative for zoom out
            zoom_level = max(1.0, min(4.0, zoom_level + 0.086 * zoom_change))

    # Get the key pressed by the user
    key_pressed = pygame.key.get_pressed()
    # Get the current position and tile of the player
    x, y = player.rect.center
    row, col = y // board.TILE_SIZE, x // board.TILE_SIZE
    tile = board.board[row][col]

    # Move the player according to the key pressed with a cooldown
    current_time = pygame.time.get_ticks()
    cooldown_time = 180  # Key press cooldown

    # Move the player according to the key pressed
    if key_pressed[pygame.K_LEFT] and current_time - last_move_time > cooldown_time:
        # Calculate the next position
        next_col = col - 1
        if next_col >= 0 and board.board[row][next_col].type != 2:
            # Set the target position for smooth interpolation
            target_x = next_col * board.TILE_SIZE
            last_move_time = current_time

    if key_pressed[pygame.K_RIGHT] and current_time - last_move_time > cooldown_time:
        # Calculate the next position
        next_col = col + 1
        if next_col < board.COLS and board.board[row][next_col].type != 2:
            # Set the target position for smooth interpolation
            target_x = next_col * board.TILE_SIZE  # Tiny offset to account for sprite centering
            last_move_time = current_time

    if key_pressed[pygame.K_UP] and current_time - last_move_time > cooldown_time:
        # Calculate the next position
        next_row = row - 1
        if next_row >= 0 and board.board[next_row][col].type != 2:
            # Set the target position for smooth interpolation
            target_y = next_row * board.TILE_SIZE
            last_move_time = current_time

    if key_pressed[pygame.K_DOWN] and current_time - last_move_time > cooldown_time:
        # Calculate the next position
        next_row = row + 1
        if next_row < board.ROWS and board.board[next_row][col].type != 2:
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

    # Check if the player is on a dirt tile and hasn't already triggered it
    if board.board[row][col].type == 0:
        # Play sound effect
        volume_factor = random.uniform(0.82, 1.0)  # Adjust the volume range
        dirt_digging_sound.set_volume(volume_factor)
        dirt_digging_sound.play()

        # Add particles
        # Create particles for visual effects
        for _ in range(20):  # Adjust the number of particles
            particle = Particle(player.rect.centerx, player.rect.centery, particleimage)
            particles.add(particle)

        # Change the tile to an EMPTY tile
        board.board[row][col].type = 1


    # Fill the screen with black
    board.screen.fill(BLACK)

    # Draw the board on the screen with the camera offset
    board.draw_board(camera, zoom_level, sprites, particles)

    # Update the sprites
    # sprites.update()
    # Draw the sprites on the screen
    # sprites.draw(board.screen)

    # Update entities
    # Boulders
    some_boulder.update(board)
    other_boulder.update(board)

    # Update particles
    # TODO yeet particles into its own class and establish proper inheritance for different ones
    particles.update()

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
