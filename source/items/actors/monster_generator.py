from actor import Monster
import stat_component
from ...constants import *
import os


class MonsterGenerator(object):

    defaults = {
            'name': 'none',
            'image': 'knight',
            'color': 'owhite',
            'health': 1,
            'attack': 1,
            'block': 0,
            'dodge': 0,
            'accuracy': 0,
            'base_health': 0,
            'base_attack': 0,
            'health_quality': 'good',
            'attack_quality': 'trained',
            'image_type': 'standard',
            'body': 'man1',
            'head': None,
            'weapon': None,
            'shield': None,
            'cloak': None,
            'wings': None,
            'tail': None
            }
            
    actor_keys = ('name', 'image', 'color', 'image_type')
            
    string_keys = ('name', 'image', 'health_quality', 'attack_quality', 'image_type')

    avatar_keys = ('body', 'head', 'weapon', 'shield', 'cloak', 'wings', 'tail')

    def __init__(self, monster_set):
        self.monster_set = monster_set

    def create_monster(self, monster_list, name):
        
        monster_data = self.get_monster_data(monster_list, name)
        if not monster_data:
            return False
            
        actor_settings, stat_settings = self.load_monster_stats(monster_data)
        
        stats = self.create_stat_component(stat_settings)
        actor = self.create_actor(actor_settings, stats)
        
        return actor
            
    def create_actor(self, settings, stats):
        
        name = settings['name']
        image_type = settings['image_type']
        color = settings['color']

        if image_type == 'standard':
            image_id = settings['image']
            image_package = (image_type, image_id, color)
        elif image_type == 'custom':
            mg = MonsterGenerator
            custom = {}
            for key in mg.avatar_keys:
                custom[key] = settings[key]
            image_package = (image_type, custom, color)
        
        new = Monster(self.monster_set, name, image_package, stats)
        
        return new
    
    def create_stat_component(self, stat_settings):
        
        hl = stat_settings['health']
        at = stat_settings['attack']
        bl = stat_settings['block']
        dg = stat_settings['dodge']
        ac = stat_settings['accuracy']
        bs_hl = stat_settings['base_health']
        bs_at = stat_settings['base_attack']
        hl_ql = stat_settings['health_quality']
        at_ql = stat_settings['attack_quality']
        
        new = stat_component.StatComponent(hl, at, bl, dg, ac, bs_hl, bs_at, hl_ql, at_ql)
        
        return new
        
    def get_monster_data(self, monster_list, name):
        
        import_path = ''.join((os.path.dirname(__file__), '\\..\\..\\..\\data\\'))
        f = open(''.join((import_path, 'monsters\\', monster_list, '.mon')), 'r')

            
        monster_data_lines = []
        found = False
        
        for line in f:
        
            if not found:
                if line.startswith('<<< %s' % name):
                    found = True
            
            elif found:
                if line.startswith('>>>'):
                    break
                else:
                    monster_data_lines.append(line)
        
        f.close()
        
        if not found:
            print 'monster not in monster set.'
            return False
            
        monster_data = {}
            
        for line in monster_data_lines:
            tag, value = line.split(': ')
            tag = tag.strip()
            value = value.strip()
            monster_data[tag] = value
            
        return monster_data
        
    def get_monster_data_value(self, data, key):
    
        mg = MonsterGenerator
    
        if key == 'color':
            return color_key[data[key]]
        elif key in mg.string_keys:
            return data[key]
        elif key in mg.avatar_keys:
            layer = data[key]
            if layer == 'none':
                layer = None
            return layer
        else:
            return int(data[key])
        
    def load_monster_stats(self, data):
        
        mg = MonsterGenerator
        
        actor_dict = {}
        stat_dict = {}
        
        # if nothing in monster data is specified for a value, use default
        for key in mg.defaults.keys():
            if key not in data.keys():
                if key in mg.actor_keys:
                    actor_dict[key] = mg.defaults[key]
                elif key in mg.avatar_keys:
                    actor_dict[key] = mg.defaults[key]
                else:
                    stat_dict[key] = mg.defaults[key]
                    
        # set the values from monster data
        for key in data.keys():
            if key in mg.actor_keys:
                actor_dict[key] = self.get_monster_data_value(data, key)
            elif key in mg.avatar_keys:
                actor_dict[key] = self.get_monster_data_value(data, key)
            else:
                stat_dict[key] = self.get_monster_data_value(data, key)

        return actor_dict, stat_dict
