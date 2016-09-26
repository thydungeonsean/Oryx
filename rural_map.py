from random import *
from map import Map
from decoration_map import DecorationMap
import rooms


class RuralMap(Map):

    def __init__(self, w=50, h=25, sd=randint(0, 9999999), loading_screen=(False, None)):

        Map.__init__(self, w, h, sd, 'ground', loading_screen=loading_screen)

        self.map_type = 'rural'

        self.descends = False

        self.tileset_id = 'village'

        self.tiles = {'wall': [],
                      'floor': [],
                      'door': [],
                      'road': [],
                      'field': [],
                      'tree': [],
                      'ground': []
                      }
        self.edges = []

        self.tile_dict = {
            'floor': 'floor',
            'wall': 'hor_wall',
            'fixed_wall': 'hor_wall',
            'door': 'open_door',
            'ground': 'ground',
            'road': 'road',
            'field': 'field',
            'tree': 'tree'
        }

        self.build_margin = 3
        self.build_zone_x, self.build_zone_y = self.set_build_zone()

        self.building_count = 0
        self.building_ids = []
        self.buildings = {}

        # tunable stats
        self.number_of_buildings = 6

        self.has_trees = True
        self.foliage_density = 200

        self.has_fields = True
        self.max_fields = 5

        # room style and size ranges
        self.room_distribution = {(45, 89): 'rect',
                                  (90, 99): 'square',
                                  (0, 44): 'rect_cross'
                                  }

        self.room_size = {'rect': ((5, 7), (4, 5)),
                          'square': ((5, 6), (0, 1)),
                          'rect_cross': ((6, 7), (5, 6))
                          }

        self.generate_map()
        #self.set_wall_image_dict()
        #self.tileset = self.load_tileset()
        #self.decoration_map = DecorationMap(self, self.seed)

        self.print_map()

    # init methods

    def set_build_zone(self):

        if self.xlim <= 12:
            x_lim = (0, self.xlim)
        else:
            min = self.build_margin
            max = self.xlim - self.build_margin
            x_lim = (min, max)

        if self.ylim <= 12:
            y_lim = (0, self.ylim)
        else:
            min = self.build_margin
            max = self.ylim - self.build_margin
            y_lim = (min, max)

        return x_lim, y_lim

    def print_map(self):

        key = {'floor': '.',
               'wall': '#',
               'fixed_wall': '#',
               'door': '+',
               'ground': '"',
               'field': '^',
               'tree': 'T'
               }

        f = open('map.txt', 'w')

        for y in range(self.ylim):
            for x in range(self.xlim):
                f.write(key[self.map[x][y]])
            f.write('\n')

        f.close()

    # tile image methods

    def find_wall_image(self, (x, y)):

        if self.point_is_on_map((x, y+1)):
            if self.map[x][y+1] in ('floor', 'ground', 'road', 'field', 'tree'):
                return 'hor_wall'
            else:
                return 'ver_wall'
        elif not self.point_is_on_map((x, y+1)):
            return 'hor_wall'

    # tile changing methods

    def point_is_in_build_zone(self, (x, y)):

        if self.build_zone_x[0] <= x <= self.build_zone_x[1] and \
                self.build_zone_y[0] <= y <= self.build_zone_y[1]:
            return True
        else:
            return False


    def is_valid_tree_location(self, point):

        invalid_neighbors = ('tree', 'door')

        adj = self.get_adj_tile_dict(point, diag=True)
        d = adj['directions']

        for direction in d:
            if adj[direction] in invalid_neighbors:
                return False

        return True

    # generation methods

    def generate_map(self):

        self.advance_loading(.2, 'placing buildings')

        for i in range(self.number_of_buildings):
            self.place_buildings()

        self.advance_loading(.4, 'placing fields')
        if self.has_fields:
            self.place_fields()

        self.advance_loading(.5, 'placing trees')
        if self.has_trees:
            self.place_trees()

        self.load_tileset()
        self.make_tiles_dictionary()
        self.set_wall_image_dict()
        self.decoration_map = DecorationMap(self, self.seed)

        self.advance_loading(.7, 'drawing map')

        self.map_image, self.map_rect = self.draw_map()

        self.clear_screen()

    def place_buildings(self):

        placed = False
        tries = 0
        door_wall = []

        while not placed:
            if tries >= 500:
                return 'failed'

            room = self.get_new_building()

            bx, by = room['bottomright']
            edge = room['edge']
            corners = room['corners']
            walls = room['walls']
            floor = room['floor']

            conflict = False

            if not bx <= self.build_zone_x[1] or not by <= self.build_zone_y[1]:
                conflict = True

            if not conflict:
                for px, py in edge:
                    if self.point_is_on_map((px, py)) and self.map[px][py] in ('wall', 'fixed_wall', 'door', 'floor'):
                        conflict = True
                        break

            if not conflict:
                for point in corners:

                    px, py = point

                    if not self.point_is_on_map(point):
                        conflict = True
                        break
                    if self.map[px][py] in ('floor', 'wall', 'fixed_wall'):
                        conflict = True
                        break

            if not conflict:
                del door_wall[:]
                for point in walls:
                    px, py = point
                    if not self.point_is_on_map(point):
                        conflict = True
                        break
                    if self.map[px][py] in ('floor', 'wall', 'fixed_wall'):
                        conflict = True
                        break

                    door_wall.append(point)

            if not conflict:
                for point in floor:

                    px, py = point

                    if not self.point_is_on_map(point):
                        conflict = True
                        break
                    if self.map[px][py] == 'floor':
                        conflict = True
                        break

            if conflict:
                tries += 1
                continue

            self.building_count += 1
            room['#'] = str(self.building_count)

            self.buildings[room['#']] = room
            self.building_ids.append(room['#'])

            self.add_tiles(walls, 'wall')
            self.add_tiles(floor, 'floor')
            self.add_tiles(corners, 'fixed_wall')
            self.edges.extend(edge)
            placed = True

            if door_wall:
                door = choice(door_wall)
                self.add_tile(door, 'door')

    def get_new_building(self):

            # topleft coord
            start = (randint(self.build_zone_x[0], self.build_zone_x[1]),
                     randint(self.build_zone_y[0], self.build_zone_y[1]))

            # get type of room
            i = randint(0, 99)
            for k1, k2 in self.room_distribution.keys():
                if k1 <= i <= k2:
                    room_key = (k1, k2)
                    break

            room_type = self.room_distribution[room_key]

            min_w, max_w = self.room_size[room_type][0]
            min_h, max_h = self.room_size[room_type][1]

            w = randint(min_w, max_w)
            h = randint(min_h, max_h)
            if room_type == 'rect':
                room = rooms.add_rect_building(start, w, h)
            elif room_type == 'rect_cross':
                room = rooms.add_rect_cross_building(start, w, h)
            elif room_type == 'square':
                room = rooms.add_square_building(start, w)

            return room

    def place_fields(self):

        max = self.max_fields
        placed = 0
        tried = 0

        while True:

            field, edge = self.get_new_field()
            if field != 'fail':
                valid = True
                for px, py in field:
                    if not self.point_is_on_map((px, py)):
                        valid = False
                        break
                    if (px, py) in self.edges:
                        valid = False
                        break
                    set = ('floor', 'wall', 'fixed_wall', 'door', 'field')
                    if self.map[px][py] in set:
                        valid = False
                        break

                if valid:
                    self.add_tiles(field, 'field')
                    self.edges.extend(edge)
                    placed += 1

            if placed >= max:
                return
            tried += 1
            if tried > 500:
                return

    def get_new_field(self):

        # topleft coord
        start = (randint(self.build_zone_x[0], self.build_zone_x[1]),
                 randint(self.build_zone_y[0], self.build_zone_y[1]))

        w = randint(5, 12)
        h = randint(4, 9)

        sx, sy = start

        bx, by = sx+w, sy+h
        if bx > self.build_zone_x[1] or by > self.build_zone_y[1]:
            return 'fail', None

        field, edge = rooms.add_field(start, w, h)
        return field, edge

    def place_trees(self):

        for i in range(self.foliage_density):

            self.try_place_tree()

    def try_place_tree(self):

        x = randint(0, self.xlim-1)
        y = randint(0, self.ylim-1)

        block_terrain = ('tree', 'floor', 'wall', 'fixed_wall', 'door', 'field')
        if self.map[x][y] in block_terrain:
            return 'fail'

        if self.point_is_in_build_zone((x, y)):

            if self.is_valid_tree_location((x, y)):
                if randint(0, 1) == 1:
                    self.add_tile((x, y), 'tree')
        else:
            self.add_tile((x, y), 'tree')
