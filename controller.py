

class Controller(object):

    def __init__(self, gamestate):

        self.GS = gamestate

        self.controlled = [self.GS.player]

    def up(self):

        for object in self.controlled:
            object.control.up()

    def down(self):

        for object in self.controlled:
            object.control.down()

    def right(self):

        for object in self.controlled:
            object.control.right()

    def left(self):

        for object in self.controlled:
            object.control.left()
