import effect
from pygame.transform import rotate


class Spin(effect.Effect):
    
    def __init__(self, mng, type, image, coord, speed=20.0, d=-1.0):
        
        effect.Effect.__init__(self, mng, type, coord)
        
        self.original = image.copy()
        
        self.image = self.original.copy()
        
        self.x, self.y = coord
        self.x += 16
        self.y += 24
        
        self.image_rect.center = self.x, self.y
        
        # speed is how many frames a complete rotation should take.
               
        self.rotate = 360.0 / speed * dir
        
    def run(self):
        
        self.image = self.original.copy()
        self.image = rotate(self.image, self.rotate * float(self.frame))
        self.image_rect = self.image.get_rect()
        
        if self.step():
            self.complete = True
 
        if self.complete:
            self.end() 