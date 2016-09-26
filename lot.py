import random
import room


class Lot(object):

    def __init__(self, owner_map, id, type, topleft, w, h):
        
        self.owner_map = owner_map
        self.seed = int(str(self.owner_map.seed)+id)
        random.seed(self.seed)
        
        self.topleft = topleft
        self.w = w
        self.h = h
        
        self.map = [['blank'for y in range(h)]for x in range(w)]
        
    def load(self):
        
        sx, sy = self.topleft
        xrange = range(sx, sx+self.w)
        yrange = range(sy, sy+self.h)
        
        for y in range(yrange):
            for x in range(xrange):
                
                ax = x - sx
                ay = y - sy
                if self.map[ax][ay] != 'blank':
                    self.owner_map.add_tile((x, y), self.map[ax][ay])
                    
        # need to load features as well

    def create(self):
        pass
