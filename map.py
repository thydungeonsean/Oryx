from random import *
import pygame
from constants import *
import font_draw as fd

from tileset import TerrainTileSet
import common_tiles as ct


class Map(object):

    tiles_dir = {
        'dungeon': ('floor', 'corridor', 'door', 'wall', 'fixed_wall', 'filled', 'feature'),
        'rural': ('floor', 'door', 'wall', 'fixed_wall', 'ground', 'road', 'field', 'tree', 'feature'),
        'cave': ('floor', 'door', 'wall', 'fixed_wall', 'filled', 'feature'),
        'world': ('ground', 'mountain', 'forest', 'water', 'depth', 'feature')
    }

    tile_to_list_key = {
        'w_feature': 'feature',
        'nw_feature': 'feature',
        'fixed_wall': 'wall',
        'filled': None
    }

    def __init__(self, w=50, h=25, sd=randint(0, 9999999), default='filled', monsterset=('kobolds', 0), npcset=None,
                 loading_screen=(False, None)):

        self.seed = sd
        seed(self.seed)
        self.xlim = w
        self.ylim = h

        self.map_type = 'basic'

        self.map = self.init_map(default)

        self.descends = True

        self.zones = []
        self.wall_image_dict = {}
        self.horizontal_walls = []

        # should be overwritten by child classes
        self.decoration_map = False
        self.feature_map = False
        self.map_image = None
        self.map_rect = None

        self.tileset_id = 'cavern1'

        if loading_screen[0]:
            self.screen = loading_screen[1]
        else:
            self.screen = None

        self.bar = LoadingBar(loading_screen[0], self.screen)

        self.monsters = None
        self.npcs = npcset

        # initialize map - this should only be set in the child classes
        # self.generate_map(loading_screen[0])
        # self.print_map()

    def init_map(self, terrain):

        return [[terrain for y in range(self.ylim)] for x in range(self.xlim)]

    def print_map(self):

        key = {'floor': '.',
               'wall': '#',
               'fixed_wall': '#',
               'door': '+',
               'corridor': 'c',
               'filled': ' ',
               'ground': '.',
               'mountain': '^',
               'water': ' ',
               'forest': '"',
               'holder': 'H',
               'depth': ' ',
               'w_feature': '>',
               'nw_feature': 'I'
               }

        f = open('map.txt', 'w')

        for y in range(self.ylim):
            for x in range(self.xlim):
                f.write(key[self.map[x][y]])
            f.write('\n')

        f.close()

    def load_tileset(self):

        self.tileset = TerrainTileSet(self.tileset_id)

    # tile image related methods

    def get_tile_image(self, tile):
        return self.tileset.get_tile(tile)

    def get_map_tile(self, (x, y)):

        if (x, y) in self.wall_image_dict.keys():
            return self.wall_image_dict[(x, y)]

        return self.tile_dict[self.map[x][y]]

    def set_wall_image_dict(self):

        for point in self.tiles['wall']:
            value = self.find_wall_image(point)
            self.wall_image_dict[point] = value
            if value == 'hor_wall':
                self.horizontal_walls.append(point)

    def find_wall_image(self, (x, y)):

        if self.point_is_on_map((x, y + 1)):
            if self.map[x][y + 1] in ('floor', 'corridor'):
                return 'hor_wall'
            elif self.map[x][y + 1] == 'filled':
                return 'hor_filled'
            else:
                return 'ver_wall'
        elif not self.point_is_on_map((x, y + 1)):
            return 'hor_filled'

    def point_is_on_map(self, (x, y)):

        if 0 <= x < self.xlim and 0 <= y < self.ylim:
            return True
        else:
            return False

    def draw_map(self):

        image = pygame.Surface((self.xlim * TILEWIDTH, self.ylim * TILEHEIGHT))
        image.fill(BLACK)
        image = image.convert()
        image_rect = image.get_rect()

        for y in range(self.ylim):
            for x in range(self.xlim):

                y_pos = y * TILEHEIGHT
                x_pos = x * TILEWIDTH

                if self.point_is_on_map((x, y)):
                    if self.decoration_map and self.decoration_map.decorated \
                            and (x, y) in self.decoration_map.varied_points:
                        t = self.decoration_map.variation_dict[(x, y)]
                    else:
                        t = self.get_map_tile((x, y))
                    tile = self.get_tile_image(t)
                    tile.position((x_pos, y_pos))
                    i, r = tile.render()
                    image.blit(i, r)

                # draw clutter
                if self.decoration_map and (x, y) in self.decoration_map.clutter_points:
                    set, tile_key = self.decoration_map.clutter_dict[(x, y)]
                    t = ct.common_tiles.common_tiles[set].get_tile(tile_key)
                    t.position((x_pos, y_pos))
                    i, r = t.render()
                    image.blit(i, r)

                # draw permanent terrain features
                if self.feature_map and (x, y) in self.feature_map.terrain_tile_features.keys():
                    t = self.feature_map.terrain_tile_features[(x, y)]
                    tile = self.get_tile_image(t)
                    tile.position((x_pos, y_pos))
                    i, r = tile.render()
                    image.blit(i, r)

        # draw permanent non-terrain features

        if self.feature_map:
            ctf = self.feature_map.clutter_tile_features

            column_color = color_key[self.tileset.attributes['base_color']]

            for point in ctf.keys():
                x, y = point
                feature = self.feature_map.feature_at_point[point]
                if ctf[point] == 'column':

                    id = 'pillar'
                    if feature.cracked:
                        id = 'pillar_crack'
                    elif feature.broken:
                        id = 'pillar_broken'

                    y_pos = y * TILEHEIGHT
                    x_pos = x * TILEWIDTH
                    tile = ct.common_tiles.common_tiles['dungeon_features'].get_tile(id)
                    tile.position((x_pos, y_pos))
                    tile.change_color(column_color)
                    i, r = tile.render()
                    image.blit(i, r)

                elif ctf[point] == 'stalagmite':
                    id = feature.image_id

                    y_pos = y * TILEHEIGHT
                    x_pos = x * TILEWIDTH
                    tile = ct.common_tiles.common_tiles['dungeon_features'].get_tile(id)
                    tile.position((x_pos, y_pos))
                    tile.change_color(column_color)
                    i, r = tile.render()
                    image.blit(i, r)

        return image, image_rect

    def render(self, frame='a'):

        return self.map_image, self.map_rect

    # map changing methods

    def add_tile(self, (x, y), tile_type):

        self.map[x][y] = tile_type

    def add_tiles(self, set_of_tiles, tile_type):

        for tile in set_of_tiles:
            self.add_tile(tile, tile_type)

    def make_tiles_dictionary(self):

        del self.tiles

        tiles = {}

        set = Map.tiles_dir[self.map_type]

        for t in set:
            id = t
            if id in Map.tile_to_list_key.keys():
                id = Map.tile_to_list_key[id]
            tiles[id] = []

        for y in range(self.ylim):
            for x in range(self.xlim):
                t = self.map[x][y]

                if t in set:
                    id = t

                    if id in Map.tile_to_list_key.keys():
                        id = Map.tile_to_list_key[id]

                    if id is not None:
                        tiles[id].append((x, y))

        self.tiles = tiles

    # adjacency tools

    def get_adj_tile_dict(self, (x, y), diag=False):

        dict = {}
        tiles = []
        if self.point_is_on_map((x, y - 1)):
            dict['n'] = self.map[x][y - 1]
            dict['n_coord'] = (x, y - 1)
            tiles.append('n')
        if self.point_is_on_map((x, y + 1)):
            dict['s'] = self.map[x][y + 1]
            dict['s_coord'] = (x, y + 1)
            tiles.append('s')
        if self.point_is_on_map((x + 1, y)):
            dict['e'] = self.map[x + 1][y]
            dict['e_coord'] = (x + 1, y)
            tiles.append('e')
        if self.point_is_on_map((x - 1, y)):
            dict['w'] = self.map[x - 1][y]
            dict['w_coord'] = (x - 1, y)
            tiles.append('w')
        if diag:
            if self.point_is_on_map((x + 1, y - 1)):
                dict['ne'] = self.map[x + 1][y - 1]
                dict['ne_coord'] = (x + 1, y - 1)
                tiles.append('ne')
            if self.point_is_on_map((x - 1, y + 1)):
                dict['sw'] = self.map[x - 1][y + 1]
                dict['sw_coord'] = (x - 1, y + 1)
                tiles.append('sw')
            if self.point_is_on_map((x + 1, y + 1)):
                dict['se'] = self.map[x + 1][y + 1]
                dict['se_coord'] = (x + 1, y + 1)
                tiles.append('se')
            if self.point_is_on_map((x - 1, y - 1)):
                dict['nw'] = self.map[x - 1][y - 1]
                dict['nw_coord'] = (x - 1, y - 1)
                tiles.append('nw')

        dict['directions'] = tiles

        return dict

    def get_point_list(self):

        l = []

        for y in range(self.ylim):
            for x in range(self.xlim):
                l.append((x, y))

        return l

    # generation methods

    def generate_map(self, loading=False):

        pass

