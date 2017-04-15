from display import Display
from ..constants import *


class MainDisplay(Display):

    def __init__(self, gamestate, view):

        Display.__init__(self, DISPLAYW, DISPLAYH, (0, 0))

        self.GS = gamestate
        self.view = view

    @property
    def map(self):
        return self.GS.current_map

    def get_frame(self):

        if self.GS.frame <= BOBRATE:
            return 'a'
        else:
            return 'b'

    def update(self):

        frame = self.get_frame()

        self.update_map(frame)

        self.update_features(frame)

        i, r = self.GS.player.render(frame)
        r.topleft = self.view.set_object_coord(self.GS.player)
        self.blit(i, r)

        self.update_monsters(frame)

        self.update_fov()

        self.deactivate()

    def update_map(self, frame):

        if self.view.x < 0 or self.view.y < 0 or self.view.x + 17 > self.map.xlim or self.view.y+11 > self.map.ylim:
            self.clear()

        self.map.map_rect.topleft = self.view.set_display_coord()
        i, r = self.map.render(frame)
        self.blit(i, r)

    def update_fov(self):

        if self.GS.FOV.on:
            i, r = self.GS.FOV.render()
            self.blit(i, r)

    def update_monsters(self, frame):

        for monster in self.map.monsters.monsters:

            if self.view.in_view(monster):
                i, r = monster.render(frame)
                r.topleft = self.view.set_object_coord(monster)
                self.blit(i, r)

    def update_features(self, frame):

        for feature in self.map.feature_map.draw_features:
            if feature.needs_draw:
                i, r = feature.render(frame)
                r.topleft = self.view.set_object_coord(feature)
                self.blit(i, r)


class View(object):

    def __init__(self, centered):

        self.centered = centered

    @property
    def x(self):
        return self.centered.x - PLAYERRELX

    @property
    def y(self):
        return self.centered.y - PLAYERRELY

    def set_display_coord(self):

        return self.x*TILEWIDTH*-1, self.y*TILEHEIGHT*-1

    def set_object_coord(self, obj):

        ox, oy = obj.coord
        x = ox - self.x
        y = oy - self.y

        return x*TILEWIDTH, y*TILEHEIGHT

    def in_view(self, obj):
        ox, oy = obj.coord
        if ox >= self.x and ox < self.x + BASE_DISPLAYW and oy >= self.y and oy < self.y + BASE_DISPLAYH:
            return True
        else:
            return False
