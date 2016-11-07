from ..graphics import font_draw as fd
from ..constants import *
import pygame


class FPSClock(object):

    def __init__(self, screen):

        self.f = fd.FontDrawer()
        self.screen = screen

        self.box = pygame.Surface((scale(24), scale(10)))
        self.box.fill(BLACK)
        self.b_rect = self.box.get_rect()
        self.b_rect.bottomright = (SCREENWIDTH, SCREENHEIGHT)

    def show_time(self, fps):

        i, r = self.f.write(str(round(fps)), WHITE)
        r.bottomright = (scale(24), scale(10))

        self.box.fill(BLACK)
        self.box.blit(i, r)

        self.screen.blit(self.box, self.b_rect)
