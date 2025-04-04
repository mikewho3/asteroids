##############################################################################################################
# Asteroids Guided Project by Mike Wylder                                                                    #
# Using Pygame and Boot.dev                                                                                  #
# https://www.boot.dev/u/mikewho3                                                                            #
#                                                                                                            #
# All Music/Sound used with permission under license from http://pixabay.com/service/license-summary/        #
##############################################################################################################



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
    pygame.mixer.music.set_volume(0.5)

    #create the screen using variables defined in constants.py
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    #Keep Score Here
    score = 0

    

    #define the fonts for various things
    big_font = pygame.font.Font(None, 48)
    font = pygame.font.Font(None, 22)
    medium_font = pygame.font.Font(None,18)
    small_font = pygame.font.Font(None, 16)

    #Containers are defined here
    Player.containers = (updatable_group,drawable_group)
    Asteroid.containers = (updatable_group,drawable_group,asteroid_group)
    AsteroidField.containers = (updatable_group)
    Shot.containers = (updatable_group,drawable_group,shot_group)

    dt = 0
    clock = pygame.time.Clock()
    

    running = True  #if True, game will play
    
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

    def status_bar():
        if ship.invincible_timer <= 0:  #Lets not display negative values on the timer shall we?
            formatted_timer = "0"
        else:
            formatted_timer = f"{ship.invincible_timer:.1f}"  #Format the timer to only show 1 decimal place
        status_text = f"Score: {score} | Extra Lives: {ship.lives} | High Score: {top_player_score} by {top_player_name} | Death Blossom: {ship.death_flower}"
        if ship.spin_cooldown > 0:
            formatted_death_flower = f"{ship.spin_cooldown:.1f}"
            status_text += f" {formatted_death_flower}"
        status_text += f" | Bullet Stream: "
        if ship.bullet_stream_cooldown > 0:
            formatted_bullet_stream = f"{ship.bullet_stream_msg}{ship.bullet_stream_cooldown:.1f}/s"
            status_text += formatted_bullet_stream
        if ship.is_bullet_stream:
            formatted_bullet_stream_a = f"{ship.bullet_stream_msg}{ship.shot_timer_bypass:.1f}/s"
            status_text += formatted_bullet_stream_a
        if ship.bullet_stream_cooldown <= 0 and ship.is_bullet_stream == False:
            formatted_bullet_stream_b = f"{ship.bullet_stream_msg}"
            status_text += formatted_bullet_stream_b
        status_text += f" | Triple Shot: "
        if ship.tri_shot_cooldown > 0:
            formatted_tri_shot = f"{ship.tri_shot_msg}{ship.tri_shot_cooldown:.1f}/s"
            status_text += formatted_tri_shot
        if ship.is_tri_shot:
            formatted_tri_shot_a = f"{ship.tri_shot_msg}{ship.tri_shot_bypass:.1f}/s"
            status_text += formatted_tri_shot_a
        if ship.tri_shot_cooldown <= 0 and ship.is_tri_shot == False:
            formatted_tri_shot_b = f"{ship.tri_shot_msg}"
            status_text += formatted_tri_shot_b
        if ship.invincible_timer > 0:
            status_text += f" | Invincible for {formatted_timer}/s"
        return status_text
    
    def control_bar():
        return "Controls | Move: -W- -A- -S- -D- | Fire: -SPACEBAR- | Death Blossom: -F- | Bullet Stream: -V- THEN -SPACEBAR- | Triple Shot: -T-"

    def bottom_bar():
        return "Music and Sounds used with permission. See Readme.txt for license and author info"

    def diff_bar():
        if ship.current_diff == 1:
            return "Asteroid Spawn Rate: Press the Number key | Normal: -1- -ACTIVE- | Hard: -2- | I Want To Explode(PERMANENT): -5-"
        if ship.current_diff == 2:
            return "Asteroid Spawn Rate: Press the Number key | Normal: -1- | Hard: -2- -ACTIVE- | I Want To Explode(PERMANENT): -5-"
        if ship.current_diff == 5:
            return "Asteroid Spawn Rate: I Want to Explode: (-!-ACTIVE-!-)"

    #begin the main game Loop
    while running:
        for event in pygame.event.get():  #for loop that stops the process if the game windows gets closed
            if event.type == pygame.QUIT:
                print("Game Over!")
                print(f"Game Score: {score}")
                return
        
    
        screen.fill(SCREEN_COLOR)  #make the screen color black

        #Text bars get rendered here
        status = status_bar()
        status_render = font.render(status,True,(255,255,255))
        control = control_bar()
        control_render = medium_font.render(control,True, (255,255,255))
        bottom = bottom_bar()
        bottom_render = small_font.render(bottom, True, (255,255,255))
        screen.blit(status_render, (20,20))
        screen.blit(control_render, (20, 20 + font.get_linesize()))  # Position below first line
        diff = diff_bar()
        if ship.current_diff == 5:
            diff_render = medium_font.render(diff,True,GAMEOVER_COLOR)
        else:
            diff_render = medium_font.render(diff,True,(255,255,255))
        screen.blit(diff_render, (20, 20 + (font.get_linesize() * 2)))  # Position below second line
        screen.blit(bottom_render,(BOTTOM_BAR_LOC_X,BOTTOM_BAR_LOC_Y))
        pygame.display.flip()
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
                if ship.lives > 0:
                    ouch = pygame.mixer.Sound("lostlife.mp3")
                    pygame.mixer.Sound.play(ouch)
                    ship.lives -= 1
                    ship.invincible_timer = PLAYER_INVINCIBILITY_TIMER
                    ship.dead_timer = PLAYER_DEATH_TIMER
                    died = big_font.render(f"You Died! Extra Lives: {ship.lives}",True, GAMEOVER_COLOR)
                    screen.blit(died,(SCREEN_WIDTH//2 - pygame.Surface.get_width(died)//2, SCREEN_HEIGHT//2 - 50))
                    pygame.display.flip()
                else:
                    dead = pygame.mixer.Sound("gameover.mp3")
                    pygame.mixer.Sound.play(dead)
                    died = big_font.render(f"----GAME OVER ----",True, GAMEOVER_COLOR)
                    screen.blit(died,(SCREEN_WIDTH//2 - pygame.Surface.get_width(died)//2, SCREEN_HEIGHT//2 - 50))
                    pygame.display.flip()
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
                    if ship.lives > 0:
                        died = big_font.render(f"You Died! Extra Lives: {ship.lives}",True, GAMEOVER_COLOR)
                        screen.blit(died,(SCREEN_WIDTH//2 - pygame.Surface.get_width(died)//2, SCREEN_HEIGHT//2 - 50))
                        pygame.display.flip()
                    else:
                        died = big_font.render(f"----GAME OVER ----",True, GAMEOVER_COLOR)
                        screen.blit(died,(SCREEN_WIDTH//2 - pygame.Surface.get_width(died)//2, SCREEN_HEIGHT//2 - 50))
                        pygame.display.flip()
                    status = status_bar()
                    status_render = font.render(status,True,GAMEOVER_COLOR)
                    control = control_bar()
                    control_render = medium_font.render(control,True, GAMEOVER_COLOR)
                    bottom = bottom_bar()
                    bottom_render = small_font.render(bottom, True, GAMEOVER_COLOR)
                    screen.blit(status_render, (20,20))
                    screen.blit(control_render, (20, 20 + font.get_linesize()))  # Position below first line
                    diff = diff_bar()
                    diff_render = medium_font.render(diff,True,GAMEOVER_COLOR)
                    screen.blit(diff_render, (20, 20 + (font.get_linesize() * 2)))  # Position below second line
                    screen.blit(bottom_render,(BOTTOM_BAR_LOC_X,BOTTOM_BAR_LOC_Y))
                    pygame.display.flip()
                    
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
                if ship.lives > 0:
                    died = big_font.render(f"You Died! Extra Lives: {ship.lives}",True, GAMEOVER_COLOR)
                    screen.blit(died,(SCREEN_WIDTH//2 - pygame.Surface.get_width(died)//2, SCREEN_HEIGHT//2 - 50))
                    pygame.display.flip()
                else:
                    died = big_font.render(f"----GAME OVER ----",True, GAMEOVER_COLOR)
                    screen.blit(died,(SCREEN_WIDTH//2 - pygame.Surface.get_width(died)//2, SCREEN_HEIGHT//2 - 50))
                    pygame.display.flip()
                status = status_bar()
                status_render = font.render(status,True,GAMEOVER_COLOR)
                control = control_bar()
                control_render = medium_font.render(control,True, GAMEOVER_COLOR)
                bottom = bottom_bar()
                bottom_render = small_font.render(bottom, True, GAMEOVER_COLOR)
                screen.blit(status_render, (20,20))
                screen.blit(control_render, (20, 20 + font.get_linesize()))  # Position below first line
                diff = diff_bar()
                diff_render = medium_font.render(diff,True,GAMEOVER_COLOR)
                screen.blit(diff_render, (20, 20 + (font.get_linesize() * 2)))  # Position below second line
                screen.blit(bottom_render,(BOTTOM_BAR_LOC_X,BOTTOM_BAR_LOC_Y))
                pygame.display.flip()
                for drawable in drawable_group:
                    drawable.draw(screen, GAMEOVER_COLOR)
                pygame.display.flip()
                
                # Additional delay after shake effect
                pygame.time.delay(1500)
                if ship.lives > 0:
                    died = big_font.render(f"You Died! Extra Lives: {ship.lives}",True, GAMEOVER_COLOR)
                    screen.blit(died,(SCREEN_WIDTH//2 - pygame.Surface.get_width(died)//2, SCREEN_HEIGHT//2 - 50))
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    ship.reset()
                else:
                    died = big_font.render(f"----GAME OVER ----",True, GAMEOVER_COLOR)
                    screen.blit(died,(SCREEN_WIDTH//2 - pygame.Surface.get_width(died)//2, SCREEN_HEIGHT//2 - 50))
                    pygame.display.flip()
                    pygame.time.delay(2000)
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