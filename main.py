import sys
import os
import pygame
from pygame.locals import *
from constants import *
import common_tiles as ct
import debug_tools as dt
import game_state


def main():

    os.environ["SDL_VIDEO_CENTERED"] = '1'  # center screen

    pygame.init()

    clock = pygame.time.Clock()

    screen = set_screen()
    ct.common_tiles.initiate_tiles()

    GS = game_state.GameState(screen, clock)

    clock_counter = dt.FPSClock(screen)

    while True:

        # update game state
        GS.update()

        # render game state
        GS.render_all()

        pygame.display.update()

        GS.clock.tick(FPS)
        clock_counter.show_time(GS.clock.get_fps())

        # get input
        GS.handle_input()


def set_screen():

    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), HWSURFACE | DOUBLEBUF)
    # screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), FULLSCREEN | HWSURFACE)

    pygame.display.set_caption('Chronicles of Oryx')

    return screen


if __name__ == '__main__':

    main()
