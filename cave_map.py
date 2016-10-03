from map import Map
from random import shuffle, randint
import cellular_automaton as ca
import monster_set as ms
from feature_map import FeatureMap
from decoration_map import DecorationMap


class CaveMap(Map):

    def __init__(self, w=50, h=30, sd=randint(0, 9999999), loading_screen=(False, None)):

        Map.__init__(self, w, h, sd, loading_screen=loading_screen)

        self.map_type = 'cave'

        self.tiles = {'wall': [],
                      'floor': [],
                      'door': []
                      }

        self.tile_dict = {
            'floor': 'floor',
            'wall': 'hor_wall',
            'filled': 'filled',
            'fixed_wall': 'hor_wall',
            'door': 'open_door',
            'w_feature': 'floor',
            'nw_feature': 'floor'
        }

        self.tileset_id = 'cavern1'

        # cellular automaton tuning stats
        self.open_noise = 45
        self.number_of_passes = 3
        self.opening_threshold = 4
        self.closing_threshold = 3

        self.automaton = ca.CellularAutomaton((self.xlim, self.ylim), self.seed, self.open_noise,
                                              self.number_of_passes, self.opening_threshold, self.closing_threshold)

        self.generate_map()
        # self.tileset = self.load_tileset()
        self.print_map()

    def generate_map(self):

        self.advance_loading(.3, 'tunelling')
        self.automaton.generate_cellular_automaton()

        self.advance_loading(.4, 'loading tunnels')
        self.load_automaton()

        self.advance_loading(.45, 'connecting caves')
        self.remove_diagonals('floor', 'filled')
        self.flood_connect_cavern()

        self.advance_loading(.5, 'adding walls')

        self.add_walls()

        self.make_tiles_dictionary()
        self.set_wall_image_dict()
        self.load_tileset()

        self.feature_map = FeatureMap(self, self.seed)

        self.make_tiles_dictionary()
        self.decoration_map = DecorationMap(self, self.seed)

        self.advance_loading(.7, 'drawing map')
        self.map_image, self.map_rect = self.draw_map()

        self.advance_loading(.8, 'adding monsters')
        self.monsters = ms.MonsterSet(self, self.seed, ('kobolds', 30))

        self.clear_screen()

    def load_automaton(self):

        for point in self.automaton.tiles.keys():
            if self.automaton.tiles[point]:
                self.add_tile(point, 'floor')

    def add_walls(self):

        p = self.get_point_list()

        for point in p:

            adj = self.get_adj_tile_dict(point, diag=True)

            px, py = point

            if self.map[px][py] == 'floor':
                continue

            wall = False

            for d in adj['directions']:
                if adj[d] == 'floor':
                    wall = True
                    break

            if wall:
                self.add_tile(point, 'wall')
    
    # connect separate caves
    def flood_connect_cavern(self):

        connected = False

        while not connected:
            point_to_cave = self.get_cave_dictionary()
            cave_to_point = self.invert_cave_dict(point_to_cave)

            # self.print_cave_ids(point_to_cave)

            self.fill_small_caves(cave_to_point)

            if len(cave_to_point) > 1:
                self.connect_caves(cave_to_point, point_to_cave)
            else:
                connected = True

    def get_cave_dictionary(self):
    
        cave_dictionary = {}

        cave = 0

        for x, y in self.get_point_list():
            if self.map[x][y] == 'filled':
                continue
            try:
                cave_dictionary[(x, y)]
            except KeyError:  # only try flood filling if it's not part of a cave already
                cave += 1
                self.flood_cave((x, y), cave_dictionary, cave)
                
        return cave_dictionary
    
    def flood_cave(self, (x, y), dict, tag):

        dict[(x, y)] = tag

        queue = [(x, y)]

        complete = False

        while not complete:

            queue = self.flood(queue, dict, tag)

            if not queue:
                complete = True

    def flood(self, queue, dict, tag):

        next_queue = []

        for point in queue:

            neighbours = self.get_neighbours(point)

            for p in neighbours:
                try:
                    dict[p]
                except KeyError:
                    dict[p] = tag
                    next_queue.append(p)

        return next_queue

    def get_neighbours(self, (x, y)):

        points = []

        d = ((x, y-1),
             (x, y+1),
             (x-1, y),
             (x+1, y)
             )

        for px, py in d:
            if self.point_is_on_map((px, py)):
                if self.map[px][py] == 'floor':
                    points.append((px, py))

        return points

    def print_cave_ids(self, dict):

        for y in range(self.ylim):
            line = ''
            for x in range(self.xlim):
                if (x, y) in dict.keys():
                    num = str(dict[(x, y)])
                    line += num
                else:
                    line += ' '

            print line

    @staticmethod
    def invert_cave_dict(cave_dict):

        new = {}

        for k, v in cave_dict.items():

            try:
                new[v].append(k)
            except KeyError:
                new[v] = [k]

        return new

    def fill_small_caves(self, caves):

        delete_list = []

        for cave in caves.keys():
            if len(caves[cave]) < 5:
                delete_list.append(cave)

        for cave in delete_list:

            for point in caves[cave]:
                self.add_tile(point, 'filled')

            del caves[cave]

    def connect_caves(self, cave_to_point, point_to_cave):

        size_comp = {}
        for cave in cave_to_point.keys():
            size_comp[cave] = cave_to_point[cave]

        sorted_caves = self.sort_by_largest(size_comp)

        sorted_caves.pop(0)  # remove largest cave

        shuffle(sorted_caves)
        cave = sorted_caves[0]
        self.connect_cave(cave, cave_to_point, point_to_cave)

    @staticmethod
    def sort_by_largest(caves):

        sorted_caves = sorted(caves.items(), key=lambda (k, v): v)
        answer = []
        for key, value in sorted_caves:
            answer.append(key)
        return answer

    def connect_cave(self, cave, caves, inv_caves):

        paths = {}

        active_points = []

        for point in caves[cave]:

            active_points.append(point)
            paths[point] = ('end', 0)

        step = 0
        found = False

        while not found:

            step += 1
            active_points = self.flood_find_cave(active_points, paths, step, inv_caves, cave)

            for x, y in active_points:
                if self.map[x][y] == 'floor':
                    found = True
                    end = (x, y)

        self.trace_connection(paths, end, cave, caves, inv_caves)

    def flood_find_cave(self, queue, paths, step, inv_caves, current_cave):

        next_queue = []

        for point in queue:

            neighbours = self.get_neighbours_find_cave(point, inv_caves, current_cave)

            for p in neighbours:
                try:
                    paths[p]
                except KeyError:
                    paths[p] = (point, step)
                    next_queue.append(p)

        return next_queue

    def get_neighbours_find_cave(self, (x, y), inv_caves, cave):

        points = []

        d = ((x, y - 1),
             (x, y + 1),
             (x - 1, y),
             (x + 1, y)
             )

        for px, py in d:
            if not self.point_is_on_map((px, py)):
                continue
            if px == 0 or py == 0 or px == self.xlim-1 or py == self.ylim-1:
                continue

            if self.map[px][py] == 'filled':
                 points.append((px, py))
            elif self.map[px][py] == 'floor' and inv_caves[(px, py)] != cave:
                points.append((px, py))

        return points
        
    def trace_connection(self, path_dict, end, cave, point_to_cave, cave_to_point):

        trace = []
        p = end
        while path_dict[p][0] != 'end':
            trace.append(p)
            p = path_dict[p][0]

        for p in trace:
            self.add_tile(p, 'floor')
