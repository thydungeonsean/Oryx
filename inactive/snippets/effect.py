class Effect(object):

    """ An effect is some sort of special visual object that will be displayed on the screen. It can 
    be an animated sprite, or a projectile or glow. An effect have a lerp so it will move.
    it will be rendered by render_effects function in render. The effect is owned by the effects list
    in the current battle state and will disappear when it is complete. """

    def __init__(self, mng, type, coord):
        
        # owned by the battle state so the effect can terminate itself when complete.
        self.mng = mng
        self.type = type
        self.coord = coord
        
        self.offx = 0
        self.offy = 0
                
        self.complete = False
        self.frame = 0
        self.maxFrame = 0
        self.delay = 0

        self.image = None
        self.image_rect = None
        
    def run(self):

        if self.step():
            self.complete = True
 
        if self.complete:
            self.end()
            
    def step(self):
        if self.delay > 0:
            self.delay -= 1
        else:
            self.frame += 1
                    
        if self.frame == self.maxFrame:
            return True
        else:
            return False
    
    def render(self):

        return self.image, self.image_rect
    
    def end(self):
        
        self.mng.effects.remove(self)