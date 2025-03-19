import pygame
from player import *
from asteroidfield import *

def main():
    pygame.init()
    updatable_group = pygame.sprite.Group()
    drawable_group = pygame.sprite.Group()
    asteroid_group = pygame.sprite.Group()
    Player.containers = (updatable_group,drawable_group)
    Asteroid.containers = (updatable_group,drawable_group)
    AsteroidField.containers = (updatable_group)
    CircleShape.containers = drawable_group
    clock = pygame.time.Clock()
    running = True
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    ship = Player(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
    asfield = AsteroidField()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill([0,0,0])
        #ship.draw(screen)
        #ship.update(dt)
        #updatable_group.update(dt)
        for updatable in updatable_group:
            updatable.update(dt)
        for drawable in drawable_group:
            drawable.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()