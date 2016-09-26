from random import *


class CellularAutomaton(object):

    def __init__(self, (x, y), sd, open_noise, passes, opening, closing, border=0, special=None, split=False):

        seed(sd)

        self.xlim = x
        self.ylim = y

        self.open_noise = open_noise
        self.number_of_passes = passes
        self.opening_threshold = opening
        self.closing_threshold = closing
        self.special_close_level = special

        self.border = border

        # if true, will weight columns and rows to be closed
        self.split = split

        self.tiles = {}
        self.new_tiles = {}

    def generate_cellular_automaton(self):

        point_list = self.get_point_list()
        self.make_map_noise(point_list)

        for t in range(self.number_of_passes):

            for point in point_list:

                self.run_automaton(point)

            del self.tiles
            self.tiles = self.new_tiles
            self.new_tiles = {}

    def block_column(self, x):

        for y in range(self.ylim):
            self.tiles[(x, y)] = False

    def block_row(self, y):

        for x in range(self.xlim):
            self.tiles[(x, y)] = False

    def make_map_noise(self, point_list):

        shuffle(point_list)

        for point in point_list:

            if randint(0, 99) < self.open_noise:
                self.tiles[point] = True
            else:
                self.tiles[point] = False

        if self.split:
            if self.split[0]:
                self.set_vert_split()
            if self.split[1]:
                self.set_hor_split()
            if self.split[2]:
                self.set_center_split()

    def set_vert_split(self):

        self.block_column(self.xlim/2)

    def set_hor_split(self):

        self.block_row(self.ylim/2)

    def set_center_split(self):

        self.block_column(self.xlim/4)
        self.block_column(self.xlim/4+self.xlim/2)
        self.block_row(self.ylim/4)
        self.block_row(self.ylim/4+self.ylim/2)

    def get_point_list(self):

        l = []

        for y in range(self.ylim):
            for x in range(self.xlim):
                l.append((x, y))

        return l

    def clear(self):

        point_list = self.get_point_list()
        for point in point_list:
            self.tiles[point] = False

    def run_automaton(self, (x, y)):

        if self.is_edge((x, y)):
            self.new_tiles[(x, y)] = False
            return

        x_r = (x, x-1, x+1)
        y_r = (y, y-1, y+1)

        tile_open = self.tiles[(x, y)]

        num_open = 0

        for py in y_r:
            for px in x_r:

                if (px, py) == (x, y):
                    continue
                elif self.tiles[(px, py)]:
                    num_open += 1

        if not tile_open and num_open >= self.opening_threshold:
            self.new_tiles[(x, y)] = True
        elif tile_open and num_open == self.special_close_level:
            self.new_tiles[(x, y)] = False
        elif tile_open and num_open <= self.closing_threshold:
            self.new_tiles[(x, y)] = False
        else:
            self.new_tiles[(x, y)] = self.tiles[(x, y)]

    def is_edge(self, (x, y)):

        if x <= self.border or x >= self.xlim-1-self.border:
            return True
        elif y <= self.border or y >= self.ylim-1-self.border:
            return True
        else:
            return False
