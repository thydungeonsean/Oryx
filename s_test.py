import monster_generator as mg
import pygame


# screen = pygame.display.set_mode((100, 100))
# pygame.display.set_caption('Oryx Demo')
#
# pygame.init()
#
#
# m = mg.MonsterGenerator()
#
# monster = m.create_monster('kobolds', 'horse')
#
# i, r = monster.image.render(frame='b')
#
# # pygame.image.save(i, 'workimage.png')
#
# screen.blit(i, r)
# pygame.display.update()
#
# event = pygame.event.wait()
# pygame.quit()
#
l = [1, 2]
try:
    l.remove(3)
except ValueError:
    print 'index error'
    pass
l.remove(3)