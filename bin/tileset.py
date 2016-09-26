from constants import *
from random import choice
import image as img


def get_tileset(file):

    f = open('assets/tilesheets/tilesets/%s.tls' % file, 'r')

    colorkeys = {}
    tilekeys = {}

    for line in f:
        key, key_end = get_key(line)
        value = get_value(line, key_end)
        if key.startswith('col_'):
            colorkeys[key] = value
        elif value != '' and key != '':
            tilekeys[key] = value

    f.close()

    # colors dictionary should have format like this - 'dark': (DK_GREY, GREY)
    # name of pallet, tuple with forecolor and backcolor for pallet

    # tile_keys dict should be 'hor_wall': ('brick_wall', 'dark')
    # can pass the tile key - brick wall, and color pair to tile drawer
    # to draw the tile from tileset

    color_dict = get_colors(colorkeys)
    
    tileset = unpack_tileset(color_dict, tilekeys)
    
    return tileset


def get_key(line):
    letters = []
    end = 0

    for letter in line:
        if letter == ':':
            end += 1
            break
        else:
            letters.append(letter)
            end += 1

    key = ''.join(letters)
    key.strip('/n')

    return key, end


def get_value(line, end):

    tag = line[end + 1:-1]
    value = tag.split(':')
    value = tuple(value)

    return value


def get_tile(dict, key):

    if key.startswith('var_'):
        return choice(dict[key])
    else:
        return dict[key]


def get_colors(pairs):

    colors = {}

    for key, pair in pairs.items():
        color_pair = (color_key[pair[0]], color_key[pair[1]])       
        k = key[4:]
        colors[k] = color_pair
    return colors
        
        
def unpack_tileset(color_dict, tile_keys):

    tileset = {}

    keys = tile_keys.keys()
    
    for key in keys:
        tile = tile_keys[key][0]
        color = color_dict[tile_keys[key][1]]
        value = (tile, color)
        tileset[key] = value

    return tileset
        

class TileSet(object):

    def __init__(self, set):

        self.set = set
        self.tileset = get_tileset(self.set)
        self.keys = self.tileset.keys()
        self.tile_images = self.set_tile_images()
                
    def set_tile_images(self):

        images = {}

        for key, value in self.tileset.items():
            tk, col = value
            tile = ('terrain', tk)
            images[key] = img.TerrainImage(tile, col)

        return images

    def get_tile(self, tile):

        return self.tile_images[tile]

    def render_tile(self, key):

        tile = self.tile_images[key]

        i, r = tile.render()

        return i, r


#t = TileSet('brick')
