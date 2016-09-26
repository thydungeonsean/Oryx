import pygame
from pygame.locals import *
from colours import *
from random import *
from color_change import color_change
import spritesheet
import sys
import frag


def set_screen():
    
    global SCREENWIDTH, SCREENHEIGHT, SCREEN, buffer, br
    
    pygame.init()
    
    SCREENWIDTH = 800
    SCREENHEIGHT = 600
    
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), HWSURFACE|DOUBLEBUF)
    SCREEN.fill(BLACK)
    
    buffer = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
    br = buffer.get_rect()
    buffer.fill(WHITE)
    buffer.convert()
    
    pygame.display.set_caption('Oryx')


def set_images():
    
    global tile, tr, wall, wr, man, manRect
    global player, pf, pfr
    
    key = {'man': (0, 0), 'guy': (0, 1)}
    key2 = {'wall': (0, 1), 'tile': (9, 0)}
    
    player = spritesheet.SpriteSheet('players', key, 16, 24, b=GRAY)
    env = spritesheet.SpriteSheet('environment', key2, 16, 24, b=GRAY)
    
    man, manRect = player.render('guy')
    man = color_change(man, manRect, (255, 0, 0))
    man.set_colorkey(GRAY)
    manRect.topleft = (150,150)
    
    tile, tr = env.render('tile')
    tile = color_change(tile, tr, (100, 100, 100))
    
    wall, wr = env.render('wall')
    wall = color_change(wall, wr, (150,100,100))
    
    pf = frag.Frag(man, manRect)
    

def get_input():
    
    global pf
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() 
        elif event.type == KEYDOWN:
            # if event.key == K_w:
                # y -= 1
            # elif event.key == K_a:
                # x -= 1
            # elif event.key == K_s:
                # y += 1
            # elif event.key == K_d:
                # x += 1
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == K_g:
                pf.erode()
                   
    
def main():
    
    set_screen()
    set_images()
    
    clock = pygame.time.Clock()
    
    c = 0
    
    while True:
        
        SCREEN.blit(buffer, br)
        
        buffer.fill(WHITE)
        get_input()
        
        demo(c)
        
        pygame.display.update()
        
        clock.tick(60)
        print clock.get_fps()
        c += 1
        if c == 60:
            c = 0
    

# def glow(c):
    # global man, manRect, mancol
    
    # man, manRect = player.render('guy')
    # nc = c
    # if c > 30:
        # x = c-30
        # nc = 30 - x
    
    # man = color_change(man, manRect,(225, nc*3, nc*3))
    # man.set_colorkey(GRAY)
    
def demo(c):

    global pf

    #glow(c)
    
    
    #buffer.blit(man, manRect)
    pf.erode()
    
    pf.render(buffer)

    
        
main()