<<<<<<< HEAD
        
=======
>>>>>>> 4cb2960ec17955fc7f71d0780445f2bfa927a14b
    # loading bar
    def clear_screen(self):
        if self.bar.on:
            self.screen.fill(BLACK)
            pygame.display.update()

    def advance_loading(self, percent, message=''):
        if self.bar.on:
            self.screen.fill(BLACK)
            self.bar.draw(percent, message)
            pygame.display.update()
            
    # clean up methods
    # remove diagonal only connections
    def remove_diagonals(self, blank_tile, check_tile):
        
        for y in range(self.ylim-1):
            for x in range(self.xlim-1):
                
                self.check_quad((x, y))
                
    def check_quad(self, (x, y), blank_tile, check_tile):
        
        points = (
                  ((x, y), (x+1, y)),
                  ((x, y+1), (x+1, y+1))
                 )
        states = [[0, 0],
                  [0, 0]
                  ]
        for py in range(2):
            for px in range(2):
                fx, fy = points[px][py]
                if self.map[fx][fy] == check_tile:
                    states[px][py] = 1
                    
        if states[0][0] == states[1][1] and states[0][1] == states[1][0] and states[0][0] != states[0][1]:
            self.fix_quad(points, states, blank_tile)
                
    def fix_quad(self, points, states, blank_tile):
        
        if states[0][0] == 1:
            walls = ((0, 0), (1, 1))
        else:
            walls = ((0, 1), (1, 0))

        x, y = walls[randint(0, 1)]
        change_point = points[x][y]
        
        self.add_tile(change_point, blank_tile)    

    # clean up methods
    # remove diagonal only connections
    def remove_diagonals(self, blank_tile, check_tile):

        for y in range(self.ylim - 1):
            for x in range(self.xlim - 1):
                self.check_quad((x, y), blank_tile, check_tile)

    def check_quad(self, (x, y), blank_tile, check_tile):

        points = (
            ((x, y), (x + 1, y)),
            ((x, y + 1), (x + 1, y + 1))
        )
        states = [[0, 0],
                  [0, 0]
                  ]
        for py in range(2):
            for px in range(2):
                fx, fy = points[px][py]
                if self.map[fx][fy] == check_tile:
                    states[px][py] = 1

        if states[0][0] == states[1][1] and states[0][1] == states[1][0] and states[0][0] != states[0][1]:
            self.fix_quad(points, states, blank_tile)

    def fix_quad(self, points, states, blank_tile):

        if states[0][0] == 1:
            walls = ((0, 0), (1, 1))
        else:
            walls = ((0, 1), (1, 0))

        x, y = walls[randint(0, 1)]
        change_point = points[x][y]

        self.add_tile(change_point, blank_tile)
        # print 'added %s at %s' % (blank_tile, str(change_point))


class LoadingBar(object):
    def __init__(self, on, screen):
        self.on = on

        self.screen = screen

        self.w = TILEWIDTH * 10
        self.h = TILEHEIGHT

        self.x = SCREENWIDTH / 2 - self.w / 2
        self.y = SCREENHEIGHT / 2 - self.h / 2

        self.font_drawer = fd.FontDrawer()
        self.font_y = self.y + scale(20)

        self.bar_image = pygame.Surface((self.w, self.h))
        self.bar_rect = self.bar_image.get_rect()
        self.bar_rect.topleft = (self.x, self.y)
        self.bar_image = self.bar_image.convert()

    def draw(self, percent, message='loading'):
        self.bar_image.fill(GREY)
        w = int(self.w * percent)
        rect = pygame.Rect((0, 0), (w, self.h))
        pygame.draw.rect(self.bar_image, WHITE, rect)

        self.screen.blit(self.bar_image, self.bar_rect)

        fi, fr = self.font_drawer.write(message, WHITE)
        x = SCREENWIDTH / 2 - fr.w / 2
        fr.topleft = (x, self.font_y)

        self.screen.blit(fi, fr)

