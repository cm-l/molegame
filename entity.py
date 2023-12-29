# entity.py
import pygame

import board

# Load some images for the entities
boulder_image = pygame.image.load("img/boulder.png")
enemy_image = pygame.image.load("img/lava_fish.png")
dynamite_image = pygame.image.load("img/dynamite.png")
player_image = pygame.image.load("img/player.png")

# Load some sounds and tunes
collision_sound = pygame.mixer.Sound("sfx/thud.wav")


# A base class for all entities
class Entity(pygame.sprite.Sprite):
    # A constructor that takes an image, a position, and a speed
    def __init__(self, image, pos, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = speed

    # A method to update the entity's position
    def update(self):
        self.update_tile()

    # A method to update the tile reference
    def update_tile(self):
        # Get the row and column of the tile
        row = self.rect.centery // board.TILE_SIZE
        col = self.rect.centerx // board.TILE_SIZE

        # Update the entity reference in the tile
        if 0 <= row < board.ROWS and 0 <= col < board.COLS:
            tile = board.board[row][col]
            # print(f"{tile.row}, {tile.col} has a {type(tile.entity)} on it.")
            tile.entity = self


# A subclass for boulders
class Boulder(Entity):
    # A constructor that calls the base class constructor with the boulder image
    def __init__(self, pos, speed):
        Entity.__init__(self, boulder_image, pos, speed)
        self.collision_sound = collision_sound
        self.collided = False
        self.collision_cooldown = 0  # Add a cooldown attribute

    # A method to update the boulder's position and behavior
    def update(self, board):
        # Basic behaviors
        super().update()

        # If there's a cooldown, decrement it
        if self.collision_cooldown > 0:
            self.collision_cooldown -= 1

        # Get the current position and tile of the boulder
        x, y = self.rect.topleft
        row, col = y // board.TILE_SIZE, x // board.TILE_SIZE
        tile_below = board.board[row + 1][col]
        tile_right = board.board[row][col + 1]
        tile_left = board.board[row][col - 1]

        # Check if the tile below the boulder is EMPTY
        if tile_below.type == 1:
            # Move the boulder one tile downwards
            self.rect.y += self.speed
            self.collided = False  # Reset the collided flag when moving down
            # print(f"Falling! Below me is ({tile_below.row},{tile_below.col} {tile_below.type}) with a {type(tile_below.entity).__name__}")
        elif not self.collided and self.collision_cooldown == 0:
            # Play collision sound only if not previously collided and cooldown is over
            # self.collision_sound.play()
            self.collided = True  # Set the collided flag to True
            self.collision_cooldown = 5  # Set a cooldown (adjust the value as needed)

        # Look to the right if the tile below is occupied by another boulder and cooldown is over
        if isinstance(tile_below.entity, Boulder) and tile_below.entity != self and self.collision_cooldown == 0:
            # self.rect.x += board.TILE_SIZE
            print(f"Boulder below! At {tile_below.row}, {tile_below.col} is a {type(tile_below.entity).__name__}")
            self.collision_sound.play()



# A subclass for enemies
class Enemy(Entity):
    # A constructor that calls the base class constructor with the enemy image
    def __init__(self, pos, speed):
        Entity.__init__(self, enemy_image, pos, speed)

    # A method to update the enemy's position and behavior
    def update(self):
        # TODO: Add your enemy logic here
        pass


# A subclass for dynamites
class Dynamite(Entity):
    # A constructor that calls the base class constructor with the dynamite image
    def __init__(self, pos, speed):
        Entity.__init__(self, dynamite_image, pos, speed)

    # A method to update the dynamite's position and behavior
    def update(self):
        # TODO: Add your dynamite logic here
        pass


# A subclass for the player
class Player(Entity):
    # A constructor that calls the base class constructor with the player image
    def __init__(self, pos, speed):
        Entity.__init__(self, player_image, pos, speed)

    # A method to update the player's position and behavior
    def update(self):
        # TODO: Add your player logic here
        pass
