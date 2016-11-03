import pygame
from random import *
from pygame.locals import *


class Blob(object):
    
    passes = 0
    
    def __init__(self, w, h, seeds, density):
    
        self.rect = [[0 for y in range(h)] for x in range(w)]
        
        size = w * h
        
        self.w = w
        self.h = h
        
        self.seeds = seeds * size
        self.density = density * size
        
        self.form_blob()
        
    def form_blob(self):
        
        self.seed_blob()
        self.grow_blob()
        
    def seed_blob(self):
        
        seeded = 0
        while seeded < self.seeds:
            Blob.passes += 1
            x, y = self.get_random_point()
            if self.rect[x][y] == 0:
                self.rect[x][y] = 1
                seeded += 1
                
    def grow_blob(self):
        
        grown = 0
        while grown < self.density:
            Blob.passes += 1
            x, y = self.get_random_point()
            if self.rect[x][y] == 0:
                grown += self.try_to_grow((x, y))
        
    def get_random_point(self):
    
        return randint(0, self.w - 1), randint(0, self.h - 1)
        
    def try_to_grow(self, (x, y)):
        
        growth = 0
        
        seeds = self.get_adj_seeds((x, y))
        
        chance = 0
        if seeds == 1:
            chance = 4
        elif seeds == 2:
            chance = 6
        elif seeds == 3:
            chance = 9
        elif seeds == 4:
            chance = 10
            
        c = randint(0, 9)
        if c < chance:
            self.rect[x][y] = 1
            growth = 1
        
        return growth
            
    def get_adj_seeds(self, (x, y)):
        
        seeds = 0
        dirs = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        for dx, dy in dirs:
            if dx > 0 and dx < self.w and dy >0 and dy < self.h:
                if self.rect[dx][dy] == 1:
                    seeds += 1
                    
        return seeds
            

def draw_blob(blob):
    
    pygame.display.set_mode((blob.w*5, blob.h*5))
    
    for y in range(blob.h):
        for x in range(blob.w):
            if blob.rect[x][y] == 1:
                draw_dot(x, y)
    
    pygame.display.update()


def draw_dot(x, y):

    s = pygame.display.get_surface()
    
    xcoord = x * 5
    ycoord = y * 5
    
    dot = pygame.Surface((5, 5))
    dot.fill((255, 0 , 0))
    dr = dot.get_rect()
    dr.topleft = (xcoord, ycoord)
    
    s.blit(dot, dr)
    
    
def handle_input():
    
    for event in pygame.event.get():
        if event.type == QUIT:
            exit() 
        
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
    
            
def main():

    pygame.init()

    b = Blob(20, 20, .01, .7)
    print Blob.passes
    
    draw_blob(b)

    while True:
        handle_input()
    
    # pygame.time.wait(2000)
    pygame.quit()
    

main()