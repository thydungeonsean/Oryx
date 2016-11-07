from random import *
import image


class AvatarGen(object):
    
    bodya = ('man1', 'man2', 'man3', 'man4', 'man6')
    bodyb = ('man3', 'man4', 'man6')
    bodyc = ('man5',)
    
    hand_weapons = (
        'dagger1',
        'dagger2',
        'dagger3',
        'dagger4',
        'dagger5',
        'sword1',
        'sword2',
        'scimitar1',
        'scimitar2',
        'sword3',
        'sword4',
        'sword5',
        'axe1',
        'axe2',
        'hammer1',
        'hammer2',
        'club1',
        'club2',
        'mace1',
        'mace2',
        'morning_star1',
        'morning_star2',
        'spear1',
        'staff1',
        'halberd',
        'spear2',
        'scythe',
        'staff2',
        'staff3',
        'staff4',
        'staff5',
        'staff6',
        'symbol1',
        'symbol2',
        'symbol3'
    )
    
    range_weapons = (
        'bow1',
        'bow2',
        'bow3',
        'bow4',
        'bow5',
        'bow6',
        'bow7',
        'sling'
    )
    
    heads = tuple(['head%s' % h for h in range(1, 22)])
    
    shields = tuple(['shield%s' % s for s in range(1, 14)])
    
    cloaks = tuple(['cape%s' % c for c in range(1, 6)])
    
    tails = ('tail1', 'tail2')
    
    wings = ('wing',)
    
    rows = ('bodies', 'hand_weapons', 'range_weapons', 'heads', 'shields', 'cloaks', 'tails', 'wings')

    
    """
    set mode to 'default' for designing an avatar
    set to:
    'random' for completely random avatar
    'melee' for single weapon or weapon and shield
    'single' for one weapon
    'weapon+shield' for weapon and shield
    'ranged' for ranged
    """
    def __init__(self, mode='default', cloak=50, human=True, wing=15, tail=30, preset=None):
        
        """ method is choose weapon, weapon + shield, ranged weapon
        Then, if there are multiple bodies available, choose one
        then choose head, cloak, wings, tail
        """
        
        self.set = 'a'

        self.layer = {
            'body': None,
            'weapon': None,
            'head': None,
            'shield': None,
            'cloak': None,
            'wing': None,
            'tail': None
        }
        
        self.row_to_layer_dict = {
            'bodies': 'body',
            'hand_weapons': 'weapon',
            'range_weapons': 'weapon',
            'heads': 'head',
            'shields': 'shield',
            'cloaks': 'cloak',
            'tails': 'tail',
            'wings': 'wing'
            }
        
        self.human = human
        self.cloak_chance = cloak
        self.wing_chance = wing
        self.tail_chance = tail
        
        if mode == 'actor' and preset is not None:
            self.preset_generate(preset)
        elif mode != 'default':
            if mode == 'actor':
                mode = 'random'
            self.random_generate(mode)
        else:
            self.default_generate()
            
        # for building an avatar
        
        a = AvatarGen
        
        self.cursor_x = 0
        self.cursor_y = 0
        
        self.rows = a.rows
        self.row_dict = {
                'bodies': {
                    'a': a.bodya,
                    'b': a.bodyb,
                    'c': a.bodyc,
                    'd': a.bodya
                    },
                'hand_weapons': a.hand_weapons,
                'heads': a.heads,
                'range_weapons': a.range_weapons,
                'shields': a.shields,
                'cloaks': a.cloaks,
                'tails': a.tails,
                'wings': a.wings
                }
        self.row_pos = {
                'bodies': {
                    'a': 0,
                    'b': 0,
                    'c': 0,
                    'd': 0
                    },
                'hand_weapons': -1,
                'heads': -1,
                'range_weapons': -1,
                'shields': -1,
                'cloaks': -1,
                'tails': -1,
                'wings': -1
                }

    def get_image_package(self, color):

        custom = {'body': self.layer['body'],
                  'head': self.layer['head'],
                  'weapon': self.layer['weapon'],
                  'shield': self.layer['shield'],
                  'cloak': self.layer['cloak'],
                  'wings': self.layer['wing'],
                  'tail': self.layer['tail']
                  }

        package = ('custom', custom, color)

        return package

    def default_generate(self):
    
        self.layer['body'] = 'man1'
        
    def preset_generate(self, preset):
        
        self.load_presets(preset)
        
    def load_presets(self, preset):
        
        layers = ('body', 'weapon', 'head', 'shield', 'cloak',
                  'wing', 'tail')
                  
        for key in preset.keys():
            self.layer[key] = preset[key]
            
        for layer in layers:
            if layer not in preset.keys():
                self.layer[key] = None
    
    def random_generate(self, weapon):

        layers = ('body', 'weapon', 'head', 'shield', 'cloak',
                  'wing', 'tail')

        for l in layers:
            self.layer[l] = None

        set = 'a'
        if weapon == 'random':
            set = choice(('a', 'a', 'a', 'b', 'b', 'b', 'c', 'c', 'a'))
        elif weapon == 'ranged':
            set = 'c'
        elif weapon == 'melee':
            set = choice(('a', 'b'))
        elif weapon == 'single':
            set = 'a'
        elif weapon == 'weapon+shield':
            set = 'b'
            
        self.set = set
            
        if set == 'a':
            self.layer['weapon'] = choice(AvatarGen.hand_weapons)
            self.layer['body'] = choice(AvatarGen.bodya)
        elif set == 'b':
            self.layer['weapon'] = choice(AvatarGen.hand_weapons)
            self.layer['body'] = choice(AvatarGen.bodyb)
            self.layer['shield'] = choice(AvatarGen.shields)
        elif set == 'c':
            self.layer['weapon'] = choice(AvatarGen.range_weapons)
            self.layer['body'] = choice(AvatarGen.bodyc)
        elif set == 'd':
            self.layer['body'] = choice(AvatarGen.bodya)
        
        if randint(0, 99) < 95:
            self.layer['head'] = choice(AvatarGen.heads)
            
        if randint(0, 99) < self.cloak_chance:
            self.layer['cloak'] = choice(AvatarGen.cloaks)
            
        if not self.human:
            if randint(0, 99) < self.wing_chance:
                self.layer['wing'] = choice(AvatarGen.wings)
            if randint(0, 99) < self.tail_chance:
                self.layer['tail'] = choice(AvatarGen.tails)
                
    def get_avatar_image(self, color):

        l = self.layer
        return image.AnimatedAvatar(l['body'], l['head'], l['weapon'], l['shield'], l['cloak'], l['wing'], l['tail'],
                                 color)

    def current_row(self, y):

        if self.rows[y] == 'bodies':
            row = self.row_dict['bodies'][self.set]
        else:
            row = self.row_dict[self.rows[y]]

        return row

    def update_row_pos(self, x, y):

        if self.rows[y] == 'bodies':
            self.row_pos['bodies'][self.set] = x
        else:
            self.row_pos[self.rows[y]] = x

    def current_x_pos(self, y):

        if self.rows[y] == 'bodies':
            x = self.row_pos['bodies'][self.set]
        else:
            x = self.row_pos[self.rows[y]]

        return x

    def control(self, key):
    
        x = self.cursor_x
        y = self.cursor_y

        # let key press affect cursor position
        move = False
        if key == 'right':
            x += 1
            move = 'hor'
        elif key == 'left':
            x -= 1
            move = 'hor'
        elif key == 'up':
            y -= 1
            move = 'vert'
        elif key == 'down':
            y += 1
            move = 'vert'
            
        elif key == 'random':
            self.random_generate('random')
        
        # changed row
        if move == 'vert':
            # update the row and column being displayed
            if y < 0:
                y = len(self.rows)-1
            if y > len(self.rows)-1:
                y = 0
            x = self.current_x_pos(y)

        # set the current row
        row = self.current_row(y)

        # changed column along row
        if move == 'hor':
            
            min = -1
            max = len(row) - 1
            if self.rows[y] == 'bodies':
                min = 0  # always have at least one body displayed
        
            # check cursor pos on row
            if x > max:
                x = min
            elif x < min:
                x = max

            self.update_row_pos(x, y)
            
            # update the avatar image
            self.adjust_avatar(row, x, y)
            
        self.cursor_x = x
        self.cursor_y = y
            
    def adjust_avatar(self, row, x, y):

        if x == -1:
            value = None
        else:
            value = row[x]
            
        row_name = self.rows[y]
        layer_key = self.row_to_layer_dict[row_name]
        
        self.layer[layer_key] = value
        
        # make sure we're setting the correct body type for weapon/shield layout
        if row_name == 'range_weapons' and x != -1:
            self.set = 'c'
            self.adjust_body()
            self.remove_layer('shield')
        elif row_name == 'hand_weapons':
            if self.layer['shield'] is not None:
                self.set = 'b'
                self.adjust_body()
            else:
                self.set = 'a'
                self.adjust_body()
        elif row_name == 'shields' and x != -1:
            self.set = 'b'
            self.adjust_body()
            if self.row_pos['range_weapons'] != -1:
                self.remove_layer('weapon')
        elif row_name == 'shields' and x == -1:
            self.set = 'a'
        elif row_name == 'range_weapons' and x == -1:
            self.set = 'a'
            self.adjust_body()
        
    def remove_layer(self, id):
        
        if id == 'bodies':
            return
        
        if self.layer[id] is not None:
            self.layer[id] = None
            self.row_pos[self.rows[self.cursor_y]] = -1
        
    def adjust_body(self):
        
        # current body type invalid
        if self.layer['body'] not in self.row_dict['bodies'][self.set]:
            row = self.row_dict['bodies'][self.set]
            x = self.row_pos['bodies'][self.set]
            self.layer['body'] = row[x]
