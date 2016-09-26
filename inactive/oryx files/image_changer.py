import pygame
from pygame.locals import *
import os


pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
darkgrey(33, 33, 33)
lightgrey(196, 196, 196)

images = []
files = os.listdir('./')

for file in files:
    if file.endswith('.png'):
        images.append(file)

for file in images:
    
    image = pygame.image.load(file)
    
    pxarray = pygame.PixelArray(image)
    
    pxarray.replace(white, black)
    
    new = pxarray.make_surface()
    pygame.image.save(new, 'changed/%s' % file)