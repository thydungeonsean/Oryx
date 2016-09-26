

class MobilityComponent(object):

    walkable = {
        'ground': ('floor', 'corridor', 'door', 'road', 'field', 'ground',  'forest', 'shallow', 'w_feature'),
        'float': ('pit', 'water'),
        'sea': ('water', 'shallow', 'depth')
    }

    def __init__(self, owner, preset='ground'):

        self.owner = owner

        mc = MobilityComponent

        self.walkable = list(mc.walkable[preset])
