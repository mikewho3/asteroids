#import required modules
import pygame
from circleshape import *

#create the Asteroid class, parent is CircleShape
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):  #initialize
        super().__init__(x,y,radius)  #initialize parent CircleShape - Required to draw and update asteroids!
        #the next line is backup code to directly call the sprite containers and thus draw and update the asteroids, not needed since I called super
        #pygame.sprite.Sprite.__init__(self,self.containers)
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self,screen,color):
        self.color = color
        pygame.draw.circle(screen,self.color,(self.position.x,self.position.y),self.radius,width=2)
    
    def update(self,dt):
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt
