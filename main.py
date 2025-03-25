# Asteroids Guided Project by Mike Wylder
# Using Pygame and Boot.dev
# https://www.boot.dev/u/mikewho3
# No claim is made to any code inside as this is a learning project
# Asteroids Background Music by Muzaproduction, Used with permission under license from http://pixabay.com/service/license-summary/
#
#
#


#import required modules
import pygame
import sys
import random
from asteroidfield import *
from highscore import *

def main():  #begin main

    #initialize pygame
    pygame.init()  

    #initialize music
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048,devicename= "System Sounds")

    #Load the music
    pygame.mixer.music.load("asteroids.ogg")
    pygame.mixer.music.set_volume(0.8)

    #create the screen using variables defined in constants.py
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    #Groups are defined here
    updatable_group = pygame.sprite.Group()
    drawable_group = pygame.sprite.Group()
    asteroid_group = pygame.sprite.Group()
    shot_group = pygame.sprite.Group()

    #Keep Score Here
    score = 0

    #Setup Starting Lives
    lives = PLAYER_STARTING_LIVES
    

    #define the fonts for various things
    big_font = pygame.font.Font(None, 48)
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 16)

    #Containers are defined here
    Player.containers = (updatable_group,drawable_group)
    Asteroid.containers = (updatable_group,drawable_group,asteroid_group)
    AsteroidField.containers = (updatable_group)
    Shot.containers = (updatable_group,drawable_group,shot_group)

    #create the clock and call pygame.time.Clock()
    clock = pygame.time.Clock()

    running = True  #if True, game will play
    dt = 0  #Delta Time - Still kind of confusing, but it makes the screen draw rate independent of the screen fps
    
    #Initialize the High Score System
    high_scores = load_high_scores()
    high_scores = high_scores[:10]
    top_player_name = high_scores[0][0]
    top_player_score = high_scores[0][1]



    #Starting the game
    #Lets tell us about the game
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    #create the ship / player and put them in the center of the screen
    ship = Player(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)

    #create the AsteroidField
    asfield = AsteroidField()

    #Start the Music
    pygame.mixer.music.play(-1)



    #begin the main game Loop
    while running:
        for event in pygame.event.get():  #for loop that stops the process if the game windows gets closed
            if event.type == pygame.QUIT:
                print("Game Over!")
                print(f"Game Score: {score}")
                return
        screen.fill(SCREEN_COLOR)  #make the screen color black
        if ship.invincible_timer <= 0:
            formatted_timer = "0"
        else:
            formatted_timer = f"{ship.invincible_timer:.1f}"
        status_bar = font.render(f"Score: {score}  |  High Score: {top_player_score} by {top_player_name} | Extra Lives: {lives}  |  Invincible for {formatted_timer}/s", True, (255,255,255))
        bottom_bar = small_font.render("Music: Asteroids by Muzaproduction | Sound Effects: RetroLaser- Driken5482 | Medium Explosion- JuveriSetila  | GameOver- Tuomas_data | LostLife- Freesound Community | Used with permission under license from http://pixabay.com/service/license-summary/", True, (255,255,255))
        screen.blit(status_bar, (20,20))
        screen.blit(bottom_bar,(BOTTOM_BAR_LOC_X,BOTTOM_BAR_LOC_Y))
        for updatable in updatable_group:  #for loop to update all objects in the group
            updatable.update(dt)
        if ship.position.x < 0:
            ship.position.x = SCREEN_WIDTH
        if ship.position.x > SCREEN_WIDTH:
            ship.position.x = 0
        if ship.position.y < 0:
            ship.position.y = SCREEN_HEIGHT
        if ship.position.y > SCREEN_HEIGHT:
            ship.position.y = 0


        #for loop to check if an asteroid hits a bullet
        for asteroid in asteroid_group:

            for bullet in shot_group:
                if asteroid.collision(bullet):  #if a bullet collides with the asteroid
                    bullet.kill()  #delete the bullet
                    asteroid.split()  #delete or split the asteroid
                    if asteroid.radius >= 60:
                        score += 1
                    if asteroid.radius == 40:
                        score += 2
                    if asteroid.radius == 20:
                        score += 3



        #for loop to kill the player if they collide with an asteroid
        for asteroid in asteroid_group:
            if asteroid.collision(ship):
                if ship.invincible_timer > 0:
                    continue
                if lives > 0:
                    ouch = pygame.mixer.Sound("lostlife.mp3")
                    pygame.mixer.Sound.play(ouch)
                    lives -= 1
                else:
                    dead = pygame.mixer.Sound("gameover.mp3")
                    pygame.mixer.Sound.play(dead)
                #Screen Shake Defined
                shake_intensity = 20
                shake_duration = 1000
                shake_start = pygame.time.get_ticks()



                # Game over animation loop
                while pygame.time.get_ticks() - shake_start < shake_duration:
                    # Calculate remaining shake percentage
                    remaining = 1 - ((pygame.time.get_ticks() - shake_start) / shake_duration)
                    current_intensity = shake_intensity * remaining
                    
                    # Generate random offset
                    offset_x = random.randint(-int(current_intensity), int(current_intensity))
                    offset_y = random.randint(-int(current_intensity), int(current_intensity))
                    
                    # Clear screen
                    screen.fill(SCREEN_COLOR)
                    if ship.invincible_timer <= 0:
                        formatted_timer = "0"
                    else:
                        formatted_timer = f"{ship.invincible_timer:.1f}"
                    status_bar = font.render(f"Score: {score}  |  High Score: {top_player_score} by {top_player_name} | Extra Lives: {lives}  |  Invincible for {formatted_timer}/s", True, GAMEOVER_COLOR)
                    bottom_bar = small_font.render("Music: Asteroids by Muzaproduction | Sound Effects: RetroLaser- Driken5482 | Medium Explosion- JuveriSetila  | GameOver- Tuomas_data | LostLife- Freesound Community | Used with permission under license from http://pixabay.com/service/license-summary/", True, GAMEOVER_COLOR)
                    screen.blit(status_bar, (20,20))
                    screen.blit(bottom_bar, (BOTTOM_BAR_LOC_X,BOTTOM_BAR_LOC_Y))
                    
                    # Draw everything with shake offset
                    for drawable in drawable_group:
                        # Save original position
                        original_pos = drawable.position.copy()
                        # Apply shake offset temporarily
                        drawable.position.x += offset_x
                        drawable.position.y += offset_y
                        # Draw with game over color
                        drawable.draw(screen, GAMEOVER_COLOR)
                        # Restore original position
                        drawable.position = original_pos
                    
                    pygame.display.flip()
                    pygame.time.delay(10)  # Small delay to control frame rate
                
                # One final frame without shake
                screen.fill(SCREEN_COLOR)
                if ship.invincible_timer <= 0:
                    formatted_timer = "0"
                else:
                    formatted_timer = f"{ship.invincible_timer:.1f}"
                status_bar = font.render(f"Score: {score}  |  High Score: {top_player_score} by {top_player_name} | Extra Lives: {lives}  |  Invincible for {formatted_timer}/s", True, GAMEOVER_COLOR)
                bottom_bar = small_font.render("Music: Asteroids by Muzaproduction | Sound Effects: RetroLaser- Driken5482 | Medium Explosion- JuveriSetila  | GameOver- Tuomas_data | LostLife- Freesound Community | Used with permission under license from http://pixabay.com/service/license-summary/", True, GAMEOVER_COLOR)
                screen.blit(status_bar, (20,20))
                screen.blit(bottom_bar, (BOTTOM_BAR_LOC_X,BOTTOM_BAR_LOC_Y))
                for drawable in drawable_group:
                    drawable.draw(screen, GAMEOVER_COLOR)
                pygame.display.flip()
                
                # Additional delay after shake effect
                pygame.time.delay(1500)
                if lives > 0:
                    ship.invincible_timer = PLAYER_INVINCIBILITY_TIMER
                    ship.reset()
                else:
                    if score > top_player_score:
                        name = get_player_name(screen,font)
                        save_high_score(name,score)
                    print("Game Over!")
                    print(f"Game Score: {score}")
                    sys.exit()



        for drawable in drawable_group:  #for loop to draw all objects in the group
            if isinstance(drawable, Asteroid):
                drawable.draw(screen,ASTEROID_COLOR)  #set the default color for asteroids
            elif isinstance(drawable, Player):
                drawable.draw(screen,PLAYER_COLOR)  #set the default color for the player ship
            elif isinstance(drawable, Shot):
                drawable.draw(screen,SHOT_COLOR)  #set the default color for the player ship
            else:
                drawable.draw(screen,[255,255,255]) #if I missed anything, draw it and make it white
        pygame.display.flip()  #updates the display
        dt = clock.tick(60) / 1000  #make the clock tick

if __name__ == "__main__":
    main()