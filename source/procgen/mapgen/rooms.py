from random import *


def add_rect_room((sx, sy), w, h):

    floor = []
    wall = []
    corners = []
    ex = sx+w
    ey = sy+h

    for y in range(sy, ey):
        for x in range(sx, ex):

            if y == sy or y == ey-1:
                if x == sx or x == ex-1:
                    corners.append((x, y))
                else:
                    wall.append((x, y))
            elif x == sx or x == ex-1:
                wall.append((x, y))
            else:
                floor.append((x, y))

            if x-sx == w/2 and y-sy == h/2:
                center = (x, y)

    room = {'walls': wall,
            'corners': corners,
            'floor': floor,
            'center': center,
            'style': 'rect'
            }

    return room


def add_square_room(start, w):

    room = add_rect_room(start, w, w)
    room['style'] = 'square'

    return room


def add_rect_cross_room((sx, sy), w, h):

    floor = []
    wall = []
    hard_points = []
    ex = sx+w
    ey = sy+h

    for y in range(sy, ey):
        for x in range(sx, ex):

            if y == sy or y == ey-1:
                if x == sx+1 or x == ex-2:
                    hard_points.append((x, y))
                elif x == sx or x == ex-1:
                    pass
                else:
                    wall.append((x, y))

            elif x == sx or x == ex-1:
                if y == sy+1 or y == ey-2:
                    hard_points.append((x, y))
                elif y == sy or y == ey-1:
                    pass
                else:
                    wall.append((x, y))

            elif y == sy+1 or y == ey-2:
                if x == sx+1 or x == ex-2:
                    hard_points.append((x, y))
                else:
                    floor.append((x, y))

            else:
                floor.append((x, y))

            if x-sx == w/2 and y-sy == h/2:
                center = (x, y)

    room = {'walls': wall,
            'floor': floor,
            'corners': hard_points,
            'center': center,
            'style': 'rect cross'
            }

    return room


def add_rect_alcove_room((sx, sy), w, h, type=2):

    if type == 0:
        room = add_rect_alcove_room_vert((sx, sy), w, h)
    elif type == 1:
        room = add_rect_alcove_room_hor((sx, sy), w, h)
    elif type == 2:
        room = add_rect_alcove_room_both((sx, sy), w, h)

    return room


def add_rect_alcove_room_vert((sx, sy), w, h):

    if w % 2 == 0:
        w += 1
    if h % 2 == 0:
        h += 1

    floor = []
    wall = []
    corners = []
    ex = sx+w
    ey = sy+h

    for y in range(sy, ey):
        for x in range(sx, ex):

            if y == sy or y == ey-1:
                if x == sx or x == ex-1:
                    corners.append((x, y))
                else:
                    wall.append((x, y))
            elif x == sx or x == ex-1:
                wall.append((x, y))
            elif y == sy + 1 or y == ey - 2:
                if (x - sx) % 2 != 0:
                    wall.append((x, y))
                else:
                    floor.append((x, y))
            else:
                floor.append((x, y))

            if x - sx == w / 2 and y - sy == h / 2:
                    center = (x, y)

    room = {'walls': wall,
            'corners': corners,
            'floor': floor,
            'center': center,
            'style': 'alcove vertical'
            }

    return room


def add_rect_alcove_room_hor((sx, sy), w, h):

    if w % 2 == 0:
        w += 1
    if h % 2 == 0:
        h += 1

    floor = []
    wall = []
    corners = []
    ex = sx+w
    ey = sy+h

    for y in range(sy, ey):
        for x in range(sx, ex):

            if y == sy or y == ey-1:
                if x == sx or x == ex-1:
                    corners.append((x, y))
                else:
                    wall.append((x, y))
            elif x == sx or x == ex-1:
                wall.append((x, y))
            elif x == sx + 1 or x == ex - 2:
                if (y - sy) % 2 != 0:
                    wall.append((x, y))
                else:
                    floor.append((x, y))
            else:
                floor.append((x, y))

            if x - sx == w / 2 and y - sy == h / 2:
                    center = (x, y)

    room = {'walls': wall,
            'corners': corners,
            'floor': floor,
            'center': center,
            'style': 'alcove horizontal'
            }

    return room


