import pygame
import sys, os
from pygame.locals import *
from constants import *

from tileset import TileSet
from map import Map
from dungeon_map import DungeonMap
from rural_map import RuralMap
from cave_map import CaveMap
from world_map import WorldMap

import common_tiles as ct


class View(object):

    def __init__(self, map):

        self.xlim = 20
        self.ylim = 12

        self.x = 0
        self.y = 0

    def move_vert(self, move):
        self.y += move

    def move_hor(self, move):
        self.x += move

    def set(self):
        return self.x, self.y


class Control(object):

    def __init__(self, view):

        self.view = view

        self.state = 'still'

    def run(self):

        if self.state == 'up':
            self.view.move_vert(15)
        elif self.state == 'down':
            self.view.move_vert(-15)
        elif self.state == 'right':
            self.view.move_hor(-15)
        elif self.state == 'left':
            self.view.move_hor(15)


def set_screen():

    # absolute screen size
    #screen = pygame.display.set_mode((800, 600), HWSURFACE | DOUBLEBUF)
    # scalled screen size
    screen = pygame.display.set_mode((1000, 750), HWSURFACE | DOUBLEBUF)
    pygame.display.set_caption('Oryx Demo')
    
    return screen
    
    
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


def draw_demo(map, view, frame):

    global screen

    screen.fill(BLACK)

    f = 'a'
    if frame > 30:
        f = 'b'

    i, r = map.render(frame=f)
    r.topleft = (view.set())
    screen.blit(i, r)


def demo():

    global screen

    os.environ["SDL_VIDEO_CENTERED"] = '1'
    pygame.init()

    clock = pygame.time.Clock()
            
    screen = set_screen()
    ct.common_tiles.initiate_tiles()

    # m = RuralMap(loading_screen=(True, screen))
    # m = CaveMap(loading_screen = (True, screen))
    # m = DungeonMap(loading_screen=(True, screen))
    m = WorldMap(w=100, h=60, loading_screen=(True, screen))
    print m.seed
    v = View(m)
    c = Control(v)
    # pygame.image.save(map, 'map.png')

    frame = 0

    while True:
        frame += 1
        if frame > 60:
            frame = 1

        draw_demo(m, v, frame)
        handle_input(c)
        pygame.display.update()
        
        clock.tick(FPS)
        # print clock.get_fps()


if __name__ == '__main__':
   
    demo()
