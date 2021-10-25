import pygame

tile=30

def no_stepfunc():
    pass

def rotate_tile():
    pass

class Tile_type:
    types_length=0
    types=[]
    def __init__(self, texture_filename, collision, letter, stepfunc=no_stepfunc):
        self.index = __class__.types_length
        __class__.types_length += 1
        
        untransformed_texture = pygame.image.load(texture_filename)
        self.texture = pygame.transform.scale(untransformed_texture, (tile, tile))
        
        self.collision = collision
        self.letter = letter
        self.stepfunc = stepfunc
        __class__.types.append(self)

    def find(letter):
        for i in __class__.types:
            if i.letter == letter:
                return i
        k # letter not found
    def find_letter(index):
        return __class__.types[index].letter

Pine_type = Tile_type("Art/pine_2.png", True, "p")
jack_type = Tile_type("Art/jack.png", False, "j")
grass_tile_type = Tile_type("Art/grass_2.png", False, "g")
sand_tile_type = Tile_type("Art/tile_3.png", False, "S")
path = Tile_type("Art/path_1.png", False, "-")
Tile_type("Art/path_2.png", False, "k")
Tile_type("Art/path_up", False, "o")
Tile_type("Art/path_3", False, "e")
Tile_type("Art/path_4", False, "i")
