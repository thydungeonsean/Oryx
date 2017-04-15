SCALE = 2


def scale(arg):

    if isinstance(arg, tuple):
        scaled_tuple = []
        for i in arg:
            scaled_tuple.append(i*SCALE)
        new = tuple(scaled_tuple)
        return new
    elif isinstance(arg, int):
        return int(arg*SCALE)


def descale(arg):
    if isinstance(arg, tuple):
        scaled_tuple = []
        for i in arg:
            scaled_tuple.append(i/SCALE)
        new = tuple(scaled_tuple)
        return new
    elif isinstance(arg, int):
        return int(arg/SCALE)


SCREENWIDTH = scale(400)
SCREENHEIGHT = scale(300)
FPS = 60

BOBRATE = FPS / 2

BASE_TILEWIDTH = 16
BASE_TILEHEIGHT = 24
TILEWIDTH = scale(BASE_TILEWIDTH)
TILEHEIGHT = scale(BASE_TILEHEIGHT)

# displays
# main display, 17 x 11 tiles - player at (8, 5) relative to topleft corner
BASE_DISPLAYW = 17
BASE_DISPLAYH = 11
DISPLAYW = TILEWIDTH * BASE_DISPLAYW
DISPLAYH = TILEHEIGHT * BASE_DISPLAYH
PLAYERRELX = 8
PLAYERRELY = 5


# turn grid coords into pixel coords
def pixel_coords((x, y)):
    
    return x*TILEWIDTH, y*TILEHEIGHT

    
# colors
WHITE = (255, 255, 255)
OWHITE = (255, 254, 255)

BLACK = (0, 0, 0)
NR_BLACK = (10, 10, 10)
VR_DK_GREY = (33, 33, 33)
DK_GREY = (66, 66, 66)
GREY = (100, 100, 100)
LT_GREY = (200, 200, 200)

RED = (255, 0, 0)
DP_RED = (180, 10, 10)
LT_RED = (230, 40, 30)

VIOLET = (220, 70, 210)

BLUE = (0, 0, 255)
GR_BLUE = (45, 100, 130)
DK_BLUE = (0, 0, 180)
GRY_BLUE = (110, 145, 190)
DK_GRY_BLUE = (66, 100, 145)

BROWN = (170, 70, 10)
DK_BROWN = (100, 40, 5)
VR_DK_BROWN = (80, 30, 0)
DKST_BROWN = (70, 25, 0)
BEIGE = (240, 230, 175)

GREEN = (50, 190, 0)
DK_GREEN = (15, 55, 0)
DP_GREEN = (0, 125, 0)
LT_BL_GREEN = (70, 235, 110)
Bl_GREEN = (0, 130, 65)
DK_BL_GREEN = (0, 90, 45)
LT_GR_GREEN = (95, 140, 110)
DK_GR_GREEN = (45, 80, 40)
GR_GREEN = (85, 150, 75)

YELLOW = (240, 210, 5)

# color key dictionary
color_key = {
    'red': RED,
    'dp_red': DP_RED,
    'lt_red': LT_RED,
    'violet': VIOLET,
    'blue': BLUE,
    'dk_blue': DK_BLUE,
    'gr_blue': GR_BLUE,
    'gry_blue': GRY_BLUE,
    'dk_gry_blue': DK_GRY_BLUE,
    'white': WHITE,
    'owhite': OWHITE,
    'black': BLACK,
    'nr_black': NR_BLACK,
    'vr_dk_grey': VR_DK_GREY,
    'dk_grey': DK_GREY,
    'lt_grey': LT_GREY,
    'grey': GREY,
    'brown': BROWN,
    'dk_brown': DK_BROWN,
    'vr_dk_brown': VR_DK_BROWN,
    'dkst_brown': DKST_BROWN,
    'beige': BEIGE,
    'yellow': YELLOW,
    'green': GREEN,
    'dk_green': DK_GREEN,
    'dp_green': DP_GREEN,
    'bl_green': Bl_GREEN,
    'lt_bl_green': LT_BL_GREEN,
    'dk_bl_green': DK_BL_GREEN,
    'lt_gr_green': LT_GR_GREEN,
    'gr_green': GR_GREEN,
    'dk_gr_green': DK_GR_GREEN
    # '': ,
}
