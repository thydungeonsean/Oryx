from constants import *
import image as img


# terrain tileset
def get_terrain_tileset(file):

    f = open('assets/tiles/tilesets/%s.tls' % file, 'r')

    colorkeys = {}
    attribkeys = {}
    tilekeys = {}

    for line in f:
        key, key_end = get_key(line)
        value = get_value(line, key_end)
        if key.startswith('col_'):
            colorkeys[key] = value
        elif key.startswith('atr_'):
            attribkeys[key] = line[key_end:].strip()
        elif value != '' and key != '':
            tilekeys[key] = value

    f.close()

    # colors dictionary should have format like this - 'dark': (DK_GREY, GREY)
    # name of pallet, tuple with forecolor and backcolor for pallet

    # tile_keys dict should be 'hor_wall': ('brick_wall', 'dark')
    # can pass the tile key - brick wall, and color pair to tile drawer
    # to draw the tile from tileset

    color_dict = get_color_pairs_dict(colorkeys)
    attributes = set_attributes(attribkeys)
    
    tileset = unpack_tileset(color_dict, tilekeys, attribkeys)
    
    return tileset, attributes


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


def get_color_pairs_dict(pairs):

    colors = {}

    for key, pair in pairs.items():
        color_pair = (color_key[pair[0]], color_key[pair[1]])       
        k = key[4:]
        colors[k] = color_pair
    return colors


def set_attributes(dict):

    new_dict = {}

    for key, value in dict.items():
        new_key = key[4:]
        new = value
        if new_key == 'crackable':
            if value == 'true':
                new = True
            else:
                new = False

        new_dict[new_key] = new

    if 'crackable' not in new_dict.keys():
        new_dict['crackable'] = False

    return new_dict

        
def unpack_tileset(color_dict, tile_keys, attribs):

    tileset = {}

    keys = tile_keys.keys()
    
    for key in keys:
        tile = tile_keys[key][0]
        color = color_dict[tile_keys[key][1]]
        value = (tile, color)
        tileset[key] = value

    return tileset
        
        
# object tileset
def get_object_tileset(file):

    f = open('assets/tiles/tilesets/%s.tls' % file, 'r')

    sheet_id = None
    tileset = {}

    for line in f:
        key, key_end = get_key(line)
        tile, color = get_value(line, key_end)
        if key.startswith('sheet_'):
            sheet_id = key[6:]
            sheet_id.strip('/n')
        elif key != '':
            tileset[key] = (tile, color_key[color])

    f.close()

    # tile_keys dict should be 'hor_wall': ('brick_wall', 'dark')
    # can pass the tile key - brick wall, and color pair to tile drawer
    # to draw the tile from tileset

    return sheet_id, tileset


def get_tile_keys(set):
    f = open('assets/tiles/tilesets/%s.tls' % set, 'r')

    keys = []

    for line in f:
        key, end = get_key(line)
        if not key.startswith('sheet_'):
            keys.append(key)

    f.close()

    return keys


class TileSet(object):

    def __init__(self, set):

        self.set = set
        self.sheet = None
        self.tileset = self.get_tileset()
        self.keys = self.tileset.keys()
        self.tile_images = self.set_tile_images()
                        
    def get_tileset(self):
        sheet, tileset = get_object_tileset(self.set)
        self.sheet = sheet
        return tileset
    
    def set_tile_images(self):

        images = {}

        for key, value in self.tileset.items():
            tk, col = value
            tile = (self.sheet, tk)
            images[key] = img.ScaledImage(tile, color=col, start_color=VR_DK_GREY)

        return images

    def get_tile(self, tile):

        return self.tile_images[tile]

    def render_tile(self, key):

        tile = self.tile_images[key]

        i, r = tile.render()

        return i, r


class OutlineTileSet(TileSet):

    def __init__(self, set):

        TileSet.__init__(self, set)

    def set_tile_images(self):

        images = {}

        for key, value in self.tileset.items():
            tk, col = value
            tile = (self.sheet, tk)
            images[key] = img.OutlinedImage(tile, color=col, start_color=VR_DK_GREY)

        return images

        
class TerrainTileSet(TileSet):

    attributes = {
        'base_color': 'lt_grey',
        'crackable': False
    }

    def __init__(self, set):

        self.attributes = {}

        TileSet.__init__(self, set)
        
    def get_tileset(self):

        self.sheet = 'terrain'
        tileset, attributes = get_terrain_tileset(self.set)
        self.attributes = attributes
        return tileset

    def set_tile_images(self):

        images = {}

        for key, value in self.tileset.items():
            tk, col = value
            tile = (self.sheet, tk)
            images[key] = img.TerrainImage(tile, col)

        return images
