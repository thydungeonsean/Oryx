import pygame
import tilesheet as ts
import tile_key_parser as tkparse
from constants import *
import outline as ol


class Image(object):
    
    def __init__(self, (tileset, key), color=BLACK, clear=WHITE):
        # for images with no transparency set clear to False
        
        self.tile_set = tileset
        ts_key = self.get_tile_key()
        self.key = key
        self.scaled = False
        self.clear = clear

        tile, tile_rect = ts.get_tile_image(self.tile_set, ts_key, self.key)

        self.image = pygame.Surface((tile_rect.w, tile_rect.h))
        self.image.fill(self.clear)
        self.rect = self.image.get_rect()

        self.image.blit(tile, tile_rect)

        self.image = self.image.convert()
        if clear:
            self.image.set_colorkey(self.clear)

        self.color = color
        self.set_color()

    def blank_image(self):
        pass

    def get_tile_key(self):

        return tkparse.get_tilesheet_key('%s_key' % self.tile_set)

    @property
    def topleft(self):

        return self.rect.topleft

    def set_scale(self):
        if not self.scaled:
            rw = scale(self.rect.w)
            rh = scale(self.rect.h)
            self.image = pygame.transform.scale(self.image, (rw, rh))
            self.rect = self.image.get_rect()
            self.scaled = True

    def set_color(self):

        pix_array = pygame.PixelArray(self.image)
        pix_array.replace(BLACK, self.color, 0.01)

    def change_color(self, new_color):

        if new_color != self.color:
            pix_array = pygame.PixelArray(self.image)
            pix_array.replace(self.color, new_color)
            self.color = new_color

    def render(self):
        return self.image, self.rect

    def position(self, (x, y)):

        self.rect.topleft = (x, y)


class ScaledImage(Image):

    def __init__(self, tile, color=BLACK, clear=WHITE):

        Image.__init__(self, tile, color, clear)

        self.set_scale()


class OutlinedImage(Image):

    def __init__(self, tile, color=BLACK):

        Image.__init__(self, tile, color)

        # put image on larger pallet so it can be outlined
        new_image = pygame.Surface((BASE_TILEWIDTH+2, BASE_TILEHEIGHT+2))
        new_image.fill(self.clear)
        new_image = new_image.convert()
        new_image.set_colorkey(self.clear)
        new_rect = new_image.get_rect()
        self.rect.topleft = (1, 1)
        new_image.blit(self.image, self.rect)
        self.image = new_image
        self.rect = new_rect

        self.outline()
        self.set_scale()

    def outline(self):

        ol.draw_outline(self.image, self.color)


class TerrainImage(ScaledImage):

    def __init__(self, tile, colors=(BLACK, DK_GREY)):

        ScaledImage.__init__(self, tile, clear=False)

        self.fore_color = colors[0]
        self.back_color = colors[1]

        self.set_colors()

    def set_colors(self):

        pix_array = pygame.PixelArray(self.image)
        if self.fore_color == LT_GREY:
            pix_array.replace(LT_GREY, self.back_color, 0.1)
            pix_array.replace(VR_DK_GREY, self.fore_color, 0.1)
        else:
            pix_array.replace(LT_GREY, self.back_color, 0.1)
            pix_array.replace(VR_DK_GREY, self.fore_color, 0.1)
