#import required modules
import pygame
from player import *

def main():  #begin main
    pygame.init()  #initialize pygame

    #Groups are defined here
    updatable_group = pygame.sprite.Group()
    drawable_group = pygame.sprite.Group()
    asteroid_group = pygame.sprite.Group()

    #Containers are defined here
    Player.containers = (updatable_group,drawable_group)
    Asteroid.containers = (updatable_group,drawable_group)
    AsteroidField.containers = (updatable_group)

    #create the clock and call pygame.time.Clock()
    clock = pygame.time.Clock()

    running = True  #if True, game will play
    dt = 0  #Not sure what this really is, but it's needed to draw the screen and time things properly
    
    #create the screen using variables defined in constants.py
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    #Starting the game
    #Lets tell us about the game
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    #create the ship / player and put them in the center of the screen
    ship = Player(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)

    #create the AsteroidField
    asfield = AsteroidField()


    #begin the main game Loop
    while running:
        for event in pygame.event.get():  #for loop that stops the process if the game windows gets closed
            if event.type == pygame.QUIT:
                return
        screen.fill([0,0,0])  #make the screen color black
        for updatable in updatable_group:  #for loop to update all objects in the group
            updatable.update(dt)
        for drawable in drawable_group:  #for loop to draw all objects in the group
            drawable.draw(screen)
        pygame.display.flip()  #not sure what this does, but it is important
        dt = clock.tick(60) / 1000  #make the clock tick

if __name__ == "__main__":
    main()