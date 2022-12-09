from ast import While
from turtle import back, left
import pygame
from pygame.locals import *
import sys
import random
from tkinter import filedialog
from tkinter import *

pygame.init()  # Begin pygame
vec = pygame.math.Vector2
HEIGHT = 350
WIDTH = 700
ACC = 0.3
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0
hit_cooldown = pygame.USEREVENT + 1

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

# Run animation for right
run_ani_R = [
    pygame.image.load("Player_Sprite_R.png"),
    pygame.image.load("Player_Sprite2_R.png"),
    pygame.image.load("Player_Sprite3_R.png"),
    pygame.image.load("Player_Sprite4_R.png"),
    pygame.image.load("Player_Sprite5_R.png"),
    pygame.image.load("Player_Sprite6_R.png"),
    pygame.image.load("Player_Sprite_R.png"),
]
# Run animation for left
run_ani_L = [
    pygame.image.load("Player_Sprite_L.png"),
    pygame.image.load("Player_Sprite2_L.png"),
    pygame.image.load("Player_Sprite3_L.png"),
    pygame.image.load("Player_Sprite4_L.png"),
    pygame.image.load("Player_Sprite5_L.png"),
    pygame.image.load("Player_Sprite6_L.png"),
    pygame.image.load("Player_Sprite_L.png"),
]
# attack animation for right
att_ani_R = [
    pygame.image.load("Player_Sprite_R.png"),
    pygame.image.load("Player_Attack_R.png"),
    pygame.image.load("Player_Attack2_R.png"),
    pygame.image.load("Player_Attack3_R.png"),
    pygame.image.load("Player_Attack4_R.png"),
    pygame.image.load("Player_Attack5_R.png"),
    pygame.image.load("Player_Sprite_R.png"),
]
# attack animation for left
att_ani_L = [
    pygame.image.load("Player_Sprite_L.png"),
    pygame.image.load("Player_Attack_L.png"),
    pygame.image.load("Player_Attack2_L.png"),
    pygame.image.load("Player_Attack3_L.png"),
    pygame.image.load("Player_Attack4_L.png"),
    pygame.image.load("Player_Attack5_L.png"),
    pygame.image.load("Player_Sprite_L.png"),
]


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bgimage = pygame.image.load("Background.png")
        self.bgY = 0
        self.bgX = 0

    def render(self):
        displaysurface.blit(self.bgimage, (self.bgX, self.bgY))


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ground.png")
        self.rect = self.image.get_rect(center=(350, 350))
        self.bgX1 = 0
        self.bgY1 = 285

    def render(self):
        displaysurface.blit(self.image, (self.rect.x, self.rect.y))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player_Sprite_R.png")
        self.rect = self.image.get_rect()
        self.jumping = False
        self.running = False
        self.move_frame = 0
        self.attacking = False
        self.attack_frame = 0

        self.vx = 0
        self.pos = vec((340, 240))
        self.vel = vec((0, 0))
        self.acc = vec((0, 0))
        self.derection = "RIGHT"

    def move(self):
        self.acc = vec((0, 0.5))  # This line for gravity logic
        # Will set Running to False if the player has slow down to certain
        if abs(self.vel.x) > 0.03:
            self.running = True
        else:
            self.running = False
        # Retrun the current key presses
        pressed_key = pygame.key.get_pressed()
        # Accelerates the player in the direction of the key press
        if pressed_key[K_LEFT]:
            self.acc.x = -ACC
        if pressed_key[K_RIGHT]:
            self.acc.x = ACC

        # Formulas to calculate velocity while accounting for friction
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc  # Updates Position with new values
        # This causes characther warping from one point of the screen to the other
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos  # Update the rect with new

    def gravity_check(self):
        hits = pygame.sprite.spritecollide(player, ground_group, False)
        if self.vel.y > 0:
            if hits:
                loswest = hits[0]
                if self.pos.y < loswest.rect.bottom:
                    self.pos.y = loswest.rect.top + 1
                    self.vel.y = 0
                    self.jumping = False
        pass

    def update(self):
        # return to base frameif it at the end of the movement sequence
        if self.move_frame > 6:
            self.move_frame = 0
            return
        if self.jumping == False and self.running == True:
            if self.vel.x > 0:
                self.image = run_ani_R[self.move_frame]
                self.derection = "RIGHT"
            else:
                self.image = run_ani_L[self.move_frame]
                self.derection = "LEFT"
            self.move_frame += 1
        # return to base frame is standing still and incorrect frame is showing
        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.move_frame == "RIGHT":
                self.image = run_ani_R[self.move_frame]
            elif self.derection == "LEFT":
                self.image = run_ani_L[self.move_frame]
        pass

    def attack(self):
        # For attacking frame
        if self.attack_frame > 6:
            self.attack_frame = 0
            self.attacking = False

        # for directiong control animation
        if self.derection == "RIGHT":
            self.image = att_ani_R[self.attack_frame]
        elif self.derection == "LEFT":
            self.correction()
            self.image = att_ani_L[self.attack_frame]
        self.attack_frame += 1
        pass

    def correction(self):
        # Function is used to correct an error
        # with character position on left attack frames
        if self.attack_frame == 1:
            self.pos.x -= 20
        if self.attack_frame == 6:
            self.pos.x += 20

    def jump(self):
        self.rect.x += 1

        # check to see if the player is in contact with the ground
        hits = pygame.sprite.spritecollide(self, ground_group, False)

        self.rect.x -= 1

        # If touching the ground,and not currenty jumping ,couse the player to jump
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12

        pass


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.derection = random.randint(0, 1)  # 0 for Right, 1 for left
        self.vel.x = (
            random.randint(2, 6) / 2
        )  # for randomized velocity this will be generated

        if self.derection == 0:
            self.pos.x = 0
            self.pos.y = 235
        if self.derection == 1:
            self.pos.x = 700
            self.pos.y = 235

    def move(self):
        # this will be cause the enemy to change direction up to reaching the end of screen
        if self.pos.x >= (WIDTH - 20):
            self.derection = 1
        elif self.pos.x <= 0:
            self.derection = 0
        # Update position with new value
        if self.derection == 0:
            self.pos.x += self.vel.x
        if self.derection == 1:
            self.pos.x -= self.vel.x
        self.rect.center = self.pos  # Update the rect with new

    def render(self):
        # dissplay the enemy on screen
        displaysurface.blit(self.image, (self.pos.x, self.pos.y))

    def update(self):
        # check for collition with player
        hits = pygame.sprite.spritecollide(self, Playergroup, False)
        # activate upon either of two expressions is true
        if hits and player.attack == True:
            self.kill()  # print kill
        elif hits and player.attacking == False:
            player_hit()


background = Background()
ground = Ground()
ground_group = pygame.sprite.Group()
ground_group.add(ground)
player = Player()
enemy = Enemy()
while True:
    player.gravity_check()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
        if event.type == pygame.KEYDOWN:
            pass
        # for jumping
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            # for attaking
            if event.key == pygame.K_RETURN:
                if player.attacking == False:
                    player.attack()
                    player.attacking = True

    background.render()
    ground.render()

    player.update()
    if player.attacking == True:
        player.attack()
    player.move()

    displaysurface.blit(player.image, player.rect)
    enemy.render()
    enemy.move()
    pygame.display.update()
    FPS_CLOCK.tick(FPS)
