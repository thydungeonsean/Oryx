import pygame
import os, sys
from pygame.locals import *
from constants import *
from dungeon_map import DungeonMap
from cave_map import CaveMap
from rural_map import RuralMap
from world_map import WorldMap
import common_tiles as ct
import player
import fov_map
import debug_tools as dt


class View(object):
    def __init__(self, map, player):
        self.xlim = 20
        self.ylim = 12

        self.x = 0
        self.y = 0

    def move(self, direction):
        if direction == 'up':
            self.y += TILEHEIGHT
        elif direction == 'down':
            self.y -= TILEHEIGHT
        elif direction == 'right':
            self.x -= TILEWIDTH
        elif direction == 'left':
            self.x += TILEWIDTH

    def set(self):
        return self.x, self.y


class Control(object):
    def __init__(self, player, view):

        self.player = player

        self.view = view

        self.state = 'still'

    def run(self):

        if self.state == 'up':
            self.player.move('up')
            self.view.move('up')
        elif self.state == 'down':
            self.player.move('down')
            self.view.move('down')
        elif self.state == 'right':
            self.player.move('right')
            self.view.move('right')
        elif self.state == 'left':
            self.player.move('left')
            self.view.move('left')


def set_screen():
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), HWSURFACE | DOUBLEBUF)
    pygame.display.set_caption('Oryx Demo')
    display = pygame.Surface((DISPLAYW, DISPLAYH))
    dr = display.get_rect()

    return screen, display, dr


def handle_input(control):
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
                # other key presses here
            if event.key == K_UP:
                control.state = 'up'
            elif event.key == K_DOWN:
                control.state = 'down'
            elif event.key == K_RIGHT:
                control.state = 'right'
            elif event.key == K_LEFT:
                control.state = 'left'

        elif control.state != 'still' and event.type == KEYUP:
            control.state = 'still'

        # mouse controls
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

    control.run()

    control.state = 'still'


def draw_demo(map, map_rect, view, player, fov, frame):
    global screen, display, dr, field

    display.fill(BLACK)
    map_rect.topleft = (view.set())
    display.blit(map, map_rect)
    
    if frame >= 30:
        animation = 'b'
    else:
        animation = 'a'
    
    i, r = player.render(frame=animation)
    display.blit(i, r)

    if field:
        f, fr = fov.render()
        display.blit(f, fr)

    screen.blit(display, dr)


def demo():
    global screen, display, dr, fog_display

    os.environ["SDL_VIDEO_CENTERED"] = '1'
    pygame.init()

    clock = pygame.time.Clock()

    screen, display, dr = set_screen()
    f_clock = dt.FPSClock(screen)

    ct.common_tiles.initiate_tiles()

    m = DungeonMap(w=50, h=30, loading_screen=(True, screen))
    print m.seed
    
    p = player.PlayerOld()
    v = View(m, p)
    c = Control(p, v)
    fov = fov_map.FOV_Map(m, p)

    global field
    field = True
    
    map, map_rect = m.map_image, m.map_rect
    
    frame = 0

    while True:

        if p.moved:
            if field:
                fov.run()
            p.moved = False

        frame += 1
        if frame > 60:
            frame = 1
            
        draw_demo(map, map_rect, v, p, fov, frame)
        handle_input(c)
        pygame.display.update()

        clock.tick(FPS)
        f_clock.show_time(clock.get_fps())


if __name__ == '__main__':
    demo()
