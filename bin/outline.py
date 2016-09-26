import pygame
from pygame.locals import *

pygame.init()


def check(pa, sur, dir, (x,y)):
    
    nx = x
    ny = y
    
    if dir == 'n':
        ny -= 1
    elif dir == 's':
        ny += 1
    elif dir == 'w':
        nx -= 1
    elif dir == 'e':
        nx += 1
        
    if pa[nx, ny] == sur.map_rgb((255, 255, 255)):
        return True
    else:
        return False



# main

print 'Enter an image to be outlined.'
f = raw_input('>')
i = None

try:
    i = pygame.image.load(f + '.png')
except:
    print 'file not found.'

if i is not None:
    
    ir = i.get_rect()
    w = ir.w
    h = ir.h
    
    pa = pygame.PixelArray(i)
    
    for y in range(h):
        for x in range(w):
            
            if pa[x, y] == i.map_rgb((33, 33, 33)):
                
                l = []
                
                if x != 0:
                    l.append(check(pa, i, 'w', (x, y)))
                
                if x != w - 1:
                    l.append(check(pa, i, 'e', (x, y)))
                    
                if y != 0:
                    l.append(check(pa, i, 'n', (x, y)))
                    
                if y != h-1:
                    l.append(check(pa, i, 's', (x, y)))
                    
                if True in l:
                    pa[x, y] = (0, 0, 0)
    
    outline = pa.make_surface()
    pygame.image.save(outline, f + 'outline.png')
    print 'done'
                
    