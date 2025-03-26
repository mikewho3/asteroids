#import required modules
import pygame
from constants import *
from circleshape import *
import gamestate
#Create the Shot Class - parent is CircleShape
class Shot(CircleShape):
    def __init__(self, x, y, radius):  #initialize
        super().__init__(x,y,radius)  #initialize parent CircleShape - Required to draw and update asteroids!
        self.x = x
        self.y = y
        self.position = pygame.Vector2(self.x,self.y)
        self.radius = radius
        self.lifespan = SHOT_LIFESPAN


    def draw(self,screen,color):
        self.color = color
        pygame.draw.circle(screen,self.color,(self.position.x,self.position.y),self.radius,width=2)
    
    def update(self,dt):
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt
        self.lifespan -= dt
        if self.lifespan <=0:
            self.kill()


#Create the Player Class - parent is CircleShape
class Player(CircleShape):
    def __init__(self,x,y):  #initialize
        super().__init__(x,y,PLAYER_RADIUS)  #call parent initialize - required for draw/update
        self.rotation = 0
        self.shot_timer = 0
        self.dead_timer = 1.2
        self.lives = PLAYER_STARTING_LIVES
        self.is_spinning = False
        self.spin_start_angle = 0
        self.current_spin_angle = 0
        self.spin_cooldown = 0
        self.spin_cooldown_max = DEATH_FLOWER_COOLDOWN  
        self.death_flower = "Available!"
        self.bullet_stream_cooldown = 0
        self.invincible_timer = 0
        self.sound_delay_cooldown = 0
        self.shot_timer_bypass = 0
        self.bullet_stream_msg = "Available!"
        self.is_bullet_stream = False
        self.is_tri_shot = False
        self.tri_shot_bypass = 0
        self.tri_shot_cooldown = 0
        self.tri_shot_msg = "Available!"
        self.current_diff = 1
        self.key_lock = 0

    def start_spinning_attack(self, shot_group):
        if self.spin_cooldown <= 0 and not self.is_spinning:
            self.is_spinning = True
            self.spin_start_angle = self.rotation
            self.current_spin_angle = 0
            self.bullet_group = shot_group
            self.dead_timer = 1.5
            self.invincible_timer = PLAYER_INVINCIBILITY_TIMER - 3.0

    def tri_shot(self):
        self.tri_shot_bypass = TRI_SHOT_DURATION
        self.is_tri_shot = True
    
    def shoot(self):
        bullet = Shot(self.position.x,self.position.y,SHOT_RADIUS)
        bullet.velocity = pygame.Vector2(0, 1)
        bullet.velocity.rotate_ip(self.rotation)
        bullet.velocity *= PLAYER_SHOOT_SPEED
        if self.is_tri_shot and self.is_spinning == False and self.is_bullet_stream == False:
            #TriShot if True
            bullet_b = Shot(self.position.x,self.position.y,SHOT_RADIUS)
            bullet_b.velocity = pygame.Vector2(0, 1)
            bullet_b.velocity.rotate_ip(self.rotation - TRI_SHOT_ROTATION)
            bullet_b.velocity *= PLAYER_SHOOT_SPEED
            bullet_c = Shot(self.position.x,self.position.y,SHOT_RADIUS)
            bullet_c.velocity = pygame.Vector2(0, 1)
            bullet_c.velocity.rotate_ip(self.rotation + TRI_SHOT_ROTATION)
            bullet_c.velocity *= PLAYER_SHOOT_SPEED
        laser = pygame.mixer.Sound("laser.mp3")
        pygame.mixer.Sound.set_volume(laser,0.6)
        pygame.mixer.Sound.play(laser)
    
    def bullet_stream(self):
        self.shot_timer_bypass = BULLET_STREAM_DURATION
        self.is_bullet_stream = True
        
        #Old Code, saved for reasons.
        #bullet_amount = BULLET_STREAM_AMOUNT
        #for X in range(bullet_amount, 0, -1):
        #    shoot = Shot(self.position.x,self.position.y,SHOT_RADIUS)
        #    shoot.velocity = pygame.Vector2(0, 1)
        #    shoot.velocity.rotate_ip(self.rotation)
        #    shoot.velocity *= PLAYER_SHOOT_SPEED
        #    laser = pygame.mixer.Sound("laser.mp3")
        #    pygame.mixer.Sound.play(laser)
        #    pygame.display.flip()
        #    pygame.time.delay(BULLET_STREAM_DELAY)

    #define / overide update - makes ship go vroom
    def update(self, dt):

        #Updates and Timers run here

        #Basic Shooting Timer
        if self.shot_timer > 0:
            self.shot_timer -= dt
        #Sound Delay So we arent spamming sounds
        if self.sound_delay_cooldown > 0:
            self.sound_delay_cooldown -= dt
        #Invincibility Timer
        if self.invincible_timer > 0:   #Make the player invincibility timer tick down
            self.invincible_timer -= dt
        #Controls Lockout Timer
        if self.dead_timer > 0:   #Make the player death timer tick down
            self.dead_timer -= dt
        #Key lock timer to prevent double press
        if self.key_lock > 0:
            self.key_lock -= dt
        if gamestate.key_lock > 0:
            gamestate.key_lock -= dt
        if gamestate.key_lock_1 > 0:
            gamestate.key_lock_1 -= dt
        if gamestate.key_lock_2 > 0:
            gamestate.key_lock_2 -= dt
        if gamestate.key_lock_5 > 0:
            gamestate.key_lock_5 -= dt
        if gamestate.key_lock_kp_enter > 0:
            gamestate.key_lock_kp_enter -= dt
        if gamestate.key_lock_kp_plus > 0:
            gamestate.key_lock_kp_plus -= dt
        #Death Blossom Cooldown Timer
        if self.spin_cooldown > 0:
            if self.dead_timer > 0:
                pass
            else:
                self.spin_cooldown -= dt
        #Death Blossom Message Control
        if self.spin_cooldown > 0:
            self.death_flower = "Cooldown: "
        else:
            self.death_flower = "Available!"
        
        #Bullet Stream Message Control
        if self.bullet_stream_cooldown > 0:  
            self.bullet_stream_msg = "Cooldown: "
        elif self.shot_timer_bypass > 0:
            self.bullet_stream_msg = "-ACTIVE-: "
        else:
            self.bullet_stream_msg = "Available!"
        #TriShot Message Control
        if self.tri_shot_cooldown > 0:  
            self.tri_shot_msg = "Cooldown: "
        elif self.tri_shot_bypass > 0:
            self.tri_shot_msg = "-ACTIVE-: "
        else:
            self.tri_shot_msg = "Available!"
        #Bullet Stream Timers and Cooldown
        if self.is_bullet_stream:
            if self.shot_timer_bypass > 0:
                if self.dead_timer > 0:
                    pass
                else:
                    self.shot_timer_bypass -= dt
            if self.shot_timer_bypass <= 0 and self.is_bullet_stream:
                self.is_bullet_stream = False
                self.shot_timer_bypass = 0
                self.bullet_stream_cooldown = BULLET_STREAM_COOLDOWN
        if self.bullet_stream_cooldown > 0:
            if self.dead_timer > 0:
                pass
            else:
                self.bullet_stream_cooldown -= dt
        #TriShot Timers and Cooldown
        if self.is_tri_shot:
            if self.tri_shot_bypass > 0:
                if self.dead_timer > 0:
                    pass
                else:
                    self.tri_shot_bypass -= dt
            if self.tri_shot_bypass <= 0 and self.is_tri_shot:
                self.is_tri_shot = False
                self.tri_shot_bypass = 0
                self.tri_shot_cooldown = TRI_SHOT_COOLDOWN
        if self.tri_shot_cooldown > 0:
            if self.dead_timer > 0:
                pass
            else:
                self.tri_shot_cooldown -= dt
        #Death Blossom Active and In Progress in this timer
        if self.is_spinning:
            self.update_spinning_attack()

        #Begin Keypress Detection

        keys = pygame.key.get_pressed()

        #Debug Controls
        if keys[pygame.K_KP_ENTER]:
            if gamestate.key_lock_kp_enter <= 0:
                gamestate.key_lock_kp_enter = 1
                print(f"DEBUG: Current asteroid_spawn_rate = {gamestate.asteroid_spawn_rate}")
        if keys[pygame.K_KP_PLUS]:
            if gamestate.key_lock_kp_plus <= 0:
                gamestate.key_lock_kp_plus = 1
                print(f"DEBUG: Current Player Values")
                print(f"----------------------------")
                print(f"self.position = {self.position}")
                print(f"self.radius = {self.radius}")
                print(f"self.rotation = {self.rotation}")
                print(f"self.lives = {self.lives}")
                print(f"(deathblossom)self.is_spinning = {self.is_spinning}")
                print(f"self.is_bullet_stream = {self.is_bullet_stream}")
                print(f"self.is_tri_shot = {self.is_tri_shot}")
                print(f"self.current_diff = {self.current_diff}")
        
        #Difficulty Controls
        if keys[pygame.K_1]:
            if self.dead_timer > 0 or self.key_lock > 0 or gamestate.key_lock_1 > 0:
                return
            else:
                if self.current_diff != 1 and self.current_diff != 5:
                    #print(f"DEBUG: attempting to change asteroid_spawn_rate to = 1")
                    gamestate.key_lock_1 = 1
                    self.current_diff = 1
                    gamestate.asteroid_spawn_rate = 0.8
                    self.sound_delay_cooldown = SOUND_DELAY
                    self.key_lock = KEY_LOCK_TIMER
                    
                    #print(f"DEBUG: Spawn Rate={gamestate.asteroid_spawn_rate} | self.current_diff={self.current_diff}")
                else:
                    if gamestate.key_lock_1 <= 0:
                        gamestate.key_lock_1 = 1
                        error_sound = pygame.mixer.Sound("error.mp3")
                        pygame.mixer.Sound.play(error_sound, maxtime=1500)
                        self.sound_delay_cooldown = SOUND_DELAY
        if keys[pygame.K_2]:
            if self.dead_timer > 0 or self.key_lock > 0 or gamestate.key_lock_2 > 0:
                return
            else:
                if self.current_diff != 2 and self.current_diff != 5:
                    #print(f"DEBUG: attempting to change asteroid_spawn_rate to = 0.7")
                    gamestate.key_lock_2 = 1
                    self.current_diff = 2
                    gamestate.asteroid_spawn_rate = 0.5
                    self.sound_delay_cooldown = SOUND_DELAY
                    self.key_lock = KEY_LOCK_TIMER

                    #print(f"DEBUG: Spawn Rate={gamestate.asteroid_spawn_rate} | self.current_diff={self.current_diff}")
                else:
                    if gamestate.key_lock_2 <= 0:
                        gamestate.key_lock_2 = 1
                        error_sound = pygame.mixer.Sound("error.mp3")
                        pygame.mixer.Sound.play(error_sound, maxtime=1500)
                        self.sound_delay_cooldown = SOUND_DELAY
        if keys[pygame.K_5]:
            if self.dead_timer > 0 or self.key_lock > 0 or gamestate.key_lock_5 > 0:
                return
            else:
                if self.current_diff != 5:
                    #print(f"DEBUG: attempting to change asteroid_spawn_rate to = 0.1 HARDCORE")
                    gamestate.key_lock_5 = 1
                    self.current_diff = 5
                    gamestate.asteroid_spawn_rate = 0.1
                    self.invincible_timer = 8
                    self.lives = 0
                    self.sound_delay_cooldown = SOUND_DELAY
                    self.key_lock = KEY_LOCK_TIMER
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    big_font = pygame.font.Font(None, 38)
                    warning = big_font.render("-!-WARNING-!- Incoming Asteroid Storm -!-WARNING-!-",True, GAMEOVER_COLOR)
                    warning_2 = big_font.render("Your Extra Ships Were Destroyed In The Storm",True, GAMEOVER_COLOR)
                    screen.blit(warning,(SCREEN_WIDTH//2 - pygame.Surface.get_width(warning)//2, SCREEN_HEIGHT//2 - 50))
                    screen.blit(warning_2,(SCREEN_WIDTH//2 - pygame.Surface.get_width(warning)//2 + 50, SCREEN_HEIGHT//2 - 50 + big_font.get_linesize()))
                    pygame.display.flip()
                    pygame.time.delay(5000)
                    

                    #print(f"DEBUG: Spawn Rate={gamestate.asteroid_spawn_rate} | self.current_diff={self.current_diff}")
                else:
                    if gamestate.key_lock_5 <= 0:
                        gamestate.key_lock_5 = 1
                        error_sound = pygame.mixer.Sound("error.mp3")
                        pygame.mixer.Sound.play(error_sound, maxtime=1500)
                        self.sound_delay_cooldown = SOUND_DELAY
                    





        if keys[pygame.K_a]:
            if self.dead_timer > 0:
                return
            else:
                self.rotate(-dt)
        if keys[pygame.K_d]:
            if self.dead_timer > 0:
                return
            else:
                self.rotate(dt)
        if keys[pygame.K_w]:
            if self.dead_timer > 0:
                return
            else:
                self.move(dt)
        if keys[pygame.K_s]:
            if self.dead_timer > 0:
                return
            else:
                self.move(-dt)
        if keys[pygame.K_SPACE]:  #Shoot
            if self.dead_timer > 0:
                return
            elif self.is_bullet_stream and self.shot_timer <= 0:
                self.shoot()
                self.shot_timer = 0.1
            elif self.shot_timer <= 0:
                self.shoot()
                self.shot_timer = PLAYER_SHOOT_COOLDOWN
        if keys[pygame.K_f]:  #Death Blossom
            if self.dead_timer > 0:
                return
            elif self.spin_cooldown > 0:
                if self.sound_delay_cooldown > 0:
                    return
                else:
                    error_sound = pygame.mixer.Sound("error.mp3")
                    pygame.mixer.Sound.play(error_sound, maxtime=1500)
                    self.sound_delay_cooldown = SOUND_DELAY
            else:
                self.start_spinning_attack(shot_group)
                power_up_sound = pygame.mixer.Sound("powerup.mp3")
                pygame.mixer.Sound.play(power_up_sound, maxtime=1500)
                self.sound_delay_cooldown = SOUND_DELAY
        if keys[pygame.K_v]:  #Bullet Stream
            if self.dead_timer > 0:
                return
            elif self.bullet_stream_cooldown > 0 or self.shot_timer_bypass > 0:
                if self.sound_delay_cooldown > 0:
                    return
                else:
                    error_sound = pygame.mixer.Sound("error.mp3")
                    pygame.mixer.Sound.play(error_sound, maxtime=1500)
                    self.sound_delay_cooldown = SOUND_DELAY
            else:
                self.bullet_stream()
                power_up_sound = pygame.mixer.Sound("powerup.mp3")
                pygame.mixer.Sound.play(power_up_sound, maxtime=1500)
                self.sound_delay_cooldown = SOUND_DELAY
        if keys[pygame.K_t]:  #TriShot
            if self.dead_timer > 0:
                return
            elif self.tri_shot_cooldown > 0 or self.tri_shot_bypass > 0 or self.is_bullet_stream:
                if self.sound_delay_cooldown > 0:
                    return
                else:
                    error_sound = pygame.mixer.Sound("error.mp3")
                    pygame.mixer.Sound.play(error_sound, maxtime=1500)
                    self.sound_delay_cooldown = SOUND_DELAY
            else:
                self.tri_shot()
                power_up_sound = pygame.mixer.Sound("powerup.mp3")
                pygame.mixer.Sound.play(power_up_sound, maxtime=1500)
                self.sound_delay_cooldown = SOUND_DELAY

    
    def update_spinning_attack(self):
        # Constants
        full_rotation = 720
        degrees_per_bullet = 45
        rotation_speed = 15  # Adjust for desired speed
        
        # Calculate next angle
        prev_angle = self.current_spin_angle
        self.current_spin_angle += rotation_speed
        
        # Update ship angle
        self.rotation = (self.spin_start_angle + self.current_spin_angle) % 720

        # Check if we should fire bullets
        # This checks all 4-degree marks we passed in this frame
        for angle in range(int(prev_angle) // degrees_per_bullet * degrees_per_bullet, 
                        int(self.current_spin_angle) // degrees_per_bullet * degrees_per_bullet + 1, 
                        degrees_per_bullet):
            if angle <= full_rotation:
                self.shoot()
        
        # Check if we've completed a full rotation
        if self.current_spin_angle >= full_rotation:
            self.is_spinning = False
            self.spin_cooldown = self.spin_cooldown_max



    #define / overide move - also makes ship go vroom
    def move(self,dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def reset(self):
        self.dead_timer = PLAYER_DEATH_TIMER
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.velocity_x = 0
        self.velocity_y = 0
        self.position = pygame.Vector2(self.x,self.y)


    #define / overide rotate - still helps make the ship go vroom
    def rotate(self,dt):
        self.rotation += (PLAYER_TURN_SPEED*dt)
    
    #makes the ship a triangle
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    #draws the ship on the screen
    def draw(self,screen,color):
        self.color = color  #makes the color white - I found I can also do this by replacing color with [255,255,255]
        pygame.draw.polygon(screen,self.color,self.triangle(),2)
    