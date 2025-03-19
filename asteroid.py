import pygame
from circleshape import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.x = x
        self.y = y
        self.radius = radius
        #print(f"Debug: Asteroid init.  {self.x},{self.y},Rad-{self.radius}")

    def draw(self,screen):
        color = [255,255,255]
        pygame.draw.circle(screen,color,(self.x,self.y),self.radius,width=2)
        #print(f"Debug: Asteroid Drawn at {self.x},{self.y}")
    
    def update(self,dt):
        self.x += self.velocity.x * dt
        self.y += self.velocity.y * dt
        #print(f"Debug: Asteroid Update was called. {self.x},{self.y}")