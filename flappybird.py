# importing modules
import pygame
import neat
import time
import os
import random

# window dimensions
WIN_WIDTH = 500
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
        self.tick_count +=1 #how much we moved after the last jump

        d = self.vel * self.tick_count + 1.5*self.tick_count**2 #how many pixel we will be moving up or down

        if d >= 16: #terminal velocity
            d = 16
        if d < 0 :
            d -= 2
        
        self.y += d #moving up or down
        
        if d < 0 or self.y < self.height + 50: #when we have reached the top
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION #rotates the bird image
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
    
    def draw(self, win):
        self.img_count += 1
        
        #switching sprites
        if self.img_count <= self.ANIMATION_TIME:
            self.img =  self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
        
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt) #rotates the image based on the top left corner
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center) #rotates the image based on its center

        win.blit(rotated_image, new_rect.topleft) #draws image

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

def draw_window(win, bird): #draws the game window
    win.blit(BG_IMG, (0,0)) #draws backgroung
    bird.draw(win) #draw the bird
    pygame.display.update() #refresh the display

def main(): #runs the main loop of the game
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    isRunning = True
    
    clock = pygame.time.Clock() #sets the frame rate
    
    while isRunning:
        for event in pygame.event.get():
            #exiting the game loop for quitting pygame
            if event.type == pygame.QUIT:
                isRunning = False
        
        bird.move()
        draw_window(win, bird)
    
    #quitting pygame by clicking on the red X
    pygame.quit()
    quit()


main()