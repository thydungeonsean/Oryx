from map import Map
from decoration_map import DecorationMap
import cellular_automaton as ca
import tileset as ts
from random import *
from constants import *
import pygame
import common_tiles as ct
from spine import Spine
from continent import Continent


class WorldMap(Map):

    def __init__(self, w=100, h=50, sd=randint(0, 9999999), default='holder', loading_screen=(False, None)):

        Map.__init__(self, w, h, sd, default, loading_screen=loading_screen)

        self.tiles = {'ground': [],
                      'mountain': [],
                      'forest': [],
                      'water': [],
                      'depth': []
                      }

        self.tile_dict = {
            'ground': 'ground',
            'mountain': 'mountain',
            'forest': 'forest',
            'water': 'water',
            'depth': 'depth',
            'holder': 'holder'
        }

        self.tileset_id = 'world'
        self.shore_tiles = ts.TileSet('shore')
        self.shore_dict = {}

        self.map_image_ani = None

        # cellular automaton tuning stats
        self.open_noise = 45
        self.number_of_passes = 2
        self.opening_threshold = 5
        self.closing_threshold = 3
        self.special = None

        # have automaton run multiple times
        self.layers = 2
        self.split = (False, True, False)
        self.num_continents = 5
        self.num_islands = 4
        self.island_threshold = 5

        self.forest_seed = randint(0, 9999)

        self.automaton = ca.CellularAutomaton((self.xlim, self.ylim), self.seed, self.open_noise,
                                              self.number_of_passes, self.opening_threshold,
                                              self.closing_threshold, border=3, special=self.special, split=self.split)

        self.continents = {}
        self.islands = {}
        self.landmass_list = []

        self.map_type = 'world'

        self.generate_map()
        self.print_map()

    def generate_map(self):

        self.advance_loading(.1, 'forming land mass')
        for i in range(self.layers):
            self.automaton.generate_cellular_automaton()
            self.load_automaton()

        self.advance_loading(.3, 'filling oceans')
        self.flood_fill_add_tiles((0, 0), 'holder', 'water')

        self.advance_loading(.5, 'forming continents')
        self.form_continents()  # TODO make diagonal only connections of continents illegal

        self.add_mountain_ranges()
        self.add_hills()

        self.advance_loading(.7, 'adding forest')
        self.add_forest()

        self.make_tiles_dictionary()

        self.load_tileset()
        self.decoration_map = DecorationMap(self, self.seed, (.40, .00, .00, .00))
        self.shore_dict = self.set_shoreline()

        self.make_tiles_dictionary()

        self.advance_loading(.8, 'drawing map')
        self.map_image, self.map_image_ani, self.map_rect = self.draw_map()

        self.clear_screen()

    def load_automaton(self):

        for point in self.automaton.tiles.keys():
            if self.automaton.tiles[point]:
                self.add_tile(point, 'ground')

    def render(self, frame='a'):

        if frame == 'a':
            return self.map_image, self.map_rect
        elif frame == 'b':
            return self.map_image_ani, self.map_rect

    # map draw
    def draw_map(self):

        main_image, rect = self.draw_map_main()
        ani_image = self.draw_animated_map(main_image, rect)

        return main_image, ani_image, rect

    def draw_map_main(self):

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
            pass
                    
        # draw shoreline around continents
        for x, y in self.shore_dict.keys():
            
            y_pos = y * TILEHEIGHT
            x_pos = x * TILEWIDTH
            
            for tile_key in self.shore_dict[(x, y)]:
                tile = self.shore_tiles.get_tile(tile_key)
                tile.position((x_pos, y_pos))
                i, r = tile.render()
                image.blit(i, r)

        return image, image_rect

    def draw_animated_map(self, main_image, rect):

        image = pygame.Surface((rect.w, rect.h))
        image.blit(main_image, rect)

        tile = self.get_tile_image('water_ani')
        for (x, y) in self.tiles['water']:
            y_pos = y * TILEHEIGHT
            x_pos = x * TILEWIDTH

            tile.position((x_pos, y_pos))
            i, r = tile.render()
            image.blit(i, r)

        tile = self.get_tile_image('depth_ani')
        for (x, y) in self.tiles['depth']:
            y_pos = y * TILEHEIGHT
            x_pos = x * TILEWIDTH

            tile.position((x_pos, y_pos))
            i, r = tile.render()
            image.blit(i, r)

        # draw shoreline around continents
        for x, y in self.shore_dict.keys():

            y_pos = y * TILEHEIGHT
            x_pos = x * TILEWIDTH

            for tile_key in self.shore_dict[(x, y)]:
                tile = self.shore_tiles.get_tile(tile_key)
                tile.position((x_pos, y_pos))
                i, r = tile.render()
                image.blit(i, r)

        return image

    def get_shoreline(self):

        shoreline = {}

        codex = {
            'n': 't',
            'e': 'r',
            'w': 'l',
            's': 'b'
        }

        for y in range(self.ylim):
            for x in range(self.xlim):
                if self.map[x][y] not in ('water', 'depth'):
                    continue

                adj = self.get_adj_tile_dict((x, y))

                for d in adj['directions']:
                    code = codex[d]
                    if adj[d] not in ('water', 'depth'):
                        try:
                            shoreline[(x, y)].append(code)
                        except KeyError:
                            shoreline[(x, y)] = [code]

        return shoreline

    def set_shoreline(self):
        
        shoreline = self.get_shoreline()
                            
        for tile in shoreline.keys():
            shore = shoreline[tile]
            if 't' in shore:
                if 'r' in shore:
                    shore.append('tr')
                if 'l' in shore:
                    shore.append('tl')
            if 'b' in shore:
                if 'r' in shore:
                    shore.append('br')
                if 'l' in shore:
                    shore.append('bl')
                    
        return shoreline
        
    # continent functions
    def flood_fill_add_tiles(self, start, replaced_type, replacer_type):
                
        replace = [start]
        self.add_tile(start, replacer_type)
        while replace:
            
            replace = self.get_neighbors_flood(replace, replaced_type)
            for tile in replace:
                self.add_tile(tile, replacer_type)
                
    def get_neighbors_flood(self, replace, replaced_type):
        
        new_points = {}
        
        for tile in replace:
            adj = self.get_adj_tile_dict(tile)

            for d in adj['directions']:
                if adj[d] == replaced_type:
                    new_points[adj['%s_coord' % d]] = None
                    
        return new_points.keys()

    def flood_continent(self, (x, y)):
        
        # Starts from an unclaimed ground point. Flood fills all reachable ground from that point
        # and adds it to a continent dict. If it finds a holder tile it will start a nested flood
        # fill to turn the holder into mountains
        
        continent_points = {(x, y): None}
        
        queue = [(x, y)]
        
        while queue:
            
            queue = self.flood_id_continent(queue, continent_points)
        
        final_points = continent_points.keys()
        
        return final_points

    def flood_id_continent(self, queue, continent_points):
        
        new_queue = []
        
        for point in queue:
            adj = self.get_adj_tile_dict(point)
            for d in adj['directions']:
                tile_type = adj[d]
                coord = adj['%s_coord' % d]
                if tile_type in ('ground', 'mountain'):  # only add existing mountains and ground to continent
                    try:
                        continent_points[coord]  # if it's already part of continent, pass
                    except KeyError:
                        continent_points[coord] = None
                        new_queue.append(coord)
                elif tile_type == 'holder':  # if find a holder block, flood fill it with mountains
                    self.flood_fill_add_tiles(coord, 'holder', 'ground')
                    
        return new_queue
                    
    def find_ground(self):

        ground = []

        for y in range(self.ylim):
            for x in range(self.xlim):
                if self.map[x][y] == 'ground':
                    ground.append((x, y))

        return ground

    def form_continents(self):

        """
        Continent_map dict holds all the land tile coords as keys to which continent they belong to.
        Continents  holds the id #'s as keys to the corresponding continent dicts
        """
        masses = {}
        mass_map = {}
        # get all ground tiles on map. Currently map is ground made from cellular automata,
        # water flood filled as a surrounding ocean, and holder tiles in any gaps that ocean
        # flood fill didn't reach - landlocked empty space.
        unclaimed_ground = self.find_ground()  
        id = 0

        while unclaimed_ground:

            id += 1
            # Continent dict has 'id'= id#, 'points'= list of tiles, 'size'=num of tiles
            mass = {'id': id, 'points': []}
            start_point = choice(unclaimed_ground)

            continent_points = self.flood_continent(start_point)

            for point in continent_points:
                try:
                    unclaimed_ground.remove(point)
                except ValueError:
                    pass
                mass['points'].append(point)
                mass_map[point] = id

            mass['size'] = len(mass['points'])
            masses[id] = mass

        c, i, d = self.sort_continents_islands_depths(masses)

        for id in c:
            new = Continent(self, masses[id])
            self.continents[id] = new
            self.landmass_list.append(new)

        for id in i:
            self.islands[id] = masses[id]

        for id in d:
            depth = masses[id]['points']
            self.add_tiles(depth, 'depth')

    def sort_continents_islands_depths(self, masses):

        c_size = {}

        for i in masses.keys():
            if masses[i]['size'] >= self.island_threshold:
                c_size[i] = masses[i]['size']

        ordered = sorted(c_size.items(), key=lambda (k, v): v, reverse=True)

        c = self.num_continents
        if c > len(ordered):
            c = len(ordered)

        continents = ordered[:c]

        c_ids = []
        for k, v in continents:
            c_ids.append(k)

        islands_depths = ordered[self.num_continents+1:]

        i = self.num_islands
        if i > len(islands_depths):
            i = len(islands_depths)

        islands = sample(islands_depths, i)

        i_ids = []
        for k, v in islands:
            i_ids.append(k)

        d_ids = []
        for k, v in islands_depths:
            if (k, v) not in islands:
                d_ids.append(k)

        return c_ids, i_ids, d_ids

    def add_forest(self):

        forest = get_forest((self.xlim, self.ylim), self.forest_seed)

        for (x, y) in forest:

            if self.map[x][y] == 'ground':
                self.add_tile((x, y), 'forest')

    # mountain ranges
    def add_mountain_ranges(self):

        spine = Spine(self)
        
        for mass in self.landmass_list:
            mass.generate_mountains(spine)

    def add_hills(self):
        pass


def get_forest((w, h), seed):

    auto = ca.CellularAutomaton((w, h), seed, 40, 1, 4, 3)
    auto.generate_cellular_automaton()

    forest = []

    for point in auto.tiles.keys():
        if auto.tiles[point]:
            forest.append(point)

    return forest
