from random import *
from ...graphics import common_tiles as ct


class DecorationMap(object):

    def __init__(self, owner_map, sd, (variety, gore, wear, age)=(.30, .10, .30, .60)):
        
        seed(sd)

        self.owner_map = owner_map
        self.xlim = owner_map.xlim
        self.ylim = owner_map.ylim
        self.tile_map = owner_map.map
        self.map_type = owner_map.map_type
        
        self.tiles = owner_map.tiles
        self.tile_dict = owner_map.tile_dict
        self.horizontal_walls = owner_map.horizontal_walls

        self.ground_list = []
        
        self.tileset = owner_map.tileset
        
        # tunable settings
        self.variety = variety
        self.gore = gore
        self.wear = wear
        self.age = age

        # initialize varied tiles for basic tile types if possible
        self.varied_points, self.variation_dict = self.vary_map()
        self.decorated = False
        if self.varied_points:
            self.decorated = True
            
        # add clutter
        self.clutter_points = []
        self.clutter_dict = {}
        self.has_gore = False
        self.has_wear = False
        self.has_age = False

        self.clutter_map()
        
    # vary basic tile types  
    def vary_map(self):

        variable_types = self.get_variable_tile_types()

        if not variable_types:
            return 0, 0

        varied_points = []
        variation_dict = {}

        for type in variable_types.keys():

            number = self.get_number_to_vary(type)

            for i in range(number):
                point = self.get_new_point_to_vary(type, varied_points)
                if not point:
                    break
                varied_points.append(point)
                variation_dict[point] = choice(variable_types[type])

        return varied_points, variation_dict

    def get_variable_tile_types(self):

        possible_variable_types = ['floor', 'wall', 'corridor', 'fixed_wall', 'ground', 'tree',
                                   'forest', 'mountain']
        types_in_map = []
        
        for type in possible_variable_types:
            if type in self.tile_dict.keys():
                types_in_map.append(type)
        
        variable_types = {}
        for type in types_in_map:
            
            key = self.tile_dict[type]
            
            options = []
            for k in self.tileset.keys:
                if k.startswith('var_%s' % key):
                    options.append(k)
                    
            if options:
                variable_types[key] = options

        return variable_types

    def get_number_to_vary(self, type):

        if type in ('floor', 'corridor', 'tree', 'mountain', 'forest'):
            return int(len(self.tiles[type]) * self.variety)
        elif type == 'hor_wall':
            return int(len(self.horizontal_walls) * self.variety)
        elif type == 'ground':
            for y in range(self.ylim):
                for x in range(self.xlim):
                    if self.tile_map[x][y] == 'ground':
                        self.ground_list.append((x, y))
            return int(len(self.ground_list) * self.variety)
        return 0

    def get_new_point_to_vary(self, type, varied_points):

        if type in ('floor', 'corridor', 'tree', 'field', 'mountain', 'forest'):
            l = self.tiles[type]
        elif type == 'hor_wall':
            l = self.horizontal_walls
        elif type == 'ground':
            l = self.ground_list

        for i in range(100):

            p = choice(l)

            if p not in varied_points:
                return p
        return False

    # add clutter to map
    def clutter_map(self):

        # use gore and age to add gore to map
        gore_points, gore_dict = self.add_gore()
        if gore_points:
            self.clutter_points.extend(gore_points)
            self.clutter_dict.update(gore_dict)
            self.has_gore = True

        # use wear setting to add cracks to tiles if crackable tileset
        if self.owner_map.tileset.attributes['crackable']:
            wear_points, wear_dict = self.add_wear()
        else:
            wear_points = False

        if wear_points:            
            self.clutter_points.extend(wear_points)
            self.clutter_dict.update(wear_dict)
            self.has_wear = True

        # use age setting to add cobwebs to corners
        if self.map_type in ('dungeon', 'cave'):
            age_points, age_dict = self.add_age()
            if age_points:
                self.clutter_points.extend(age_points)
                self.clutter_dict.update(age_dict)
                self.has_age = True

    def get_new_point_to_clutter(self, possible_points, clutter_points):

        for i in range(100):
            p = choice(possible_points)
            if p not in clutter_points:
                return p

        return False

    def add_gore(self):
        
        gore_points = []
        gore_dict = {}

        valid_points = []
        if self.map_type == 'dungeon':
            del valid_points
            valid_points = ('floor', 'corridor')
        elif self.map_type == 'cave':
            del valid_points
            valid_points = ('floor',)
        elif self.map_type == 'rural':
            del valid_points
            valid_points = ('floor', 'ground', 'field')

        possible_points = []

        for type in valid_points:
            if type != 'ground':
                possible_points.extend(self.tiles[type])
            else:
                possible_points.extend(self.ground_list)

        number = int(len(possible_points) * self.gore)

        for i in range(number):
            point = self.get_new_point_to_clutter(possible_points, gore_points)
            if not point:
                break
            gore_points.append(point)
            gore_dict[point] = ('gore', self.choose_gore())

        return gore_points, gore_dict

    def add_wear(self):

        wear_points = []
        wear_dict = {}

        wear_tiles = ('crack1', 'crack2')

        if self.map_type == 'dungeon':
            valid_points = ('floor', 'corridor')
        elif self.map_type == 'cave':
            valid_points = ('floor',)
        elif self.map_type == 'rural':
            valid_points = []
        elif self.map_type == 'world':
            valid_points = []

        for type in valid_points:
            possible_points = self.tiles[type]
            number = int(len(possible_points) * (self.wear/10.0))

            for i in range(number):
                point = self.get_new_point_to_vary(type, wear_points)
                if not point:
                    break
                wear_points.append(point)
                wear_dict[point] = ('dungeon_clutter', choice(wear_tiles))

        return wear_points, wear_dict

    def choose_gore(self):

        tiles = ct.common_tiles.tile_keys['gore']

        mode = randint(0, 3)
        if mode == 0:
            selection = tiles

        else:
            set = random()
            if set > self.age:
                selection = []
                for t in tiles:
                    if t.startswith('blood') or t.startswith('corpse'):
                        selection.append(t)
            elif set <= self.age:
                selection = []
                for t in tiles:
                    if t.startswith('bone') or t.startswith('corpse'):
                        selection.append(t)

        return choice(selection)

    # cobwebs and dust
    def add_age(self):

        age_list = []
        age_dict = {}

        possible_points = self.get_wall_edges()

        num = int(len(possible_points) * (self.age/2.5))

        edges = possible_points.keys()
        shuffle(edges)

        for i in range(num):
            edge = edges[i]
            age_list.append(edge)
            d = choice(possible_points[edge])
            if d not in ('tr', 'tl', 'br', 'bl'):
                value = 'dust_%s' % d
            else:
                if randint(0, 2) > 0:
                    value = 'cobweb_%s' % d
                else:
                    value = 'dust_%s' % d
            age_dict[edge] = ('dungeon_clutter', value)

        return age_list, age_dict

    def get_wall_edges(self):

        points = {}

        valid_points = []
        if self.map_type == 'dungeon':
            del valid_points
            valid_points = ('floor', 'corridor')
        elif self.map_type == 'cave':
            del valid_points
            valid_points = ('floor',)

        possible_points = []

        for type in valid_points:
            possible_points.extend(self.tiles[type])

        key = {
            'n': 't',
            's': 'b',
            'e': 'r',
            'w': 'l',
            'ne': 'tr',
            'nw': 'tl',
            'se': 'br',
            'sw': 'bl'
        }

        for point in possible_points:
            valid, edges = self.point_is_valid_for_dust(point, key)
            if valid:
                points[point] = edges

        return points

    def point_is_valid_for_dust(self, point, key):

        m = self.owner_map

        adj = m.get_adj_tile_dict(point)

        edges = []

        for d in adj['directions']:
            if adj[d] in ('wall', 'fixed_wall'):
                edges.append(key[d])

        if 't' in edges:
            if 'r' in edges:
                edges.append('tr')
            if 'l' in edges:
                edges.append('tl')
        if 'b' in edges:
            if 'r' in edges:
                edges.append('br')
            if 'l' in edges:
                edges.append('bl')

        redundant = ('tr', 'tl', 'bl', 'br')

        for d in redundant:
            if d in edges:
                try:
                    edges.remove(d[0])
                except ValueError:
                    pass
                try:
                    edges.remove(d[1])
                except ValueError:
                    pass

        valid = False
        if edges:
            valid = True

        return valid, edges
