import pygame
from ..constants import *
import os


class FontDrawer(object):

    import_path = ''.join((os.path.dirname(__file__), '\\..\\..\\assets\\'))

    def __init__(self):
        self.font = pygame.font.Font(''.join((FontDrawer.import_path, 'font/oryxtype.ttf')), 16)

    def write(self, text, color):
        fii = self.font.render(text, False, color)
        r = fii.get_rect()
        fi = pygame.transform.scale(fii, (scale(r.w), scale(r.h)))
        r = fi.get_rect()

        return fi, r
