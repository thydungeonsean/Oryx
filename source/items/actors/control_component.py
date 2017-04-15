

class ControlComponent(object):

    def __init__(self, owner):

        self.owner = owner

    def up(self):
        pass

    def down(self):
        pass

    def right(self):
        pass

    def left(self):
        pass

    def space(self):
        pass


class ActorControlComponent(ControlComponent):

    def __init__(self, owner):

        ControlComponent.__init__(self, owner)

    def up(self):
        self.owner.try_move('up')

    def down(self):
        self.owner.try_move('down')

    def right(self):
        self.owner.try_move('right')

    def left(self):
        self.owner.try_move('left')
