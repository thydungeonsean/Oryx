import pygame
from ..constants import *


class Display(object):
    def __init__(self, w, h, topleft):

        self.w = w
        self.h = h

        self.topleft = topleft

        self.surface = pygame.Surface((w, h))
        self.surface.fill(BLACK)
        self.surface = self.surface.convert()
        # self.surface.set_colorkey(WHITE)
        self.rect = self.surface.get_rect()
        self.rect.topleft = self.topleft

        self.active = True
        self.clickable = False

    @property
    def x1(self):
        return self.topleft[0]

    @property
    def x2(self):
        return self.topleft[0] + self.w

    @property
    def y1(self):
        return self.topleft[1]

    @property
    def y2(self):
        return self.topleft[1] + self.h

    def clear(self):
        self.surface.fill(BLACK)

    def activate(self):

        self.active = True

    def deactivate(self):

        self.active = False

    def blit(self, image, rect):

        self.surface.blit(image, rect)

    def render(self):

        return self.surface, self.rect

    def mouse_over(self, (mx, my)):

        if self.x2 >= mx >= self.x1 and self.y2 >= my >= self.y1:
            return True
        else:
            return False

    def get_rel_pos(self, pos):

        vx, vy = self.topleft
        mx, my = pos

        rx = mx - vx
        ry = my - vy

        return rx, ry

    def click(self, button, pos):

        if button == 'l':
            self.left_click(pos)
        elif button == 'r':
            self.right_click(pos)

    def left_click(self, pos):

        pass

    def right_click(self, pos):

        pass
