

class DijkstraMap(object):

    def __init__(self, owner_map, goals):
        
        self.owner_map = owner_map
        self.xlim = self.owner_map.xlim
        self.ylim = self.owner_map.ylim
        
        self.map = {}
        self.load_map()
      
        self.goals = goals

        self.initialize_map()

    def print_map(self):

        for y in range(self.ylim):
            line = ''
            for x in range(self.xlim):
                if (x, y) in self.map.keys():
                    num = str(self.map[(x, y)])
                    if len(num) < 3:
                        num = ' %s' % num
                    if len(num) < 2:
                        num = '%s ' % num
                    line += num
                else:
                    line += '   '

            print line

    def load_map(self):

        for y in range(self.ylim):
            for x in range(self.xlim):
                if self.walkable(self.owner_map.map[x][y]):
                    self.map[(x, y)] = 999

    def walkable(self, tile):

        if tile in ('floor', 'door', 'corridor', 'ground', 'field'):
            return True
        return False

    def initialize_map(self):

        active_points = []
        for point in self.goals:
            self.map[point] = 0
            active_points.append(point)

        complete = False
        
        active_points = self.run_dijkstra(active_points, start=True)

        while not complete:

            active_points = self.run_dijkstra(active_points)

            if not active_points:
                complete = True

    def run_dijkstra(self, checklist, start=False):

        next_points = []

        for point in checklist:
            change = False
            neighbours, neighbour_values = self.get_neighbour_points(point)
            lowest = sorted(neighbour_values)[0]

            if self.map[point] >= lowest + 2:
                self.map[point] = lowest + 1
                change = True
                
            if change or start:
                next_points.extend(neighbours)

        return next_points

    def get_neighbour_points(self, (x, y)):

        points = ((x, y-1),
                  (x, y+1),
                  (x-1, y),
                  (x+1, y)
                  )
        neighbours = []
        values = []

        for point in points:

            try:
                values.append(self.map[point])
                neighbours.append(point)
            except KeyError:
                pass

        return neighbours, values
