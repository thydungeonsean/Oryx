from random import *
from feature import *
import rooms as r


class FeatureMap(object):

    # this is specifically a DungeonMap Feature map
    # TODO add class hierarchy for feature maps?
    # need rural / urban / cavern / site features separate

    def __init__(self, map, sd):

        self.seed = sd
        seed(self.seed)

        self.map = map
        self.map_type = map.map_type
        self.descends = self.map.descends

        # main feature list
        self.features = {}
        self.feature_at_point = {}

        # for drawing purposes - commontiles sets
        self.terrain_tile_features = {}
        self.clutter_tile_features = {}

        # draw list
        self.draw_features = []

        ############
        # parameters
        ############

        self.columned_rooms = .5  # percentage of columned rooms
        self.wear = .5  # same as decoration map wear

        self.generate_features()

    # generation algorithm

    def generate_features(self):

        if self.map_type in ('dungeon', 'cave'):
            self.add_dungeon_entrance_and_exit()

        self.add_doors()

        if self.map_type == 'dungeon':
            self.add_columns()
        elif self.map_type == 'cave':
            self.add_stalagmites()

    # basics

    def add_feature(self, point, type, id=None):

        if type == 'entrance':
            new = Entrance(id, self.map, point)
        elif type == 'door':
            new = Door(id, self.map, point)
        elif type == 'lintel':
            new = Lintel(id, self.map, point)
        elif type == 'column':
            new = Column(id, self.map, point)
        elif type == 'stalagmite':
            new = Stalagmite(id, self.map, point)

        self.feature_at_point[point] = new
        # only functional features need an id??
        if id is not None:
            self.features[id] = new

        if not new.permanent:
            self.draw_features.append(new)

    @staticmethod
    def get_farthest(dist_map, spread):
        largest = sorted(dist_map.items(), key=lambda (k, v): v, reverse=True)[:spread]
        answer = []
        for key, value in largest:
            answer.append(key)
        return answer

    # dungeon entrance / exit methods

    def add_dungeon_entrance_and_exit(self):

        points = self.get_entrance_exit_points()

        entrance = choice(points)

        id = 'ent1'

        self.terrain_tile_features[entrance] = 'entrance'
        self.map.add_tile(entrance, 'w_feature')
        self.add_feature(entrance, 'entrance', id)
        self.add_lintels(entrance)

        if self.descends:
            exit = self.get_dungeon_exit_point(entrance, points, 5)
            id = 'ent2'
            self.terrain_tile_features[exit] = 'entrance'
            self.map.add_tile(exit, 'w_feature')
            self.add_feature(exit, 'entrance', id)
            self.add_lintels(exit)

    def add_lintels(self, point):

        lintels = []

        adj = self.map.get_adj_tile_dict(point, diag=True)
        for d in adj['directions']:
            p = adj['%s_coord' % d]
            if adj[d] == 'filled':
                lintels.append(p)
                self.map.add_tile(p, 'wall')
            elif adj[d] in ('wall', 'fixed_wall'):
                if self.map.wall_image_dict[point] == 'hor_filled':
                    lintels.append(p)
                    self.map.add_tile(p, 'wall')

        for l in lintels:
            image = self.map.find_wall_image(l)
            self.terrain_tile_features[l] = image
            self.add_feature(l, 'lintel')

    def get_dungeon_exit_point(self, (ex, ey), points, spread):

        dist_map = {}
        for x, y in points:
            dist = abs(ex - x) + abs(ey - y)
            dist_map[(x, y)] = dist

        possible = self.get_farthest(dist_map, spread)

        return choice(possible)

    def get_entrance_exit_points(self):

        points = []

        for px, py in self.map.tiles['wall']:
            if self.map.map[px][py] != 'wall':
                pass
            elif self.is_valid_entrance_exit_point((px, py)):
                points.append((px, py))

        return points

    def is_valid_entrance_exit_point(self, (x, y)):

        adj = self.map.get_adj_tile_dict((x, y))

        keys = adj['directions']
        if not sorted(keys) == sorted(['n', 's', 'e', 'w']):
            return False

        valid_door_posts = ('wall', 'fixed_wall')
        valid_threshold = ('floor', 'filled')
        if adj['n'] in valid_door_posts and adj['s'] in valid_door_posts and \
                adj['e'] in valid_threshold and \
                adj['w'] in valid_threshold and adj['w'] != adj['e']:
            return True
        elif adj['e'] in valid_door_posts and adj['w'] in valid_door_posts and \
                adj['n'] in valid_threshold and \
                adj['s'] in valid_threshold and adj['s'] != adj['n']:
            return True

        return False

    # doors

    def add_doors(self):

        for tile in self.map.tiles['door']:
            self.add_feature(tile, 'door', 'door%s' % str(tile))

    # columns

    def add_columns(self):

        rooms = self.create_columned_rooms()

        for room in rooms:
            self.add_column_features(room)

    def create_columned_rooms(self):

        number_of_columned_rooms = int(self.map.room_count * self.columned_rooms)

        rooms = range(1, self.map.room_count + 1)

        columned_rooms = []

        while len(columned_rooms) < number_of_columned_rooms:

            # end when we've tried all rooms or have the right percentage
            if not rooms:
                break

            int_id = choice(rooms)

            id = str(int_id)
            rooms.remove(int_id)

            room = self.map.rooms[id]

            # for now, 66/33 split for rooms with rimming of columns vs. filled with columns - only different in
            # very large rooms... maybe make fill less likely
            style = 'collonade'
            if randint(0, 2) == 0:
                style = 'complete'

            if r.add_columns(room, style=style):
                columned_rooms.append(room)

        return columned_rooms

    def add_column_features(self, room):

        num = len(room['columns'])

        cracked = int(num * self.wear)
        broken = int(num * (self.wear * .4))

        columns = []

        for point in room['columns']:
            self.add_feature(point, 'column')
            columns.append(self.feature_at_point[point])
            self.clutter_tile_features[point] = 'column'
            self.map.add_tile(point, 'nw_feature')

        shuffle(columns)

        for i in range(cracked):
            columns[i].crack_column()

        shuffle(columns)

        for i in range(broken):
            columns[i].break_column()

    # stalagmites
    def add_stalagmites(self):

        points = self.get_free_points()

        # TODO make stalagmite percentage a tunable for caverns?
        num = int(len(points)*.1)

        for i in range(num):

            if not points:
                break
            stalagmite = choice(points)
            self.add_feature(stalagmite, 'stalagmite')
            if randint(0, 1) == 0:
                self.feature_at_point[stalagmite].alternate()
            self.clutter_tile_features[stalagmite] = 'stalagmite'
            self.map.add_tile(stalagmite, 'nw_feature')

            self.free_point(stalagmite, points)

    def free_point(self, point, points):

        adj = self.map.get_adj_tile_dict(point, diag=True)
        for d in adj['directions']:
            tile = adj['%s_coord' % d]
            try:
                points.remove(tile)
            except ValueError:
                pass

    def get_free_points(self):

        floor = self.map.tiles['floor']

        points = []

        for point in floor:
            if self.point_is_free(point):
                points.append(point)

        return points

    def point_is_free(self, point):

        adj = self.map.get_adj_tile_dict(point, diag=True)
        for d in adj['directions']:
            if adj[d] in ('wall', 'fixed_wall', 'door', 'nw_feature'):
                return False

        return True
