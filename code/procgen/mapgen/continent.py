from random import *
from terrain_crawler import *


class Continent(object):

    def __init__(self, owner_map, mass):
    
        self.world = owner_map
        self.map = self.world.map
        
        self.dict = mass
        
        self.id = mass['id']
        self.points = mass['points']
        self.size = mass['size']
        
        self.name = self.get_name()
        self.seed = self.get_seed()
        seed(self.seed)
        
        self.mountains = int(self.size * uniform(0.1, 0.2))  # number of mountain tiles to aim for
        
    def get_name(self):
        
        return 'continent%s' % self.id
        
    def get_seed(self):
        
        owner = str(self.world.seed)
        new = int(owner + str(self.id))
        
        return new
    
    # adding mountains to continent
    def get_height_map(self, spine):
        
        height_map = {}
        
        for x, y in self.points:
            if self.world.map[x][y] == 'ground':
                height = spine.spine_map[(x, y)]
                height_map[(x, y)] = height
            
        return height_map

    @staticmethod
    def get_height_ranges(height_map):

        # h_range is a count of how many of each height value exists on continent
        h_range = {}
        
        for v in height_map.values():
            try:
                h_range[v] += 1
            except KeyError:
                h_range[v] = 1
            
        return sorted(h_range.keys()), h_range
        
    def generate_mountains(self, spine):
    
        height_map = self.get_height_map(spine)

        range_of_heights, height_range_map = self.get_height_ranges(height_map)
        
        highest = range_of_heights[-1]  # or maybe [0] - can't remember how sorted works
        
        # set what types of ranges we can have
        mountain_type_dict = {
                'peak': True,
                'wall': True,
                'barrier': True,
                'range': True,
                'coastal': True
                }
        
        if highest < 4:  # we have a very small or narrow continent - don't add as many mountains?
            self.mountains = int(self.size * uniform(0.05, 0.25))
            mountain_type_dict['range'] = False
            mountain_type_dict['wall'] = False
            
        number_placed = 0
        mountain_types = []
        for m in mountain_type_dict.keys():
            if mountain_type_dict[m]:
                mountain_types.append(m)
        
        while number_placed < self.mountains:
            
            mountain_type = choice(mountain_types)
            
            if mountain_type == 'peak':
                number_placed += self.place_peaks(height_map, range_of_heights)
            elif mountain_type == 'wall':
                placed, null = self.place_wall(height_map, range_of_heights)
                number_placed += placed
            elif mountain_type == 'barrier':
                number_placed += self.place_barrier(height_map, range_of_heights)
            elif mountain_type == 'range':
                number_placed += self.place_range(height_map, range_of_heights)
            elif mountain_type == 'coastal':
                number_placed += self.place_range(height_map, range_of_heights, level=1)
                
    def place_peaks(self, height_map, height_ranges):
        
        highest = height_ranges[-1]
        min = 5
        max = 12        

        if highest < 4:
            start_range = [highest]
            min = 3
            max = 7
        elif highest < 6:
            start_range = height_ranges[-3:]
        else:
            start_range = height_ranges[4:]
            max = 20
        
        start_height = choice(start_range)
        start = self.get_start_point_at_range(start_height, height_map)
        if not start:
            return 0
        
        crawler = MountainPeakCrawler(self, start, randint(min, max), height_map)
        zone_size = crawler.grow_zone()
        
        return zone_size
    
    def place_wall(self, height_map, height_ranges, start=None):
        
        highest = height_ranges[-1]
        min = 5
        max = 12        

        if highest < 4:
            start_range = [highest]
            min = 2
            max = 5
        elif highest < 6:
            start_range = height_ranges[-3:]
        else:
            start_range = height_ranges[-4:]
            max = 16

        if start is None:

            start_height = choice(start_range)
            start = self.get_start_point_at_range(start_height, height_map)
            if not start:
                return 0, None
        
        crawler = MountainWallCrawler(self, start, randint(min, max), height_map)
        zone_size = crawler.grow_zone()
        
        return zone_size, start
        
    def place_barrier(self, height_map, height_ranges):
        
        barrier_1_size, start = self.place_wall(height_map, height_ranges)
        barrier_2_size, null = self.place_wall(height_map, height_ranges, start=start)
        barrier_1_size += barrier_2_size
        
        return barrier_1_size
        
    def place_range(self, height_map, height_ranges, level=None):
        
        highest = height_ranges[-1]
        
        if level is None: # if no set level for range, choose one
            if highest < 6:
                start_range = height_ranges[1:-2]
            else:
                start_range = height_ranges[1:-4]
            level = choice(start_range)
        
        min = 6
        max = 10
        
        if highest < 6:
            pass
        elif highest < 10:
            max = 15
        else:
            min = 10
            max = 20
        
        start = self.get_start_point_at_range(level, height_map)
        if not start:
            return 0

        size = randint(min, max)

        crawler = MountainRangeCrawler(self, start, size, height_map)
        zone_size = crawler.grow_zone()

        return zone_size

    @staticmethod
    def get_start_point_at_range(start_height, height_map):
        
        possible = []
        for point, height in height_map.items():
            
            if height == start_height:
                possible.append(point)

        if not possible:  # no points at that height range
            return False

        return choice(possible)

