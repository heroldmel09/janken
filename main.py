from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time
import cv2
from cvzone.ClassificationModule import Classifier
import pygame
import sys
import random
import time

pygame.init()

hieght = 500
width = 730
display = pygame.display.set_mode((width, hieght))
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

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

offset = 20
imgSize = 300
classifier = Classifier("model/keras_model.h5", "model/labels.txt")
labels = ["rock", "paper", "scissor"]
folder = "data/paper"
counter = 0


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
        return self.key

    def user(self):
        while True:
            success, img = cap.read()
            imgOutput = img.copy()
            hands, img = detector.findHands(img)
            if hands:
                hand = hands[0]
                x, y, w, h = hand["bbox"]

                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
                imgCrop = img[y - offset : y + h + offset, x - offset : x + w + offset]

                imgCropShape = imgCrop.shape

                aspectRatio = h / w

                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    imgResizeShape = imgResize.shape
                    wGap = math.ceil((imgSize - wCal) / 2)
                    imgWhite[:, wGap : wCal + wGap] = imgResize
                    prediction, index = classifier.getPrediction(imgWhite, draw=False)
                    print(prediction, index)

                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    imgResizeShape = imgResize.shape
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap : hCal + hGap, :] = imgResize
                    prediction, index = classifier.getPrediction(imgWhite, draw=False)

                cv2.rectangle(
                    imgOutput,
                    (x - offset, y - offset - 50),
                    (x - offset + 90, y - offset - 50 + 50),
                    (255, 0, 255),
                    cv2.FILLED,
                )
                cv2.putText(
                    imgOutput,
                    labels[index],
                    (x, y - 26),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1.7,
                    (255, 255, 255),
                    2,
                )
                return labels[index]
                cv2.rectangle(
                    imgOutput,
                    (x - offset, y - offset),
                    (x + w + offset, y + h + offset),
                    (255, 0, 255),
                    4,
                )
            if time.time() - self.start < self.time:
                break


animation = Animation()
score = [0, 0]
while True:
    print("computer" + animation.render())
    print("user" + animation.user())
    user = animation.user()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if user == animation.render():
            print("It's a tie!")
        elif user == "rock":
            if animation.render() == "paper":
                score[1] += 1
                print("Computer Wins!")
            elif animation.render() == "scissor":
                score[0] += 1
                print("You Win!")
        elif user == "paper":
            if animation.render() == "rock":
                score[0] += 1
                print("You Win!")
            elif animation.render() == "scissor":
                score[1] += 1
                print("Computer Wins!")
        elif user == "scissor":
            if animation.render() == "rock":
                score[1] += 1
                print("Computer Wins!")
            elif animation.render() == "paper":
                score[0] += 1
                print("You Win!")

    pygame.display.update()
    clock.tick(60)

    cv2.waitKey(1)
