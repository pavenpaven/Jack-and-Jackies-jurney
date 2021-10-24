#!/usr/bin/env python3
import sys
import pygame
import tile_types
import time

tile=30
map_size = (30, 12)

def parse_args(args, length):
    if length == 1:
        print("few args")
        exit()
    if args[1][0] == "-":
        parse_mode(args)
    else:
        if length < 3:
            print("too few args")
        open_level_edit(args[1], args[2])

def get_segname_room(filename, segname):
    with open(filename, "r") as fil:
        text = fil.read()
        
    for i in text.split("?"):
        segments = i.split("#")
        if segments[0] == segname:
            break
    else:
        print("no segment name named: ", segname)
        pygame.quit()
        exit()
    return segments

    

def open_level_edit(filename, segname):
    def check_key():
        quit = False
        for event in  pygame.event.get():
            if event.type == pygame.KEYDOWN:
                vec = [0, 0]
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    last_pressed=framecount
                    vec[0]+=-1
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    last_pressed=framecount
                    vec[0]+=1
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    last_pressed=framecount
                    vec[1] +=-1
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    vec[1] += 1
                if event.key == pygame.K_x:
                    curser.change_tile()
                curser.pos = (vec[0]+curser.pos[0], vec[1]+curser.pos[1])
                last_pressed=framecount
            if event.type == pygame.QUIT:
                quit = True
        return quit

    def graphics():
        window.fill((0,0,0))
        scene.render()
        pygame.display.update()
        
    class Map:
        def __init__(self, size, pos): #size is a tuple
            self.size = size
            self.pos = pos
            #texture= pygame.image.load(backgrund_filename)
            #self.backgrund_tile = pygame.transform.scale(texture,size)
            self.surface = pygame.Surface((size[0]*tile, size[1]*tile))
            self.tiles = []
    
        def load_room(self, filename, segname):
            segments = get_segname_room(filename, segname)
            row = segments[1].split("\n")
            self.tiles=[]
            for i in row:
                row_tiles = []
                for f in i:
                    row_tiles.append(tile_types.Tile_type.find(f).index)
                self.tiles.append(row_tiles)
    
        def render(self):
            self.surface.fill((0,0,0))
            #self.surface.blit(self.backgrund_tile, (0,0))
            y = 0
            for i in self.tiles:
                x = 0
                for f in i:
                    self.surface.blit(tile_types.Tile_type.types[f].texture, (x,y))
                    x += tile
                y += tile
            self.surface.blit(curser.texture, (curser.pos[0]*tile, curser.pos[1]*tile))
            window.blit(self.surface, self.pos)
        
        def save(self, filename, segname):
            with open(filename, "r") as fil:
                tex = fil.read()
            n = 0
            seg = tex.split("?") 
            for i in seg:
                if i.split("#")[0] == segname:
                    break
                n+=1
            seg.pop(n)
            room_info = segname + "#" + self.convert_to_letters() + "#"
            seg.insert(n, room_info)
            result = ""
            b=0
            for i in seg:
                if not b == len(seg) -1:
                    result += i + "?"
                b+=1

            with open(filename, "w") as fil:
                fil.write(result)
        
        def convert_to_letters(self):
            out = ""
            n=0
            for i in self.tiles:
                for f in i:
                    out += tile_types.Tile_type.find_letter(f)
                if not n == len(self.tiles) -1:
                    out += "\n"
                n+=1
            return out

    class Curser:
        def __init__(self, pos, texture):
            tex = pygame.image.load(texture)
            self.texture = pygame.transform.scale(tex ,(tile, tile))
            self.pos = pos
        def change_tile(self):
            if scene.tiles[self.pos[1]][self.pos[0]] != len(tile_types.Tile_type.types) - 1:
                scene.tiles[self.pos[1]][self.pos[0]]+=1
            else:
                scene.tiles[self.pos[1]][self.pos[0]] = 0

    curser = Curser((1,1), "Art/jack.png")
    scene = Map((30,12), (0, tile*2))      
    scene.load_room(filename, segname)
    window = pygame.display.set_mode((900,600))
    running = True
    clock = pygame.time.Clock()
    framecount = 0
    last_pressed = 0
    while running:
        clock.tick(30)
        framecount+=1
        if framecount % 60 == 0:
            print(clock.get_fps())
        graphics()
        quit=check_key()
        if quit == True:
            scene.save(filename, segname)
            pygame.quit()
            running=False

def parse_mode(args):
    if args[1] == "-c":
        creat_segment(args[2], args[3])

def creat_segment(filename, segname):
    
    tiles = ""
    for i in range(map_size[1]):
        for f in range(map_size[0]):
            tiles += "g"
        tiles += "\n"

    result = segname + "#" + tiles + "#" + "?"

    with open(filename, "a") as fil:
        fil.write(result)

def merge_file():
    pass
  

def main():
	parse_args(sys.argv, len(sys.argv))

main()