def add_rect_alcove_room_both((sx, sy), w, h):

    if w % 2 == 0:
        w += 1
    if h % 2 == 0:
        h += 1

    floor = []
    wall = []
    corners = []
    ex = sx+w
    ey = sy+h

    for y in range(sy, ey):
        for x in range(sx, ex):

            if y == sy or y == ey-1:
                if x == sx or x == ex-1:
                    corners.append((x, y))
                else:
                    wall.append((x, y))
            elif x == sx or x == ex-1:
                wall.append((x, y))
            elif y == sy + 1 or y == ey - 2:
                if (x - sx) % 2 != 0:
                    wall.append((x, y))
                else:
                    floor.append((x, y))
            elif x == sx + 1 or x == ex - 2:
                if (y - sy) % 2 != 0:
                    wall.append((x, y))
                else:
                    floor.append((x, y))
            else:
                floor.append((x, y))

            if x - sx == w / 2 and y - sy == h / 2:
                    center = (x, y)

    room = {'walls': wall,
            'corners': corners,
            'floor': floor,
            'center': center,
            'style': 'alcove both'
            }

    return room


def add_rect_building(start, w, h):

    room = add_rect_room(start, w, h)

    sx, sy = start
    room['bottomright'] = (sx+w, sy+h)

    edge = add_edge(start, w, h)

    room['edge'] = edge

    return room


def add_rect_cross_building(start, w, h):

    room = add_rect_cross_room(start, w, h)

    sx, sy = start
    room['bottomright'] = (sx+w, sy+h)

    edge = add_edge(start, w, h)
    room['edge'] = edge

    return room


def add_square_building(start, w):

    room = add_rect_building(start, w, w)

    return room


def add_edge((sx, sy), w, h):

    edgex = (sx-1, sx+w+1)
    edgey = (sy-1, sy+h+1)

    edge = []

    for y in range(edgey[0], edgey[1]):
        for x in range(edgex[0], edgex[1]):
            if y == edgey[0] or y == edgey[1]-1:
                edge.append((x, y))
            elif (x == edgex[0] or x == edgex[1]-1) and (x, y) not in edge:
                edge.append((x, y))

    return edge


def get_distance(r1, r2):

    x1, y1 = r1
    x2, y2 = r2

    x_dist = abs(x1 - x2)
    y_dist = abs(y1 - y2)

    dist = x_dist + y_dist

    return dist


def add_field((sx, sy), w, h):

    field = []
    edge = []
    ex = sx+w
    ey = sy+h

    for y in range(sy-1, ey+1):
        for x in range(sx-1, ex+1):

            if y == sy-1 or y == ey:
                edge.append((x, y))
            elif x == sx-1 or x == ex:
                edge.append((x, y))
            else:
                field.append((x, y))

    return field, edge


def add_columns(room, style='collonade'):

    x1, y1 = room['corners'][0]
    x2, y2 = room['corners'][3]
    if room['style'] == 'rect cross':
        x1 -= 1
        x2, y2 = room['corners'][11]
        x2 += 1

    edge = 4

    w = x2 - x1 - edge + 1
    h = y2 - y1 - edge + 1

    w_offset = 0
    h_offset = 0
    if room['style'] == 'alcove both':
        w -= 2
        h -= 2
        w_offset = 1
        h_offset = 1
    elif room['style'] in ('rect cross', 'alcove horizontal'):
        w -= 2
        w_offset = 1
    elif room['style'] == 'alcove vertical':
        h -= 2
        h_offset = 1

    if w < 3 and h < 3:
        return False

    cx = x1 + edge/2 + w_offset
    cy = y1 + edge/2 + h_offset

    if style == 'collonade':
        columns = make_collonade((cx, cy), w, h)
    elif style == 'complete':
        columns = fill_with_columns((cx, cy), w, h)

    room['columns'] = columns

    return room


def make_collonade((cx, cy), w, h):

    columns = []

    for y in range(cy, cy + h):
        for x in range(cx, cx + w):
            if (y == cy or y == cy + h - 1) and (x-cx) % 2 == 0:
                columns.append((x, y))
            elif (x == cx or x == cx + w - 1) and (y-cy) % 2 == 0:
                columns.append((x, y))

    return columns


# TODO remove all random functions from rooms module in case it will fuck with seed() in generators


def fill_with_columns((cx, cy), w, h):

    columns = []

    q = 0
    p = 0

    # if w % 2 == 0:
    #     q = randint(0, 1)
    # if h % 2 == 0:
    #     p = randint(0, 1)

    for y in range(cy, cy + h):
        for x in range(cx, cx + w):
            if (y - cy) % 2 == p and (x - cx) % 2 == q:
                columns.append((x, y))

    return columns


