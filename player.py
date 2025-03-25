#import required modules
import pygame
from circleshape import *


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
        self.is_spinning = False
        self.spin_start_angle = 0
        self.current_spin_angle = 0
        self.spin_cooldown = 0
        self.spin_cooldown_max = DEATH_FLOWER_COOLDOWN  
        self.death_flower = "Available!"
        self.bullet_stream_cooldown = 0
        self.invincible_timer = 0
        self.sound_delay_cooldown = 0

    def start_spinning_attack(self, shot_group):
        if self.spin_cooldown <= 0 and not self.is_spinning:
            self.is_spinning = True
            self.spin_start_angle = self.rotation
            self.current_spin_angle = 0
            self.bullet_group = shot_group
            self.dead_timer = 1.5
            self.invincible_timer = PLAYER_INVINCIBILITY_TIMER - 3.0
    
    def shoot(self):
        bullet = Shot(self.position.x,self.position.y,SHOT_RADIUS)
        bullet.velocity = pygame.Vector2(0, 1)
        bullet.velocity.rotate_ip(self.rotation)
        bullet.velocity *= PLAYER_SHOOT_SPEED
        laser = pygame.mixer.Sound("laser.mp3")
        pygame.mixer.Sound.play(laser)
    
    def bullet_stream(self):
        bullet_amount = BULLET_STREAM_AMOUNT
        for X in range(bullet_amount, 0, -1):
            shoot = Shot(self.position.x,self.position.y,SHOT_RADIUS)
            shoot.velocity = pygame.Vector2(0, 1)
            shoot.velocity.rotate_ip(self.rotation)
            shoot.velocity *= PLAYER_SHOOT_SPEED
            laser = pygame.mixer.Sound("laser.mp3")
            pygame.mixer.Sound.play(laser)
            pygame.display.flip()
            pygame.time.delay(BULLET_STREAM_DELAY)

    #define / overide update - makes ship go vroom
    def update(self, dt):
        if self.shot_timer > 0:
            self.shot_timer -= dt
        if self.sound_delay_cooldown > 0:
            self.sound_delay_cooldown -= dt
        if self.invincible_timer > 0:   #Make the player invincibility timer tick down
            self.invincible_timer -= dt
        if self.dead_timer > 0:   #Make the player death timer tick down
            self.dead_timer -= dt
        if self.spin_cooldown > 0:
            self.spin_cooldown -= dt
        if self.spin_cooldown > 0:
            self.death_flower = "Cooldown: "
        else:
            self.death_flower = "Available!"
        if self.bullet_stream_cooldown > 0:
            self.bullet_stream_cooldown -= dt
        if self.is_spinning:
            self.update_spinning_attack()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self.dead_timer > 0:
                pass
            else:
                self.rotate(-dt)
        if keys[pygame.K_d]:
            if self.dead_timer > 0:
                pass
            else:
                self.rotate(dt)
        if keys[pygame.K_w]:
            if self.dead_timer > 0:
                pass
            else:
                self.move(dt)
        if keys[pygame.K_s]:
            if self.dead_timer > 0:
                pass
            else:
                self.move(-dt)
        if keys[pygame.K_SPACE]:
            if self.dead_timer > 0:
                pass
            elif self.shot_timer <= 0:
                self.shoot()
                self.shot_timer = PLAYER_SHOOT_COOLDOWN
        if keys[pygame.K_f]:
            if self.dead_timer > 0:
                pass
            elif self.spin_cooldown > 0:
                if self.sound_delay_cooldown > 0:
                    pass
                else:
                    error_sound = pygame.mixer.Sound("error.mp3")
                    pygame.mixer.Sound.play(error_sound, maxtime=1500)
                    self.sound_delay_cooldown = SOUND_DELAY
            else:
                self.start_spinning_attack(shot_group)
        if keys[pygame.K_SPACE] and keys[pygame.K_LSHIFT]:
            if self.dead_timer > 0:
                pass
            elif self.bullet_stream_cooldown > 0:
                if self.sound_delay_cooldown > 0:
                    pass
                else:
                    error_sound = pygame.mixer.Sound("error.mp3")
                    pygame.mixer.Sound.play(error_sound, maxtime=1500)
                    self.sound_delay_cooldown = SOUND_DELAY
            else:
                self.bullet_stream()
                self.bullet_stream_cooldown = BULLET_STREAM_COOLDOWN

    
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