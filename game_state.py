import pygame
from pygame.locals import *
from dungeon_map import DungeonMap
from cave_map import CaveMap
from rural_map import RuralMap
from world_map import WorldMap
from player import Player
import controller
import main_display as md
import fov_map as fov


class GameState(object):

    def __init__(self, screen, clock):

        self.screen = screen
        self.clock = clock

        self.frame = 1

        self.player = Player()

        self.mode = 'menu'

        self.controller = controller.Controller(self)
        self.FOV = fov.FOV_Map(None, self.player, True)

        self.current_map = None
        self.preloaded_maps = {}

        self.load_new_map('cave')

        self.display = md.MainDisplay(self, md.View(self.player))

    def load_new_map(self, type):

        load = (True, self.screen)

        if type == 'cave':
            new = CaveMap(loading_screen=load)
        elif type == 'dungeon':
            new = DungeonMap(loading_screen=load)
        elif type == 'village':
            new = RuralMap(loading_screen=load)
        elif type == 'world':
            new = WorldMap(loading_screen=load)

        del self.current_map
        self.current_map = new

        entrance = self.current_map.feature_map.features['ent1'].coord
        self.player.add_to_map(self.current_map, entrance)

        self.FOV.load_map(self.current_map)

    def update(self):

        self.tick_frame()

        self.FOV.run()

        self.display.update()

    def render_all(self):
        i, r = self.display.render()
        self.screen.blit(i, r)

    def handle_input(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()

                elif event.key == K_UP:
                    self.controller.up()
                elif event.key == K_DOWN:
                    self.controller.down()
                elif event.key == K_RIGHT:
                    self.controller.right()
                elif event.key == K_LEFT:
                    self.controller.left()

                # mouse controls
                # elif event.type == MOUSEBUTTONDOWN:
                #     mouse_button = mouse.get_button(pygame.mouse.get_pressed())
                #     mouse_pos = pygame.mouse.get_pos()
                #     mouse.mouse_click(self, mouse_button, mouse_pos)
    def tick_frame(self):
        self.frame += 1
        if self.frame > 60:
            self.frame = 1
