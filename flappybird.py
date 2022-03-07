# importing modules
import pygame
import neat
import time
import os
import random

# window dimensions
WIN_WIDTH = 600
WIN_HEIGHT = 800

#bird frames
BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
] 
#transform.scale2x() -> doubles the size of the image
#image.load() -> loads the image to pygame
#os.path -> current path || join -> joins more path

#pipe images
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
#floor image
BASE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
#background image
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

class Bird:
    #"constants" of the class
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25 #degrees
    ROT_VEL = 5 #rotation velocity
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        #bird starting position
        self.x = x
        self.y = y

        self.tilt = 0
        self.tick_count = 0 #useful for physics in the game

        self.vel = 0 #velocity
        self.height = self.y
        self.img_count = 0 #index of the images
        self.img = self.IMGS[0] #current sprite

    def jump(self):
        self.vel = -10.5 #(0,0) coordinate is the top-left corner, so we need to have a negative velocity to get higher
        self.tick_count = 0 #tell when was our last jump
        self.height = self.y
    
    def move(self):
        pass