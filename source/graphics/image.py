import pygame
import tilesheet as ts
from ..constants import *


class Image(object):
    
    def __init__(self, (tileset, key), color=BLACK, clear=WHITE, start_color=BLACK, alpha=None):
        # for images with no transparency set clear to False

        self.scaled = False
        self.clear = clear
        self.alpha = alpha

        ts_key = self.get_tile_key(tileset)
        tile, tile_rect = ts.get_tile_image(tileset, ts_key, key)

        self.image = pygame.Surface((tile_rect.w, tile_rect.h))
        self.image.fill(self.clear)
        self.rect = self.image.get_rect()

        self.image.blit(tile, tile_rect)

        self.image = self.image.convert()
        if clear:
            self.image.set_colorkey(self.clear)

        self.color = color
        self.set_color(start_color)

        if self.alpha is not None:
            self.set_alpha()

    def set_alpha(self):

        self.image.set_alpha(self.alpha)
        self.image = self.image.convert_alpha()

    def blank_image(self):
        pass

    def get_tile_key(self, tileset):

        return ts.get_tilesheet_key('%s_key' % tileset)

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

    def set_color(self, start_color):

        pix_array = pygame.PixelArray(self.image)
        pix_array.replace(start_color, self.color, 0.01)

    def change_color(self, new_color):

        if new_color != self.color:
            pix_array = pygame.PixelArray(self.image)
            pix_array.replace(self.color, new_color)
            self.color = new_color

    def render(self):
        return self.image, self.rect

    def position(self, (x, y)):

        self.rect.topleft = (x, y)
        
    def blit(self, image, rect):
        
        self.image.blit(image, rect)


class ScaledImage(Image):

    def __init__(self, tile, color=BLACK, clear=WHITE, start_color=BLACK, alpha=None):

        Image.__init__(self, tile, color, clear, start_color, alpha=alpha)

        self.set_scale()


# for pre-made heroes/monsters
class OutlinedImage(Image):

    def __init__(self, tile, color=BLACK, start_color=BLACK, alpha=None):

        Image.__init__(self, tile, color, start_color=start_color, alpha=alpha)

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

        draw_outline(self.image, self.color)

    def position(self, (x, y)):

        self.rect.topleft = (x-SCALE, y-SCALE)


class CopiedActorImage(OutlinedImage):

    def __init__(self, copy):

        self.scaled = True
        self.clear = copy.clear
        self.alpha = copy.alpha

        self.image = pygame.Surface((copy.rect.w, copy.rect.h))
        self.image.fill(self.clear)
        self.rect = self.image.get_rect()

        self.image.blit(copy.image, copy.rect)

        self.image = self.image.convert()
        if self.clear:
            self.image.set_colorkey(self.clear)

        self.color = copy.color

        if self.alpha is not None:
            self.set_alpha()

        
# for custom avatars and procedurally generated heros and soldiers 
class AvatarImage(Image):
    
    def __init__(self, body, head=None, weapon=None, shield=None, cloak=None, wings=None, tail=None, color=BLACK,
                 alpha=None, frame='a'):

        self.layer_dict = {
                'head': head,
                'weapon': weapon,
                'shield': shield,
                'cloak': cloak,
                'wings': wings,
                'tail': tail
                }
        
        self.frame = frame
        frame_id = {'a': '1', 'b': '2'}
        
        bodyid = body + frame_id[self.frame]
        
        Image.__init__(self, ('avatar', bodyid), color)
        self.compile_image()
        
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
        
    def compile_image(self):
        
        for layer in self.layer_dict.keys():
            if self.layer_dict[layer] is not None:
                self.add_layer(self.layer_dict[layer])
                
    def add_layer(self, layer):
        
        image = Image(('avatar_equipment', layer), self.color)
        i, r = image.render()
        
        # draw differently for the bobbing animation frame
        if self.frame == 'b':
            r.topleft = (0, 1)
        
        self.blit(i, r)

    def outline(self):
        if self.color != BLACK:
            draw_outline(self.image, self.color)

    def position(self, (x, y)):
        self.rect.topleft = (x - SCALE, y - SCALE)


# animated images - from monsters tilesheet
class AnimatedSprite(object):

    def __init__(self, id, color, alpha=None):
        
        self.image_a = OutlinedImage(('monsters', id+'1'), color, alpha=alpha)
        self.image_b = OutlinedImage(('monsters', id+'2'), color, alpha=alpha)
        
        self.images = {
                    'a': self.image_a,
                    'b': self.image_b
                    }
        
    @property
    def topleft(self):

        return self.image_a.topleft
        
    def position(self, pos):
        
        self.image_a.position(pos)
        self.image_b.position(pos)
    
    def change_color(self, new_color):
        
        self.image_a.change_color(new_color)
        self.image_b.change_color(new_color)
    
    def render(self, frame='a'):
        
        image = self.images[frame]
        
        return image.render()
        
        
# animated images - from avatar generator
class AnimatedAvatar(AnimatedSprite):
    
    def __init__(self, body, head=None, weapon=None, shield=None, cloak=None, wings=None, tail=None, color=BLACK,
                 alpha=None):
        
        self.image_a = AvatarImage(body, head, weapon, shield, cloak, wings, tail, color, alpha, frame='a')
        self.image_b = AvatarImage(body, head, weapon, shield, cloak, wings, tail, color, alpha, frame='b')
        
        self.images = {
            'a': self.image_a,
            'b': self.image_b
            }


class CopiedAnimatedSprite(AnimatedSprite):

    def __init__(self, copy):

        copy_a = copy.image_a
        copy_b = copy.image_b

        self.image_a = CopiedActorImage(copy_a)
        self.image_b = CopiedActorImage(copy_b)

        self.images = {
            'a': self.image_a,
            'b': self.image_b
        }


# for terrain tiles - two color images
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


# effect functions
def check_diff_color(pix_array, surface, direction, (x, y), key_color):
    
    nx = x
    ny = y
    
    if direction == 'n':
        ny -= 1
    elif direction == 's':
        ny += 1
    elif direction == 'w':
        nx -= 1
    elif direction == 'e':
        nx += 1
        
    if pix_array[nx, ny] == surface.map_rgb(key_color):
        return True
    else:
        return False


def draw_outline(surface, color):

    ir = surface.get_rect()
    w = ir.w
    h = ir.h

    pix_array = pygame.PixelArray(surface)

    for y in range(h):
        for x in range(w):

            if pix_array[x, y] == surface.map_rgb(WHITE):

                l = []

                if x != 0:
                    l.append(check_diff_color(pix_array, surface, 'w', (x, y), color))

                if x != w - 1:
                    l.append(check_diff_color(pix_array, surface, 'e', (x, y), color))

                if y != 0:
                    l.append(check_diff_color(pix_array, surface, 'n', (x, y), color))

                if y != h-1:
                    l.append(check_diff_color(pix_array, surface, 's', (x, y), color))

                if True in l:
                    pix_array[x, y] = BLACK