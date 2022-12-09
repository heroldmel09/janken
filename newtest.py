import pygame
import random
import time
import sys


pygame.init()

hieght = 500
width = 730
display = pygame.display.set_mode((width, hieght))
image1 = pygame.image.load("paper.png")
image2 = pygame.image.load("rock.png")
image3 = pygame.image.load("scisso.png")

# set image size
image1 = pygame.transform.scale(image1, (200, 200))
image2 = pygame.transform.scale(image2, (200, 200))
image3 = pygame.transform.scale(image3, (200, 200))
janken = [image1, image2, image3]
clock = pygame.time.Clock()


class Animetion(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.locx = 200
        self.locy = 200
        self.time = 10

    def render(self):
        while self.time:
            self.rand_pic = random.choice(janken)
            display.blit(self.rand_pic, (self.locx, self.locy))
            pygame.display.update()
            time.sleep(1)
            self.time -= 1


animetion = Animetion()
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    animetion.render()
    pygame.display.update()
    clock.tick(60)
