import pygame
import sys, os
from pygame.locals import *
from constants import *

import tileset as ts
import font_draw as fd


class Gallery(object):

    def __init__(self):

        # self.tileset = ts.TerrainTileSet('cavern1')
        self.tileset = ts.TileSet('village_clutter')
        self.index = 0
        self.keys = self.tileset.keys
        self.images = self.tileset.tile_images

    def render(self):
        key = self.images[self.keys[self.index]]
        i, r = key.render()

        return i, r

    def current_key(self):

        return self.keys[self.index]

    def step(self):

        self.index += 1
        if self.index >= len(self.keys):
            self.index = 0


def set_screen():
    
    screen = pygame.display.set_mode((200, 200), HWSURFACE | DOUBLEBUF)
    pygame.display.set_caption('Oryx Demo')
    
    return screen
    
    
def handle_input(i):
        
    for event in pygame.event.get():
        if event.type == QUIT:
            exit() 
        
        elif event.type == KEYDOWN:
            i.step()
            if event.key == K_ESCAPE:
                exit()
        # other key presses here
        
        # mouse controls
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
    
    
def draw_demo(image, f):
        
    global screen
    
    screen.fill(BLUE)
    i, r = image.render()
    screen.blit(i, r)

    fi, fr = f.write(image.current_key(), RED)

    fr.topleft = (0, TILEHEIGHT)
    screen.blit(fi, fr)

    
def demo():
    
    global screen
    
    os.environ["SDL_VIDEO_CENTERED"] = '1'
    pygame.init()
    
    clock = pygame.time.Clock()
            
    screen = set_screen()

    g = Gallery()
    f = fd.FontDrawer()
        
    while True:
        
        draw_demo(g, f)
        handle_input(g)
        pygame.display.update()
        
        clock.tick(FPS)
    
    
if __name__ == '__main__':
   
    demo()
