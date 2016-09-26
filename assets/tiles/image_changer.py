import pygame
from pygame.locals import *
import os


pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
darkgrey = (33, 33, 33)
lightgrey = (200, 200, 200)

images = ['terrain_objects.png']
# files = os.listdir('./')

# for file in files:
    # if file.endswith('.png'):
        # images.append(file)

for file in images:
    
    image = pygame.image.load(file)
    
    pxarray = pygame.PixelArray(image)
    
    #pxarray.replace(white, lightgrey)
    pxarray.replace(black, darkgrey)
    
    new = pxarray.make_surface()
    pygame.image.save(new, 'new_tile.png')