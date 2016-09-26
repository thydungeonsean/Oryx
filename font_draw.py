import pygame
from constants import *


class FontDrawer(object):
    def __init__(self):
        self.font = pygame.font.Font('assets/font/oryxtype.ttf', 16)

    def write(self, text, color):
        fii = self.font.render(text, False, color)
        r = fii.get_rect()
        fi = pygame.transform.scale(fii, (scale(r.w), scale(r.h)))
        r = fi.get_rect()

        return fi, r
