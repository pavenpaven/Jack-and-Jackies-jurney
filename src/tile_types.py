import pygame

tile=30

def no_stepfunc():
    pass

def rotate_tile():
    pass

class Tile_type:
    types_length=0
    types=[]
    def __init__(self, texture_filename, collision, letter, key = None, rotate=0, flipx=False, flipy=False, stepfunc=no_stepfunc):
        self.index = __class__.types_length
        __class__.types_length += 1
        
        untransformed_texture = pygame.image.load(texture_filename)
        self.texture = pygame.transform.scale(untransformed_texture, (tile, tile))
        self.texture = pygame.transform.rotate(self.texture, 90 * rotate)
    
        self.key = key
        self.collision = collision
        self.letter = letter 
        self.stepfunc = stepfunc
        __class__.types.append(self)
        
        if flipx or flipy:
            self.letter = "1" + letter
            self.texture = pygame.transform.flip(self.texture ,flipx , flipy)
            Tile_type(texture_filename, collision, letter)

        if rotate != 0:
            self.letter = str(rotate)+ letter
            Tile_type(texture_filename, collision, letter, rotate = rotate -1)

    def find(letter):
        for i in __class__.types:
            if i.letter == letter:
                return i
        print(letter)
        k # letter not found
    def find_letter(index):
        return __class__.types[index].letter

Tile_type("Art/unknown.png", True, "u", key=pygame.K_u)
Pine_type = Tile_type("Art/pine_2.png", True, "p", key = pygame.K_p)
jack_type = Tile_type("Art/jack.png", True, "j", rotate=3)
grass_tile_type = Tile_type("Art/grass_2.png", False, "g", key = pygame.K_g)
sand_tile_type = Tile_type("Art/tile_3.png", False, "S")
path = Tile_type("Art/path_1.png", False, "-", key = pygame.K_h, rotate=1)
Tile_type("Art/path_2.png", False, "k", rotate=3)
Tile_type("Art/path_3.png", False, "e", rotate=3)
Tile_type("Art/path_4", False, "i")
Tile_type("Art/fading.png", False, "f", rotate = 3)
Tile_type("Art/window.png", True, "w", flipx = True)
Tile_type("Art/door.png", False, "d")
Tile_type("Art/roof.png", True, "r", key=pygame.K_t)
Tile_type("Art/purple_door.png", False, "D")
Tile_type("Art/purple_window.png", True, "W", flipx = True)
Tile_type("Art/yellow_door.png", False, "y", key=pygame.K_y)
Tile_type("Art/yellow_window.png", True, "Y", flipx = True)
Tile_type("Art/blue_window.png", True, "b")
Tile_type("Art/blue_window1.png", True, "B", flipx = True)
Tile_type("Art/blue_window2.png", True, "q")
Tile_type("Art/blue_door.png", False, "Q")
Tile_type("Art/good_floor6.png", False, "F", key=pygame.K_f)
Tile_type("Art/good_floor6_2.png", False, "U")
Tile_type("Art/matta2.png", False, "t", flipx = True)
Tile_type("Art/froll.png", True, "T")
Tile_type("Art/wall.png", True,  "v")
Tile_type("Art/wall_top.png", True, "V")
Tile_type("Art/stone_mark.png", False, "s", key=pygame.K_q)
Tile_type("Art/stone_face.png", True, "o", key=pygame.K_c)
Tile_type("Art/stone_wall.png", True, "O")
Tile_type("Art/stone_mark_grass_corner.png", False, "z", rotate=3)
Tile_type("Art/stone_mark_grass_edge.png", False, "Z", rotate=3)
Tile_type("Art/stone_mark_grass_long_edge.png", False, "x", rotate=3)
Tile_type("Art/stone.png", True, "N", key=pygame.K_v)
Tile_type("Art/cave_entraince.png", False, "X", rotate=3)
Tile_type("Art/kant_cave_entrance.png", False, "^", rotate=3)
Tile_type("Art/upper_middle_shop.png", True, "*", key=pygame.K_b)
Tile_type("Art/down_middel_shop.png", True, "~")
Tile_type("Art/upper_corner_shop.png", True, "!", flipx = True)
Tile_type("Art/down_corner_shop.png", True, "@", flipx = True)
Tile_type("Art/kon.png", True, "£")
Tile_type("Art/sand_tile.png", False, "[", key=pygame.K_e)
Tile_type("Art/water.png", True, "]")
Tile_type("Art/water_edge.png", False, "{", rotate=3)
Tile_type("Art/water_corner.png", False, "}", rotate=3)
Tile_type("Art/water_long_edge.png", False, "R", rotate=3)
Tile_type("Art/table.png", True, "J")
Tile_type("Art/plate.png", True, "I")
Tile_type("Art/Teracota.png", False, "E")
