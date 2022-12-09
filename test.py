import pygame
import random
import time

# initialize pygame
pygame.init()

# set a display size
display_width = 800
display_height = 600
screen = pygame.display.set_mode((display_width, display_height))

# set title
pygame.display.set_caption("Random and Time Image with Random Animation")

# set a clock
clock = pygame.time.Clock()

# set colors
black = (0, 0, 0)
white = (255, 255, 255)

# set images
image1 = pygame.image.load("paper.png")
image2 = pygame.image.load("rock.png")
image3 = pygame.image.load("scisso.png")

# set image size
image1 = pygame.transform.scale(image1, (200, 200))
image2 = pygame.transform.scale(image2, (200, 200))
image3 = pygame.transform.scale(image3, (200, 200))

# define a function for random animation
def random_animation(x, y):
    pygame.draw.rect(screen, black, [x, y, 200, 200])
    pygame.display.update()
    time.sleep(1)
    pygame.draw.rect(screen, white, [x, y, 200, 200])
    pygame.display.update()
    time.sleep(1)
    pygame.draw.rect(screen, black, [x, y, 200, 200])
    pygame.display.update()
    time.sleep(1)
    pygame.draw.rect(screen, white, [x, y, 200, 200])
    pygame.display.update()


# set x and y for image
x = display_width * 0.2
y = display_height * 0.2

# set a boolean to control loop
done = False

# main loop
while not done:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # set random image
    random_image = random.choice([image1, image2, image3])

    # display image
    screen.blit(random_image, (x, y))
    pygame.display.update()

    # call the random animation function
    random_animation(x, y)

    # set a time for animation
    clock.tick(60)

# quit pygame
