import pygame
import sys
import os
from pygame.locals import *
from constants import *
import avatar_gen as ag
import font_draw as fd


class Control(object):
    def __init__(self, gen, avatar):

        self.gen = gen

        self.avatar = avatar

        self.state = 'still'

    def run(self):

        if self.state == 'up':
            self.gen.control(self.state)
            return False
        elif self.state == 'down':
            self.gen.control(self.state)
            return False
        elif self.state == 'right':
            self.gen.control(self.state)
            return True
        elif self.state == 'left':
            self.gen.control(self.state)
            return True
        elif self.state == 'random':
            self.gen.control(self.state)
            return True
            
        return False


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
            elif event.key == K_r:
                control.state = 'random'

        elif control.state != 'still' and event.type == KEYUP:
            control.state = 'still'

        # mouse controls
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            
def set_screen():
    screen = pygame.display.set_mode((TILEWIDTH+100, TILEHEIGHT+50), HWSURFACE | DOUBLEBUF)
    pygame.display.set_caption('Oryx Demo')

    return screen
    
    
def draw_demo(avatar, frame, f, gen):
    global screen
    
    if frame >= 30:
        animation = 'b'
    else:
        animation = 'a'
    
    image, rect = avatar.render(frame=animation)
    
    screen.fill(VR_DK_GREY)
    screen.blit(image, rect)

    row = gen.rows[gen.cursor_y]

    row_name = gen.rows[gen.cursor_y]
    layer_key = gen.row_to_layer_dict[row_name]
    column = gen.layer[layer_key]

    write(f, row, TILEHEIGHT)
    write(f, column, TILEHEIGHT+12)


def write(f, content, y):

    global screen

    i, r = f.write(content, OWHITE)
    r.topleft = (0, y)

    screen.blit(i, r)

    
def demo():
    global screen

    sys.setrecursionlimit(26000)

    os.environ["SDL_VIDEO_CENTERED"] = '1'
    pygame.init()

    clock = pygame.time.Clock()

    screen = set_screen()
    
    gen = ag.AvatarGen()
    a = gen.get_avatar_image(RED)
    c = Control(gen, a)
    f = fd.FontDrawer()
    
    frame = 0
    
    while True:
    
        frame += 1
        if frame > 60:
            frame = 0
    
        draw_demo(a, frame, f, gen)
        handle_input(c)
        change = c.run()
        c.state = 'still'
        
        if change:
            a = gen.get_avatar_image(RED)
        
        pygame.display.update()

        clock.tick(FPS)
        # print clock.get_fps()


if __name__ == '__main__':
    demo()
