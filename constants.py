import pygame
#Constants defined for other modules to import

#Screen Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_HALF_WIDTH = SCREEN_WIDTH / 2
SCREEN_HALF_HEIGHT = SCREEN_HEIGHT /2

#Groups are defined here
updatable_group = pygame.sprite.Group()
drawable_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()
shot_group = pygame.sprite.Group()

#Asteroid Constants
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
#asteroid_spawn_rate = 5
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
ASTEROID_LIFESPAN = 20
ASTEROID_VELOCITY_MULTIPLIER = 1.5  #Currently Only affects asteroids that get hit by a bullet and split

#Player Constants
PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN = 0.3
PLAYER_STARTING_LIVES = 3
PLAYER_INVINCIBILITY_TIMER = 6.8
PLAYER_DEATH_TIMER = 4.8
DEATH_FLOWER_COOLDOWN = 30
BULLET_STREAM_COOLDOWN = 15
BULLET_STREAM_DURATION = 8
TRI_SHOT_COOLDOWN = 20
TRI_SHOT_DURATION = 8
KEY_LOCK_TIMER = 1

#Color Constants
PLAYER_COLOR = [255,255,255]
ASTEROID_COLOR = [255,255,255]
GAMEOVER_COLOR = [255,0,0]
SCREEN_COLOR = [0,0,0]
SHOT_COLOR = [155,0,155]

#Shot Constants
SHOT_RADIUS = 5
SHOT_LIFESPAN = 3.5
TRI_SHOT_ROTATION = 15

#Bar Locations
BOTTOM_BAR_LOC_X = 10
BOTTOM_BAR_LOC_Y = SCREEN_HEIGHT - 16

#Sound Delay

SOUND_DELAY = 1.0