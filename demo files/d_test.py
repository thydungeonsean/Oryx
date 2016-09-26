import dijkstra_map as djk
import dungeon_map as dm
import rural_map
import cave_map
from random import choice, sample

import pygame
pygame.init()
screen = pygame.display.set_mode((10, 10))


m = dm.DungeonMap()
# m = rural_map.RuralMap()
# m = cave_map.CaveMap()
print 'dungeon generated'
p = [choice(m.tiles['floor'])]
# p = sample(m.tiles['floor'], 3)

dijk = djk.DijkstraMap(m, p)
print 'd map made'
dijk.print_map()
