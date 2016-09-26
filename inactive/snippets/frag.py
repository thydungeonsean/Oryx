import pygame
from random import choice
from colours import *


class Frag(object):
    
    def __init__(self, image, rect, back=GRAY):
    
        self.base_image = image
        self.base_coord = rect.topleft
        self.bx, self.by = self.base_coord
        self.full_w = rect.w
        self.full_h = rect.h
        
        self.back = back
        
        self.fsize = 4
        self.fragments = self.frag()
        
        
    def frag(self):
        
        fragments = []
        
        pixels = pygame.PixelArray(self.base_image)
        
        s = self.fsize
        
        for x in range(self.full_w/self.fsize):
            for y in range(self.full_h/self.fsize):

                f = pixels[x*s:(x+1)*s, y*s:(y+1)*s].make_surface()
                f.set_colorkey(self.back)
                f.convert()
                fr = f.get_rect()
                fr.topleft = self.bx + x*s, self.by + y*s
                fragments.append((f, fr))
                
        
        return fragments
        
    def render(self, surface):
        
        for f, fr in self.fragments:
            
            surface.blit(f, fr)
            
    def erode(self):
        
        if self.fragments:
            self.fragments.remove(choice(self.fragments))