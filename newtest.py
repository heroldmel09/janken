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
janken = {"paper": image1, "rock": image2, "scissor": image3}
clock = pygame.time.Clock()


class Animation(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.locx = 200
        self.locy = 200
        self.time = 3
        self.speed = 0.30 / len(janken)
        self.start = time.time()

    def render(self):
        while time.time() - self.start < self.time:
            self.key, self.value = random.choice(list(janken.items()))
            # screen display
            display.blit(self.value, (self.locx, self.locy))
            pygame.display.update()
        return print(self.key)


animation = Animation()
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    animation.render()
    pygame.display.update()
    clock.tick(60)
