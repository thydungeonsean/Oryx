

class Settlement(object):

    def __init__(self, world, (x, y)):

        # domestic
        self.name = 'Almay'
        self.population = 100
        self.race = 'human'
        self.happiness = 0
        self.unrest = 0

        # world map
        self.world = world
        self.x = x
        self.y = y
        self.territory = []
        self.borders = []
        self.image = None
        self.terrain = self.world.map[x][y]

        # politics
        self.allies = []
        self.enemies = []
        self.trade = 0
        self.resources = []

    def ally_with(self, target):

        try:
            self.enemies.remove(target)
        except ValueError:
            pass

        self.allies.append(target)

    def war_with(self, target):

        try:
            self.allies.remove(target)
        except ValueError:
            pass

        self.enemies.append(target)

