import pygame
import components
import NN
import population
import os

pygame.init()

win_width=432
win_height=768

gap=150

bg=pygame.transform.scale(pygame.image.load(os.path.join("assets/background-day.png")),(win_width,win_height))
ground=pygame.transform.scale(pygame.image.load(os.path.join("assets/base.png")),(win_width,112*1.5))

topImg=pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join("assets/pipe-green.png")),(52,550)),True,True)
bottomImg=pygame.transform.scale(pygame.image.load(os.path.join("assets/pipe-green.png")),(52,550))

birdUp=pygame.image.load(os.path.join("assets/yellowbird-upflap.png"))
birdMid=pygame.image.load(os.path.join("assets/yellowbird-midflap.png"))
birdDown=pygame.image.load(os.path.join("assets/yellowbird-downflap.png"))

window=pygame.display.set_mode((win_width,win_height))



ground=components.Ground(win_height)
font = pygame.font.Font('freesansbold.ttf', 32)

brains=[]

pipes=[]

pipes.append(components.Pipes())

