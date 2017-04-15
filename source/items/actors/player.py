import source.graphics.image as img
import source.graphics.avatar_gen as ag
from source.constants import *
from actor import Actor
from source.graphics.avatar_gen import AvatarGen
import stat_component


class Player(Actor):
    def __init__(self):

        name = 'Jorgen'

        # premade image
        # image_packet = ('standard', 'rogue', RED)

        # custom image
        ag = AvatarGen('random')
        image_packet = ag.get_image_package(RED)

        stats = self.create_stat_component()

        Actor.__init__(self, name, image_packet, stats)

    def create_stat_component(self):

        hl = 4
        at = 1
        bl = 0
        dg = 1
        ac = 0
        bs_hl = 5
        bs_at = 5
        hl_ql = 'good'
        at_ql = 'trained'

        new = stat_component.StatComponent(hl, at, bl, dg, ac, bs_hl, bs_at, hl_ql, at_ql)

        return new


class PlayerOld(object):

    def __init__(self):

        self.image = img.AnimatedSprite('centaur_chief', color=RED)

        #self.image = img.AvatarImage('man11', 'head1', 'sword1', color=BLUE)

        a = ag.AvatarGen(mode='random')
        #self.image = a.get_avatar_image(YELLOW)

        self.x = PLAYERRELX
        self.y = PLAYERRELY

        self.image.position((self.x*TILEWIDTH, self.y*TILEHEIGHT))

        self.moved = False

    @property
    def coord(self):
        return self.x, self.y

    def move(self, direction):

        if direction == 'up':
            self.y -= 1
        elif direction == 'down':
            self.y += 1
        elif direction == 'right':
            self.x += 1
        elif direction == 'left':
            self.x -= 1

        self.moved = True


    def render(self, frame='a'):

        return self.image.render(frame)
