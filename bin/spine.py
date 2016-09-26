

class Spine(object):

    def __init__(self, owner_map):

        self.world = owner_map
        self.map = self.world.map
        self.coasts = self.world.get_shoreline().keys()  # list of all water coords adj to land

        self.spine_map = self.find_spine()
        self.print_spine()

    def find_spine(self):

        points = self.coasts[:]
        step = 0
        spine_map = {}

        while points:
            step += 1
            points = self.get_neighbours(points, step, spine_map)

        return spine_map

    def get_neighbours(self, active, step, spine_map):

        next = []

        for point in active:

            adj = self.world.get_adj_tile_dict(point)

            for d in adj['directions']:
                adj_coord = adj['%s_coord' % d]
                if adj[d] == 'ground':
                    try:
                        spine_map[adj_coord]
                    except KeyError:
                        spine_map[adj_coord] = step
                        next.append(adj_coord)

        return next

    def print_spine(self):

        w = self.world.xlim
        h = self.world.ylim

        for y in range(h):
            line = ''
            for x in range(w):
                try:
                    node = str(self.spine_map[(x, y)])
                    if len(node) < 2:
                        node += ' '
                    line += node
                except KeyError:
                    line += '  '
            print line
