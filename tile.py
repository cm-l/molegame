# tile.py
import pygame
import random

# Define some constants
TILE_SIZE = 40
DIRT = 0
EMPTY = 1
ROCK = 2

# Load some images for the tiles
dirt_image = pygame.image.load("img/dirt.png")
dirt_image = pygame.transform.scale(dirt_image, (TILE_SIZE, TILE_SIZE))
rock_image = pygame.image.load("img/rock.png")
rock_image = pygame.transform.scale(rock_image, (TILE_SIZE, TILE_SIZE))
empty_image = pygame.image.load("img/empty.png")
empty_image = pygame.transform.scale(empty_image, (TILE_SIZE, TILE_SIZE))


# A class to represent a tile
class Tile:
    # A constructor that takes a type and a position
    def __init__(self, tile_type, row, col):
        self.type = tile_type
        self.row = row
        self.col = col
        self.entity = None

    # A method to get the color of the tile
    def get_color(self):
        if self.type == DIRT:
            return 139, 69, 19  # brown
        elif self.type == EMPTY:
            return 0, 0, 0  # black
        elif self.type == ROCK:
            return 128, 128, 128  # gray
        else:
            return 255, 255, 255  # white

    def get_glyph(self):
        if self.type == DIRT:
            return "#"
        if self.type == EMPTY:
            return "."
        if self.type == ROCK:
            return "X"

    # A method to get the image of the tile
    def get_image(self):
        if self.type == DIRT:
            return dirt_image
        elif self.type == ROCK:
            return rock_image
        elif self.type == EMPTY:
            return empty_image
        else:
            return None

    # A static method to generate a random tile type
    @staticmethod
    def random_type():
        return random.choice([EMPTY, DIRT, EMPTY, EMPTY])
