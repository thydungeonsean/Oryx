from random import *
from image import AnimatedSprite
from image import AnimatedAvatar
from image import CopiedAnimatedSprite
from control_component import ActorControlComponent
import mobility


class Actor(object):
    
    def __init__(self, name, image_package, stat_component, mobility_component='ground'):
        
        self.stats = stat_component
        self.mobility = self.set_mobility(mobility_component)
        self.control = ActorControlComponent(self)
        
        self.name = name
        self.hp = self.stats.max_health

        self.map = None
        self.x = 0
        self.y = 0

        # image package is 3 part tuple:
        # image type - standard is pregen monster from monsters tilesheet
        # image_id - key for monsters tilesheet
        # color for image
        self.image = self.set_image(image_package)

    @property
    def coord(self):
        return self.x, self.y

    # initializing
    def set_image(self, image_package):
        
        if image_package[0] == 'standard':
            type, id, color = image_package
            image = AnimatedSprite(id, color)
        elif image_package[0] == 'custom':
            type, custom, color = image_package
            body = custom['body']
            head = custom['head']
            weapon = custom['weapon']
            shield = custom['shield']
            cloak = custom['cloak']
            wings = custom['wings']
            tail = custom['tail']
            image = AnimatedAvatar(body, head, weapon, shield, cloak, wings, tail, color)
        elif image_package[0] == 'preloaded':
            type, image, color = image_package
            
        return image

    @staticmethod
    def copy_image(actor):
        return CopiedAnimatedSprite(actor.image)

    def set_mobility(self, preset):

        return mobility.MobilityComponent(self, preset)

    def add_to_map(self, map, (x, y)):

        self.map = map
        self.x = x
        self.y = y

    # combat        
    def take_hit(self, damage, blocked=False):
        
        self.hp -= damage
        
        if self.hp <= 0:
            self.hp = 0
            
            self.die()
            
    def die(self):
        
        pass
        
    def attack(self, target):
        
        a = self.stats
        t = target.stats
        
        if randint(1, 100) > t.dodge_chance(a):
            # hit!
            damage = a.damage(t)
            if damage == 0:
                blocked = True
            target.take_hit(damage, blocked)

    def render(self, frame='a'):

        i, r = self.image.render(frame=frame)

        return i, r

    def try_move(self, direction):

        if direction == 'up':
            move = self.x, self.y - 1
        elif direction == 'down':
            move = self.x, self.y + 1
        elif direction == 'right':
            move = self.x + 1, self.y
        elif direction == 'left':
            move = self.x - 1, self.y

        bump = False
        walkable = False
        if self.valid_move(move):
            walkable = True

        if walkable and not bump:
            self.position(move)

    def valid_move(self, (mx, my)):

        terrain = self.map.map[mx][my]
        if terrain in self.mobility.walkable:
            return True
        else:
            return False

    def position(self, (mx, my)):
        self.x = mx
        self.y = my


class Monster(Actor):
    
    def __init__(self, monster_set, name, image_package, stat_component, mobility_component='ground'):

        self.monster_set = monster_set
        Actor.__init__(self, name, image_package, stat_component, mobility_component)

    # initializing
    def set_image(self, image_package):

        for monster in self.monster_set.monsters:
            # if this monster has already been created, duplicate it's image
            # in theory this is faster than creating new Animated Sprite objects?
            if self.name == monster.name:
                image = self.copy_image(monster)
                return image

        if image_package[0] == 'standard':
            type, id, color = image_package
            image = AnimatedSprite(id, color)
        elif image_package[0] == 'custom':
            type, custom, color = image_package
            body = custom['body']
            head = custom['head']
            weapon = custom['weapon']
            shield = custom['shield']
            cloak = custom['cloak']
            wings = custom['wings']
            tail = custom['tail']
            image = AnimatedAvatar(body, head, weapon, shield, cloak, wings, tail, color)
        elif image_package[0] == 'preloaded':
            type, image, color = image_package

        return image

