import pygame
from ..constants import *


# gets an image off of a tilesheet using the tilesheet_key dictionary
def get_tile_image(tileset, tileset_key, key):
    
    tile_sheet = pygame.image.load('assets/tiles/%s.png' % tileset)
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
    

# returns a dictionary of tile names and offset coords for a tilesheet image
def get_tilesheet_key(file):
    
    f = open('assets/tiles/keys/%s.txt' % file, 'r')
    
    tilesheet_key = {}

    for line in f:

        key, end = get_tile_key(line)
        value = get_tile_offset_value(line, end)
        tilesheet_key[key] = value

    f.close()
    return tilesheet_key
    

# gets tile name key from key file
def get_tile_key(line):
    
    letters = []
    end = 0
    
    for letter in line:
        if letter == ' ':
            break
        else:
            letters.append(letter)
            end += 1
            
    key = ''.join(letters)
    
    return key, end
    
  
# gets offset value for tile from key file  
def get_tile_offset_value(line, end):
    
    tup = []
    value = []
    state = 'one'
    
    for letter in line[end+1:-1]:
        if state == 'one' and letter != ',':
            value.append(letter)
        elif state == 'one' and letter == ',':
            v1 = int(''.join(value))
            tup.append(v1)
            state = 'two'
            value = []
        elif state == 'two':
            value.append(letter)
    
    v2 = int(''.join(value))
    tup.append(v2)
    value = tuple(tup)
    
    return value