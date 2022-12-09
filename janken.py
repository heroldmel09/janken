import pygame
import sys
from pygame.locals import *
import random
from random import randint


pygame.init()
WIDTH = 750
HEIGHT = 350

display = pygame.display.set_mode((WIDTH, HEIGHT))
images = ["rock.png", "paper.png", "scisso.png"]
random_number = randint(0, len(images) - 1)

# Load the randomly chosen image
image = pygame.image.load(images[random_number])

# Define a list of animations
animations = [pygame.transform.rotate, pygame.transform.flip, pygame.transform.scale]

# Generate a random number
random_number = randint(0, len(animations) - 1)

# Apply the randomly chosen animation to the image
image = animations[random_number](image, 3)

# Draw the image to the screen
display.blit(image, (0, 0))

# Update the window
pygame.display.update()


pygame.display.set_caption("jankentest")
while True:
    events = pygame.event.get()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
