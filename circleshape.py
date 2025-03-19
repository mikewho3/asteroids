#import required modules
import pygame


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):  #initialize
        # we will be using this later
        if hasattr(self, "containers"):  #this initializes the Sprite containers and is required to draw and update
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen,color):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    #lets define a method to detect collisions
    def collision(self,other):
        distance = self.position.distance_to(other.position) #distance to the other obj
        rad = self.radius + other.radius #combined radius of the circles of both obj's
        return distance <= rad  #check if the combined radius is touching or overlaping the other obj