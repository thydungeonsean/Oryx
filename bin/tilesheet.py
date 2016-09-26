import pygame
from constants import *


def get_tile_image(tileset, tileset_key, key):
    
    tile_sheet = pygame.image.load('assets/tilesheets/%s.png' % tileset)
    tsr = tile_sheet.get_rect()
    
    point = tileset_key[key]
    
    tile = pygame.Surface((BASE_TILEWIDTH, BASE_TILEHEIGHT))
    tile.fill(WHITE)
    tr = tile.get_rect()
    
    set_offset(tsr, point)
    tile.blit(tile_sheet, tsr)
    
    return tile, tr
    

def set_offset(rect, (px, py)):
    
    x = px * BASE_TILEWIDTH * -1
    y = py * BASE_TILEHEIGHT * -1
    
    rect.topleft = (x, y)