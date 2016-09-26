from random import *
import monster_generator as mg
import fov_map as fov


class MonsterSet(object):

    packs = ('kobolds',)

    roles = ('minion', 'soldier', 'skirmish', 'range')

    distribution = {
        'minion': .3,
        'soldier': .2,
        'skirmish': .3,
        'range': .2
    }

    walkable = {
        'dungeon': ('floor', 'corridor'),
        'cave': ('floor',),
        'rural': ('ground', 'field', 'floor', 'road')
    }

    def __init__(self, map, sd, (pack, number)):

        self.seed = sd
        seed(self.seed)

        self.map = map
        self.map_type = map.map_type
        self.pack = pack
        self.number = number

        self.monster_types = self.get_monster_types()
        self.monster_list = []
        self.monsters = []

        self.generate_monsters()

    def get_monster_types(self):

        try:
            f = open('data/packs/%s.mpack' % self.pack, 'r')
        except IOError:
            print 'file not found'
            return

        types = {
            'skirmish': [],
            'soldier': [],
            'range': [],
            'minion': []
        }

        for line in f:
            if line == "":
                return types

            name, role = line.split(': ')
            role = role.strip()

            types[role].append(name)

        f.close()
        return types

    def generate_monsters(self):

        gen = mg.MonsterGenerator(self)

        self.get_monster_list()
        for monster in self.monster_list:
            self.monsters.append(gen.create_monster(self.pack, monster))

        self.position_monsters()

    def get_monster_list(self):

        ms = MonsterSet

        extra_weight = 1.0
        monster_dist = {'extra': 0}
        for role in ms.distribution.keys():
            try:
                monster_dist[role] = int(self.number * ms.distribution[role])
                extra_weight -= ms.distribution[role]
            except KeyError:
                pass

        monster_dist['extra'] += int(self.number * extra_weight)

        for role in monster_dist.keys():
            for i in range(monster_dist[role]):
                if role == 'extra':
                    r = choice(ms.roles)
                    self.monster_list.append(choice(self.monster_types[r]))
                else:
                    self.monster_list.append(choice(self.monster_types[role]))

    def position_monsters(self):

        free = self.get_valid_monster_positions()

        for monster in self.monsters:
            coord = choice(free)
            free.remove(coord)
            monster.add_to_map(self.map, coord)

    def get_valid_monster_positions(self):

        # make it so no monsters visible from entrance point
        entrance = self.map.feature_map.features['ent1']
        fov_temp = fov.Calc_Only_FOV(centered_entity=entrance)
        fov_temp.load_map(self.map)

        ms = MonsterSet

        walkable_types = ms.walkable[self.map_type]
        walkable = []
        for type in walkable_types:
            for point in self.map.tiles[type]:
                if point not in fov_temp.visible:
                    walkable.append(point)

        return walkable
