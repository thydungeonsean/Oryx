import pygame
import sys, os
from pygame.locals import *
from constants import *


def set_screen():
    
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), HWSURFACE | DOUBLEBUF)
    pygame.display.set_caption('Oryx Demo')
    
    return screen
    
    
def handle_input():
        
        for event in pygame.event.get():
            if event.type == QUIT:
                exit() 
            
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
            # other key presses here
            
            # mouse controls
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
    
    
def draw_demo():
        
    pass

    
def demo():
    
    os.environ["SDL_VIDEO_CENTERED"] = '1'
    pygame.init()
    
    clock = pygame.time.Clock()
            
    screen = set_screen()

        
    while True:
        
        draw_demo()
        handle_input()
        pygame.display.update()
        
        clock.tick(FPS)
    
    
if __name__ == '__main__':
   
    demo()
    