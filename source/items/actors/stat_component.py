

class StatComponent(object):

    attack = {
            'weak': 15,
            'trained': 20,
            'mighty': 25
            }
            
    health = {
            'frail': 40,
            'good': 50,
            'robust': 60
            }
            
    block = {'normal': 5}
            
    dodge = {'normal': 10}
    
    accuracy = {'normal': 5}

    def __init__(self, health, attack, block=0, dodge=0, accuracy=0, base_health=0, base_attack=0,
                 health_quality='normal', attack_quality='trained'):
        
        # to allow some variation in starting health and attack
        self.base_health = base_health
        self.base_attack = base_attack
        
        # number of "orbs" for each stat
        self.health_orbs = health
        self.attack_orbs = attack
        self.block_orbs = block
        self.dodge_orbs = dodge
        self.accuracy_orbs = accuracy
        
        # quality of orbs for health and attack
        self.health_quality = health_quality
        self.attack_quality = attack_quality
        
        self.current_health_quality = health_quality
        self.current_attack_quality = attack_quality
        
        # straight bonuses to stats from effects
        self.bonus_health = 0
        self.bonus_attack = 0
        self.bonus_block = 0
        self.bonus_dodge = 0
        self.bonus_accuracy = 0
    
    def reset(self):
        
        self.current_health_quality = self.health_quality
        self.current_attack_quality = self.attack_quality
    
    @property
    def health_orb_value(self):
        
        sc = StatComponent
        
        return sc.health[self.current_health_quality]
        
    @property
    def attack_orb_value(self):
        
        sc = StatComponent
        
        return sc.attack[self.current_attack_quality]
    
    @property
    def block_orb_value(self):
        
        sc = StatComponent
        
        return sc.block['normal']
        
    @property
    def dodge_orb_value(self):
        
        sc = StatComponent
        
        return sc.dodge['normal']
    
    @property
    def accuracy_orb_value(self):
        
        sc = StatComponent
        
        return sc.accuracy['normal']
    
    @property
    def max_health(self):
    
        return self.base_health + (self.health_orbs * self.health_orb_value) + self.bonus_health
    
    @property
    def attack(self):
        
        return self.base_attack + (self.attack_orbs * self.attack_orb_value) + self.bonus_attack
        
    @property
    def block(self):
        
        return (self.block_orbs * self.block_orb_value) + self.bonus_block
        
    @property
    def dodge(self):
    
        return (self.dodge_orbs * self.dodge_orb_value) + self.bonus_dodge
        
    @property
    def accuracy(self):
        
        return (self.accuracy_orbs * self.accuracy_orb_value) + self.bonus_accuracy
        
    def dodge_chance(self, attacker):
        
        chance = self.dodge - attacker.accuracy
        if chance < 0:
            chance = 0
            
        return chance
        
    def damage(self, target):
        
        damage = self.attack - target.block
        
        if damage < 0:
            damage = 0
            
        return damage
