from random import *


class TerrainCrawler(object):

    def __init__(self, continent, terrain, start_point, size, height_map):
        
        self.continent = continent
        self.world = continent.world
        self.map = continent.map

        self.new_terrain = terrain
        self.replace_terrain = self.set_replace_terrain()

        self.active_points = [start_point]
        self.grown_points = [start_point]

        self.remaining_steps = size

        self.height_map = height_map
        self.height_level = height_map[start_point]

    def set_replace_terrain(self):
        
        if self.new_terrain == 'mountain':
            return ('ground',)            
                    
    def _purge(self, to_remove): 
        for point in to_remove:
            self.active_points.remove(point)
            
    def grow_zone(self):

        while self.remaining_steps > 0:
        
            self.step()
            self.remaining_steps -= 1
            
        for point in self.grown_points:
            self.world.add_tile(point, self.new_terrain)

        return len(self.grown_points)
        
    def step(self):
        pass
        
    def change_height_level(self):
        pass
            
    def get_valid_adj_points(self, point):
    
        valid = []
    
        adj = self.world.get_adj_tile_dict(point, diag=True)
        
        for d in adj['directions']:
            d_coord = '%s_coord' % d
            
            if adj[d_coord] in self.grown_points:
                continue
                
            if adj[d] not in self.replace_terrain:
                continue

            try:
                self.height_map[adj[d_coord]]
            except KeyError:  # not part of height map
                continue

            if self.height_map[adj[d_coord]] != self.height_level:
                continue
            
            # if at this point, point is valid for crawling, add to list
            valid.append(adj[d_coord])
                
        return valid

                
class MountainCrawler(TerrainCrawler):
    
    def __init__(self, continent, start_point, size, height_map):
        
        TerrainCrawler.__init__(self, continent, 'mountain', start_point, size, height_map)
        
    def grow_zone(self):

        while self.remaining_steps > 0:
        
            self.step()
            self.remaining_steps -= 1
            
        for point in self.grown_points:
            self.world.add_tile(point, self.new_terrain)
            
        # remap is reason for overwrite
        self.remap_heightmap()

        return len(self.grown_points)
        
    def remap_heightmap(self):
        # this makes areas adj to the mountain range created less likely
        # to become mountains in next pass - to separate ranges
        
        for point in self.grown_points:
            adj = self.world.get_adj_tile_dict(point)
            for d in adj['directions']:
                d_coord = '%s_coord' % d
                if adj[d_coord] in self.grown_points:
                    continue
                if adj[d] not in self.replace_terrain:
                    continue
                try:
                    self.height_map[adj[d_coord]] -= 2
                except KeyError:
                    pass
                

class MountainPeakCrawler(MountainCrawler):

    def __init__(self, continent, start_point, size, height_map):
        
        MountainCrawler.__init__(self, continent, start_point, size, height_map)

    def step(self):
        
        point = False
        
        while not point:
        
            point = self.get_next_step()
            # if no next step at height range, change height range
            if not point:
                _continue = self.change_height_level()
                if not _continue:
                    return
                    
        self.grown_points.append(point)
        self.active_points.append(point)

    def get_next_step(self):
        
        shuffle(self.active_points)
        to_remove = []        
        
        for point in self.active_points:
            
            adj = self.get_valid_adj_points(point)
            if not adj:  # no valid neighbors for active point
                to_remove.append(point)
            else:
                self._purge(to_remove)
                return choice(adj)
                
        return False

    def change_height_level(self):
        
        self.active_points = []
        
        for point in self.grown_points:
            self.active_points.append(point)
            
        self.height_level -= 1
        
        if self.height_level <= 0:
            return False
        return True
   
            
class MountainWallCrawler(MountainCrawler):
    
    def __init__(self, continent, start_point, size, height_map):
        
        MountainCrawler.__init__(self, continent, start_point, size, height_map)
        self.start = start_point
        
    def step(self):
    
        point = False
        
        while not point:
        
            point = self.get_next_step()
            
            if not point:
                return

            self.change_height_level()
                
        self.grown_points.append(point)
        self.active_points.append(point)
        
    def get_next_step(self):
        
        shuffle(self.active_points)
        to_remove = []        
        
        for point in self.active_points:
            
            adj = self.get_valid_adj_points(point)
            if not adj:  # no valid neighbors for active point
                to_remove.append(point)
            else:
                self._purge(to_remove)
                return choice(adj)
                
        return False
        
    def change_height_level(self):
        
        self.active_points = []
        
        for point in self.grown_points:
            self.active_points.append(point)
            
        self.height_level -= 1
        
        if self.height_level <= 0:
            return False
        return True

    def remap_heightmap(self):

        range_points = self.grown_points[:]
        range_points.remove(self.start)

        # this makes areas adj to the mountain range created less likely
        # to become mountains in next pass - to separate ranges

        for point in range_points:
            adj = self.world.get_adj_tile_dict(point)
            for d in adj['directions']:
                d_coord = '%s_coord' % d
                if adj[d_coord] in self.grown_points:
                    continue
                if adj[d] not in self.replace_terrain:
                    continue
                try:
                    self.height_map[adj[d_coord]] -= 2
                except KeyError:
                    pass

            
class MountainRangeCrawler(MountainCrawler):

    def __init__(self, continent, start_point, size, height_map):
        
        MountainCrawler.__init__(self, continent, start_point, size, height_map)
        self.base_height = self.height_level
        self.levels = [-1, 1]
        
    def step(self):
        
        point = False
        
        while not point:
        
            point = self.get_next_step()
            # if no next step at height range, change height range
            if not point:
                _continue = self.change_height_level()
                if not _continue:
                    return
                    
        self.grown_points.append(point)
        self.active_points.append(point)

    def get_next_step(self):
        
        shuffle(self.active_points)
        to_remove = []        
        
        for point in self.active_points:
            
            adj = self.get_valid_adj_points(point)
            if not adj:  # no valid neighbors for active point
                to_remove.append(point)
            else:
                self._purge(to_remove)
                return choice(adj)
                
        return False
        
    def change_height_level(self):
        
        if not self.levels:
            return False
        
        self.active_points = []
        
        for point in self.grown_points:
            self.active_points.append(point)
        
        mod = choice(self.levels)
        self.levels.remove(mod)
        
        self.height_level = self.base_height + mod

        return True
