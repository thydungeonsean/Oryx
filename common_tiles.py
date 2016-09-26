import tileset as ts


class Common_Tiles(object):

    outlined = ('dungeon_features',)

    def __init__(self):

        self.init = False

        self.common_tiles = {
                            'gore': None,
                            'dungeon_clutter': None,
                            'village_clutter': None,
                            'dungeon_features': None
                            }

        self.tile_keys = {}

        for key in self.common_tiles.keys():
            self.tile_keys[key] = ts.get_tile_keys(key)

    def initiate_tiles(self):

        if self.init:
            return

        for name in self.common_tiles.keys():

            if name in Common_Tiles.outlined:
                self.common_tiles[name] = ts.OutlineTileSet(name)
            else:
                self.common_tiles[name] = ts.TileSet(name)

        self.init = True

# init = False
# gore = None
# dungeon_clutter = None
# village_clutter = None
#
# common_tiles = {
#                 'gore': gore,
#                 'dungeon_clutter': dungeon_clutter,
#                 'village_clutter': village_clutter
#                 }
#
#
# tile_keys = {}
# for key in common_tiles.keys():
#     tile_keys[key] = ts.get_tile_keys(key)
#
#
# def initiate_tiles():
#     print 'stuff'
#     global init, gore, dungeon_clutter, village_clutter
#
#     gore = ts.TileSet('gore')
#     print gore
#     dungeon_clutter = ts.TileSet('dungeon_clutter')
#     village_clutter = ts.TileSet('village_clutter')
#
#     init = True

common_tiles = Common_Tiles()
