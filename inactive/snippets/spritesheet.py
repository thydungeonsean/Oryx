import pygame
from colours import *


class SpriteSheet(object):
       
    # loads image, w,h are tile dimensions, s is scale multiplier, b is colorkey
    def __init__(self, image, key, w, h, s=2, b=WHITE):
        
        ws = w*s
        hs = h*s
        
        self.key = key
        self.b = b
        
        image = pygame.image.load('assets/'+image+'.png')
        tempRect = image.get_rect()
        image = pygame.transform.scale(image, (tempRect.w * s, tempRect.h * s))
        #image.set_colorkey(b)
        
        self.FullImage = image
        self.FullRect = self.FullImage.get_rect()
        
        self.tile = pygame.Surface((ws, hs))
        #self.tile.set_colorkey(b)
        self.tile.fill(b)
        self.tileRect = self.tile.get_rect()

        gridw = self.FullRect.w / ws
        gridh = self.FullRect.h / hs
        
        self.frameDict = {}
        for y in range(gridh):
            for x in range(gridw):
                self.frameDict[(x,y)] = (-1 * x * ws, -1 * y * hs)
    
    def render(self, frame):
        
        if type(frame) is tuple:
            point = self.frameDict[frame]
        else:
            point = self.frameDict[self.key[frame]]
        
        self.FullRect.topleft = point
        
        self.tile.fill(self.b)
        self.tile.blit(self.FullImage, self.FullRect)
        self.tile.convert()
        
        return self.tile, self.tileRect