# entity.py
import pygame

# Load some images for the entities
boulder_image = pygame.image.load("img/boulder.png")
enemy_image = pygame.image.load("img/lava_fish.png")
dynamite_image = pygame.image.load("img/dynamite.png")
player_image = pygame.image.load("img/player.png")


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
        # TODO: Add your movement logic here
        pass


# A subclass for boulders
class Boulder(Entity):
    # A constructor that calls the base class constructor with the boulder image
    def __init__(self, pos, speed):
        Entity.__init__(self, boulder_image, pos, speed)

    # A method to update the boulder's position and behavior
    def update(self):
        # TODO: Add your boulder logic here
        pass


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
