#import required modules
from asteroidfield import *


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
        self.invincible_timer = 0
    
    def shoot(self):
        bullet = Shot(self.position.x,self.position.y,SHOT_RADIUS)
        bullet.velocity = pygame.Vector2(0, 1)
        bullet.velocity.rotate_ip(self.rotation)
        bullet.velocity *= PLAYER_SHOOT_SPEED


    #define / overide update - makes ship go vroom
    def update(self, dt):
        if self.shot_timer > 0:
            self.shot_timer -= dt
        if self.invincible_timer > 0:   #Make the player invincibility timer tick down
            self.invincible_timer -= dt
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            if self.shot_timer <= 0:
                self.shoot()
                self.shot_timer = PLAYER_SHOOT_COOLDOWN
    
    #define / overide move - also makes ship go vroom
    def move(self,dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def reset(self):
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