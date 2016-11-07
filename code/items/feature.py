

class Feature(object):

    def __init__(self, type, id, map, point):

        self.type = type
        self.id = id

        self.map = map
        self.x, self.y = point

        # blocks line of sight
        self.blocks = False

        # permanent means feature is drawn at map generation
        # otherwise it is drawn by main display when on screen
        # permanent features should not be mutable or walkable
        # non permanent needs an image
        self.permanent = True
        self.needs_draw = False

    @property
    def coord(self):
        return self.x, self.y


class Entrance(Feature):

    def __init__(self, id, map, point):

        Feature.__init__(self, 'entrance', id, map, point)
        self.blocks = True


class Lintel(Feature):

    def __init__(self, id, map, point):

        Feature.__init__(self, 'lintel', id, map, point)
        self.blocks = True
        self.image = self.map.get_tile_image('ver_wall')


class Door(Feature):

    def __init__(self, id, map, point):

        Feature.__init__(self, 'door', id, map, point)

        self.permanent = False
        self.image = self.map.get_tile_image('close_door')

        self.needs_draw = True
        self.closed = True
        self.blocks = True

    def toggle(self):

        if self.closed:
            self.closed = False
            self.blocks = False
            self.needs_draw = True
        else:
            self.closed = True
            self.blocks = True
            self.needs_draw = False

    def render(self, frame='a'):

        return self.image.render()


class Column(Feature):

    def __init__(self, id, map, point):

        Feature.__init__(self, 'column', id, map, point)

        self.blocks = True
        self.cracked = False
        self.broken = False

    def crack_column(self):
        self.cracked = True

    def break_column(self):
        self.broken = True
        self.cracked = False
        self.blocks = False


class Stalagmite(Feature):

    def __init__(self, id, map, point):

        Feature.__init__(self, 'stalagmite', id, map, point)

        self.blocks = True
        self.image_id = 'stalagmite'

    def alternate(self):
        self.image_id = 'stalagtite'
