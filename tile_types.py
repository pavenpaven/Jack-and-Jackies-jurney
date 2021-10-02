import pygame

tile=60

def no_stepfunc():
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

Pine_type = Tile_type("Art/Pine_1.png", True, "p")
jack_type = Tile_type("Art/jack.png", False, "j")
grass_tile_type = Tile_type("Art/tile_1.png", False, "g")
