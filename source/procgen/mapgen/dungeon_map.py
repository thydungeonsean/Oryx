from random import *
from map import Map
from decoration_map import DecorationMap
from feature_map import FeatureMap
import rooms
from ...items.actors import monster_set as ms


class DungeonMap(Map):

    def __init__(self, w=50, h=30, sd=randint(0, 9999999), loading_screen=(False, None)):

        Map.__init__(self, w, h, sd, 'filled', loading_screen=loading_screen)

        self.map_type = 'dungeon'

        self.room_count = 0
        self.room_ids = []
        self.rooms = {}

        self.tiles = {'wall': [],
                      'floor': [],
                      'corridor': [],
                      'door': []
                      }

        self.tile_dict = {
                        'floor': 'floor',
                        'wall': 'hor_wall',
                        'filled': 'filled',
                        'fixed_wall': 'hor_wall',
                        'door': 'open_door',
                        'corridor': 'floor',
                        'w_feature': 'floor',
                        'nw_feature': 'floor'
                        }

        # tunable stats for generation
        self.number_of_rooms = 30
        self.number_of_extra_corridors = 10

        # room style and size ranges
        self.room_distribution = {(0, 49): 'rect',
                                  (100, 100): 'square',
                                  (50, 69): 'rect_cross',
                                  (70, 99): 'alcove'
                                  }
        self.room_size = {'rect': ((5, 15), (5, 9)),
                          'rect_cross': ((5, 15), (5, 9)),
                          'square': ((5, 12), (0, 1)),
                          'alcove': ((5, 12), (5, 10))
                          }

        self.tileset_id = 'brick'

        # initialize map
        self.generate_map()
        self.print_map()



    # generation methods

    def generate_map(self):

        self.advance_loading(0, 'generating rooms')
        for i in range(self.number_of_rooms):
            successful = self.place_room()

        self.advance_loading(.2, 'connecting dungeon')
        self.connect_zones()

        self.advance_loading(.4, 'finishing walls')
        self.fill_in_walls()

        self.advance_loading(.5, 'adding doorways')
        self.add_corridor_doors()

        self.advance_loading(.55, 'adding features')

        self.make_tiles_dictionary()
        self.set_wall_image_dict()
        self.load_tileset()

        self.feature_map = FeatureMap(self, self.seed)
        self.make_tiles_dictionary()
        self.decoration_map = DecorationMap(self, self.seed)

        self.advance_loading(.6, 'drawing map')
        self.map_image, self.map_rect = self.draw_map()

        self.advance_loading(.8, 'adding monsters')
        self.monsters = ms.MonsterSet(self, self.seed, ('kobolds', 20))

        self.clear_screen()

    def get_new_room(self):

        # topleft coord
        start = (randint(0, self.xlim - 1), randint(0, self.ylim - 1))

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

        if w % 2 == 0:
            w += 1
        if h % 2 == 0:
            h += 1

        if room_type == 'rect':
            room = rooms.add_rect_room(start, w, h)
        elif room_type == 'rect_cross':
            room = rooms.add_rect_cross_room(start, w, h)
        elif room_type == 'square':
            room = rooms.add_square_room(start, w)
        elif room_type == 'alcove':
            room = rooms.add_rect_alcove_room(start, w, h, type=randint(0, 2))

        return room

    def place_room(self):

        placed = False
        tries = 0
        shared_wall = []

        while not placed:
            if tries >= 100:
                return 'failed'

            room = self.get_new_room()

            corners = room['corners']
            walls = room['walls']
            floor = room['floor']

            conflict = False
            del shared_wall[:]

            for point in corners:

                px, py = point

                if not self.point_is_on_map(point):
                    conflict = True
                    break
                if self.map[px][py] == 'floor':
                    conflict = True
                    break

            if not conflict:
                for point in walls:

                    px, py = point

                    if not self.point_is_on_map(point):
                        conflict = True
                        break
                    if self.map[px][py] == 'floor':
                        conflict = True
                        break
                    if self.map[px][py] == 'wall':
                        shared_wall.append(point)

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

            self.room_count += 1
            room['#'] = str(self.room_count)

            self.rooms[room['#']] = room
            self.room_ids.append(room['#'])

            self.add_tiles(walls, 'wall')
            self.add_tiles(floor, 'floor')
            self.add_tiles(corners, 'fixed_wall')
            placed = True

            # if rooms.add_columns(room):
            #     self.add_tiles(room['columns'], 'wall')

            # initialize zone
            self.zones.append([room['#']])

            if shared_wall:
                connection, door = self.place_shared_door(shared_wall)
                if connection:
                    self.join_shared_door_zones(door)

    def place_shared_door(self, shared_wall):
        valid = self.get_valid_door_locations(shared_wall, 'shared')
        if valid:
            door = choice(valid)
            self.add_tile(door, 'door')
            self.add_lintels(door)
            return True, door
        else:
            return False, (0, 0)

    def get_valid_door_locations(self, wall, door_type):

        valid = []

        for point in wall:
            if self.is_valid_door_location(point, door_type):
                valid.append(point)

        return valid

    def is_valid_door_location(self, (x, y), door_type):

        adj = self.get_adj_tile_dict((x, y))

        keys = adj['directions']
        if not sorted(keys) == sorted(['n', 's', 'e', 'w']):
            return False

        if door_type == 'shared':
            valid_door_posts = ('wall', 'fixed_wall')
            valid_threshold = ('floor',)
            if adj['n'] in valid_door_posts and adj['s'] in valid_door_posts \
                    and adj['e'] in valid_threshold and adj['w'] in valid_threshold:
                return True
            if adj['e'] in valid_door_posts and adj['w'] in valid_door_posts \
                    and adj['n'] in valid_threshold and adj['s'] in valid_threshold:
                return True
            return False

        elif door_type == 'corridor':
            valid_door_posts = ('wall', 'fixed_wall')
            valid_threshold = ('floor', 'corridor')
            if adj['n'] in valid_door_posts and adj['s'] in valid_door_posts and \
                    adj['e'] in valid_threshold and \
                    adj['w'] in valid_threshold and adj['w'] != adj['e']:
                return True
            if adj['e'] in valid_door_posts and adj['w'] in valid_door_posts and \
                    adj['n'] in valid_threshold and \
                    adj['s'] in valid_threshold and adj['s'] != adj['n']:
                return True
            return False

    def add_lintels(self, point):

        adj = self.get_adj_tile_dict(point)

        keys = adj['directions']
        if not sorted(keys) == sorted(['n', 's', 'e', 'w']):
            return False

        valid_door_posts = ('wall', 'fixed_wall')

        lintels = []

        if adj['n'] in valid_door_posts and adj['s'] in valid_door_posts \
                and adj['e'] == 'floor' and adj['w'] == 'floor':
            lintels.extend([adj['n_coord'], adj['s_coord']])
        if adj['e'] in valid_door_posts and adj['w'] in valid_door_posts \
                and adj['n'] == 'floor' and adj['s'] == 'floor':
            lintels.extend([adj['w_coord'], adj['e_coord']])

        self.add_tiles(lintels, 'fixed_wall')

    def fill_in_walls(self):

        new_walls = []

        for y in range(self.ylim):
            for x in range(self.xlim):
                if self.map[x][y] == 'filled':
                    adj = self.get_adj_tile_dict((x, y), diag=True)
                    directions = adj['directions']
                    change = False
                    for d in directions:
                        if adj[d] in ('floor', 'corridor'):
                            change = True
                            break

                    if change:
                        new_walls.append((x, y))

        if new_walls:
            self.add_tiles(new_walls, 'wall')

    # corridor methods

    def is_valid_corridor(self, corridor):
        for x, y in corridor:
            if self.map[x][y] == 'wall' or self.map[x][y] == 'filled':
                pass
            else:
                return False
        return True

    def try_corridor(self, r1, r2_key):
        r2 = self.rooms[r2_key]

        sx, sy = r1['center']
        ex, ey = r2['center']

        if ex > sx:
            h_direction = 'e'
        elif ex <= sx:
            h_direction = 'w'

        if ey > sy:
            v_direction = 's'
        elif ey < sy:
            v_direction = 'n'
        elif ey == sy:
            v_direction = None

        x_dist = abs(sx - ex)
        y_dist = abs(sy - ey)
        if x_dist > y_dist:
            # horizontal_first
            direction = h_direction
        else:
            # vertical_first
            direction = v_direction

        corridor = []

        px, py = sx, sy
        seeking = True

        while seeking:

            if direction == 'n':
                py -= 1
            elif direction == 's':
                py += 1
            elif direction == 'w':
                px -= 1
            elif direction == 'e':
                px += 1

            if direction in ('n', 's') and py == ey:
                direction = h_direction
            elif direction in ('e', 'w') and px == ex:
                direction = v_direction

            if direction is None:
                seeking = False

            if not self.point_is_on_map((px, py)):
                seeking = False

            if (px, py) in r1['floor']:
                continue
            elif (px, py) in r2['floor']:
                seeking = False
            elif self.map[px][py] == 'wall' and (px, py) not in r1['walls'] and (px, py) not in r2['walls']:
                seeking = False
            elif (px, py) in r1['walls'] and (px, py) in r2['walls'] and self.is_valid_door_location((px, py), 'shared'):
                corridor.append((px, py))
                seeking = False
            else:
                corridor.append((px, py))

        return corridor

    def get_nearest(self, room_map, num):
        lowest = sorted(room_map.items(), key=lambda (k, v): v)[:num]
        answer = []
        for key, value in lowest:
            answer.append(key)
        return answer

    def room_dist_map(self, room, keys):
        map = {}

        for k in keys:
            r = self.rooms[k]
            dist = rooms.get_distance(room['center'], r['center'])
            map[r['#']] = dist

        return map

    def door_connects_rooms(self, corridor, r1, r2_key):
        r2 = self.rooms[r2_key]

        start = corridor[0]
        end = corridor[-1]
        if start in r1['walls'] and end in r2['walls']:
            return True
        return False

    def get_corridor(self):

        corridor = []

        for y in range(self.ylim):
            for x in range(self.xlim):
                if self.map[x][y] == 'corridor':
                    corridor.append((x, y))

        return corridor

    def add_corridor_doors(self):
        valid = self.get_valid_door_locations(self.get_corridor(), 'corridor')

        valid = self.remove_adj_doors(valid)

        for point in valid:
            self.add_tile(point, 'door')

    def remove_adj_doors(self, set):
        pairs = []

        for px, py in set:
            adj = ((px, py - 1),
                   (px, py + 1),
                   (px - 1, py),
                   (px + 1, py))
            for p in adj:
                if p in set:
                    pair = sorted([(px, py), p])
                    pairs.append(pair)

        unique_pairs = []
        for p in pairs:
            if p not in unique_pairs:
                unique_pairs.append(p)

        remove_list = []
        for p in unique_pairs:
            remove_list.append(choice(p))

        for e in remove_list:
            set.remove(e)

        return set

    # zone methods

    def connect_zones(self):
        unconnected = True
        count = 0
        extra_corridors = 0

        while True:

            count += 1
            if count > 1000 and unconnected:
                print 'Fail'
                return 'unconnected'
            elif count > 1000 and not unconnected:
                return 'connected'
            elif len(self.zones) == 1:
                unconnected = False
            elif not unconnected and extra_corridors >= self.number_of_extra_corridors:
                return 'connected'

            zone = choice(self.zones)
            room = self.rooms[choice(zone)]

            if unconnected:
                targets = self.get_rooms_from_other_zones(zone)
            else:
                targets = self.get_rooms_from_other_zones(None)

            distance_map = self.room_dist_map(room, targets)

            if 3 <= len(targets):
                sample_size = 3
            else:
                sample_size = len(targets)

            target_rooms = self.get_nearest(distance_map, sample_size)
            target_room = choice(target_rooms)

            corridor = self.try_corridor(room, target_room)
            if corridor and self.is_valid_corridor(corridor) and self.door_connects_rooms(corridor, room, target_room):
                self.add_tiles(corridor, 'corridor')
                if unconnected:
                    zones = [room['#'], target_room]
                    self.join_zones(zones)
                elif not unconnected:
                    extra_corridors += 1

    def join_zones(self, join_zones):
        state = '1'
        for zone in self.zones:
            for room in zone:
                if room in join_zones and state == '1':
                    z1 = zone
                    state = '2'
                elif room in join_zones and state == '2':
                    z2 = zone
        self.zones.remove(z1)
        self.zones.remove(z2)
        z1.extend(z2)
        self.zones.append(z1)

    def join_shared_door_zones(self, door):
        adj = self.get_adj_tile_dict(door)
        directions = adj['directions']
        thresholds = []
        for d in directions:
            x, y = adj['%s_coord' % d]
            if self.map[x][y] == 'floor':
                thresholds.append((x, y))
        zones = []
        for t in thresholds:
            for room in self.rooms.values():
                if t in room['floor']:
                    zones.append(room['#'])

        if len(zones) == 2:
            self.join_zones(zones)
        else:
            print "can't join"
            return False

    def get_rooms_from_other_zones(self, restricted):
        answer = []

        for zone in self.zones:
            if zone == restricted:
                continue
            else:
                for room in zone:
                    answer.append(room)

        return answer

    def get_zone(self, r_key):
        for zone in self.zones:
            if r_key in zone:
                return zone
