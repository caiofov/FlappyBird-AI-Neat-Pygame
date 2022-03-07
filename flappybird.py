# importing modules
import pygame
import neat
import time
import os
import random

pygame.font.init() #inits the font

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
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
#background image
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))


STAT_FONT = pygame.font.SysFont("comicsans", 50) #font for score


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
        #mask -> list os pixels of an image
        return pygame.mask.from_surface(self.img)



class Pipe:
    GAP = 200
    VEL = 3

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True) #flips the image to get the pipe on the top
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450) #gets a random number to set height
        self.top = self.height - self.PIPE_TOP.get_height() #coordinate of the top pipe to be drawn
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL #moves the pipe to the left
    
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        #setting masks
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        #distance between elements
        top_offset = (self.x - bird.x, self.top - round(bird.y)) 
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        #checking if they collide
        #if don't collide -> return None
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True #collides

        return False 



class Base:
    VEL = 3
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG
    
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        #when an image is completely out of the screen, we must put this image right before the other one
        if self.x1 + self.WIDTH < 0: 
            self.x1 = self.x2 + self.WIDTH
        
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, bird, pipes, base, score): #draws the game window
    win.blit(BG_IMG, (0,0)) #draws backgroung

    for pipe in pipes: #draws all the pipes
        pipe.draw(win)
    base.draw(win) #draws the floor
    bird.draw(win) #draw the bird
    
    #draws the score
    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    pygame.display.update() #refresh the display

def main(): #runs the main loop of the game
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    isRunning = True
    score = 0
    add_pipe = False
    
    clock = pygame.time.Clock() #sets the frame rate
    
    while isRunning:
        for event in pygame.event.get():
            #exiting the game loop for quitting pygame
            if event.type == pygame.QUIT:
                isRunning = False
        
        # bird.move()
        base.move()

        rem = [] #list of pipes to be removed of the actual list
        
        for pipe in pipes:
            if pipe.collide(bird): #checks collision
                pass
            
            if pipe.x +pipe.PIPE_TOP.get_width() < 0: #checks if the pipe is out of the screen
                rem.append(pipe) #pipe to be removed
            
            if not pipe.passed and pipe.x < bird.x: #tells the bird has passed the pipe
                pipe.passed = True
                add_pipe = True

            pipe.move()

        if add_pipe: #adds a new pipe to the pipe list
            score += 1
            pipes.append(Pipe(600))
            add_pipe = False

        for r in rem: #removes the passed pipes
            pipes.remove(r)
        
        draw_window(win, bird, pipes, base, score)

        if bird.y + bird.img.get_height() >= 730: #hit the floor
            pass

    #quitting pygame by clicking on the red X
    pygame.quit()
    quit()


main()