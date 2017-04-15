from ..constants import *
import pygame
import math
import tileset as ts


class Calc_Only_FOV(object):
    block_tiles = ('wall', 'fixed_wall', 'bl_feature', 'tree', 'filled', 'close_door')

    sin_table = []
    cos_table = []

    for angle in range(360):
        sin_table.append(math.sin(angle))
        cos_table.append(math.cos(angle))

    def __init__(self, owner_map=None, centered_entity=None):

        self.map = {}

        self.visible = []

        self.owner_map = owner_map
        self.centered_entity = centered_entity

    @property
    def center(self):
        return self.centered_entity.coord

    def load_map(self, owner_map):

        self.owner_map = owner_map
        om = self.owner_map

        del self.map
        self.map = {}

        for y in range(om.ylim):
            for x in range(om.xlim):

                blocked = self.check_blocked((x, y))
                self.map[(x, y)] = blocked

        self.run()

    def check_blocked(self, (x, y)):
        tile = self.owner_map.map[x][y]
        if tile in FOV_Map.block_tiles:
            return True
        if tile == 'door' and self.door_closed((x, y)):
            return True
        try:
            # a way to make features block line of sight
            fm = self.owner_map.feature_map
            f = fm.feature_at_point[(x, y)]
            if self.feature_blocks((x, y)):
                return True
        except KeyError:
            pass

        return False

    def door_closed(self, point):

        id = 'door%s' % str(point)
        door = self.owner_map.feature_map.features[id]

        if door.closed:
            return True
        else:
            return False

    def feature_blocks(self, point):

        fm = self.owner_map.feature_map
        feature = fm.feature_at_point[point]

        if feature.blocks:
            return True
        else:
            return False

    def run(self):

        visible = self.get_visible_spaces()
        del self.visible
        self.visible = visible

    def get_visible_spaces(self):

        visible = []

        for angle in range(0, 360, 1):
            visible = self.cast_angle_ray(angle, visible)

        return visible

    def cast_angle_ray(self, angle, visible):

        sx, sy = self.center

        x = float(sx * TILEWIDTH)
        y = float(sy * TILEHEIGHT)

        mapw = (self.owner_map.xlim - 1) * TILEWIDTH
        maph = (self.owner_map.ylim - 1) * TILEHEIGHT

        radius = scale(16)

        for r in range(0, radius, int(SCALE)):
            x += r * FOV_Map.cos_table[angle]
            y += r * FOV_Map.sin_table[angle]

            if x < -TILEWIDTH or x > mapw or y < -TILEHEIGHT or y > maph:
                break

            gx = int(round(x / TILEWIDTH))
            gy = int(round(y / TILEHEIGHT))

            if (gx, gy) not in visible:
                visible.append((gx, gy))

            try:
                if self.map[(gx, gy)] and (gx, gy) != self.center:
                    break
            except KeyError:
                break

        return visible


class FOV_Map(Calc_Only_FOV):

    def __init__(self, owner_map=None, centered_entity=None, on=False):

        Calc_Only_FOV.__init__(self, owner_map, centered_entity)

        self.last_center = None

        self.on = on
        
        self.image = pygame.Surface((DISPLAYW, DISPLAYH))
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        
        self.fog = pygame.Surface((TILEWIDTH, TILEHEIGHT))
        self.fog.fill(NR_BLACK)
        self.fog = self.fog.convert()
        self.fog_rect = self.fog.get_rect()

        self.edges = ts.TileSet('fog')

    @property
    def view_coord(self):
        x, y = self.center
        return x - PLAYERRELX, y - PLAYERRELY

    def toggle_fog(self):

        if self.on:
            self.on = False
        else:
            self.on = True

    def get_relative_coord(self, (x, y)):
        vx, vy = self.view_coord
        return x - vx, y - vy

    def run(self):

        if not self.on:
            return

        if self.last_center != self.center:
            visible = self.get_visible_spaces()
            del self.visible
            self.visible = visible
            self.update_fog(visible)

    def update_fog(self, visible):

        self.last_center = self.center

        self.image.fill(WHITE)
        field = []
        visible_field = []

        for point in visible:
            rel_point = self.get_relative_coord(point)
            visible_field.append(rel_point)

        for y in range(11):
            for x in range(19):
                if (x, y) not in visible_field:
                    field.append((x, y))
                else:
                    edges = self.check_edges((x, y), visible_field)
                    # edges = []
                    for point, edge in edges:
                        tile = self.edges.get_tile(edge)
                        i, r = tile.render()
                        r.topleft = pixel_coords((x, y))
                        self.image.blit(i, r)

        for x, y in field:

            self.fog_rect.topleft = pixel_coords((x, y))
            self.image.blit(self.fog, self.fog_rect)
    
    def render(self):

        return self.image, self.rect

    @staticmethod
    def check_edges((x, y), visible):

        edges = []

        t = False
        b = False
        r = False
        l = False

        p = (x, y)

        if (x, y-1) not in visible:
            t = True
            edges.append((p, 't'))

        if (x, y+1) not in visible:
            b = True
            edges.append((p, 'b'))

        if (x-1, y) not in visible:
            l = True
            edges.append((p, 'l'))

        if (x+1, y) not in visible:
            r = True
            edges.append((p, 'r'))

        if t and l:
            edges.append((p, 'tl'))

        if t and r:
            edges.append((p, 'tr'))

        if b and l:
            edges.append((p, 'bl'))

        if b and r:
            edges.append((p, 'br'))

        return edges


def get_sight_radius((center)):

    # precomputing pseudo circle radius 7 tiles wide, 5 tiles high

    x, y = center

    x_range = (0, 1, 2, 3, 4, 5, 6, 6, 7, 7)
    y_range = (5, 5, 5, 4, 4, 4, 3, 2, 1, 0)

    circumference = []

    for i in range(10):
        a = (x_range[i]+x), (y_range[i]+y)
        b = (x_range[i]*-1)+x, (y_range[i]+y)
        c = (x_range[i]+x), (y_range[i]*-1)+y
        d = (x_range[i]*-1)+x, (y_range[i]*-1)+y
        for p in (a, b, c, d):
            if p not in circumference:
                circumference.append(p)

    return circumference
