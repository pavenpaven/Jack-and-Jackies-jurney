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
                    curser.change_tile(1)
                if event.key == pygame.K_z:
                    curser.change_tile(-1)
                n=0
                for j in tile_types.Tile_type.types:
                    if event.key == j.key:
                        scene.tiles[curser.pos[1]][curser.pos[0]] = n
                    n+=1
                curser.pos = (vec[0]+curser.pos[0], vec[1]+curser.pos[1])
                last_pressed=framecount
            if event.type == pygame.QUIT:
                quit = True
        return quit

    def graphics():
        window.fill((0,0,0))
        scene.render()
        window.blit(font.render("tut", False, (255,255,0)), (100,100))
        pygame.display.update()
        
    class Map:
        def __init__(self, size, pos): #size is a tuple
            self.size = size
            self.pos = pos
            #texture= pygame.image.load(backgrund_filename)
            #self.backgrund_tile = pygame.transform.scale(texture,size)
            self.surface = pygame.Surface((size[0]*tile, size[1]*tile))
            self.tiles = []
            self.loading_zone = []
    
        def load_room(self, filename, segname):
            segments = get_segname_room(filename, segname)
            row = segments[1].split("\n")
            self.tiles=[]
            u=0
            for i in row:
                row_tiles = []
                for f in i:
                    if f[0] == "1" or f[0] == "2" or f[0] == "3" or f[0] == "|":
                        if f[0] == "|":
                            u = -1
                        else:
                            u = int(f[0])
                    else:
                        row_tiles.append(tile_types.Tile_type.find(f).index - u)
                        u = 0
                self.tiles.append(row_tiles)
            
            
            lz_segs = segments[2].split(";") # lz_segs for loading_zone_segments
            if lz_segs[0]:
                func = lambda x: Loading_zone_cluster(int(x[0]), x[1], int(x[2]), int(x[3]), int(x[4]), int(x[5]), int(x[6]), int(x[7]))
                print(list(map(lambda x: x.split("."), lz_segs)))
                self.loading_zone = list(map(func, list(map(lambda x: x.split(".") ,lz_segs))))
                print(self.loading_zone)

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
            for i in self.loading_zone:
                rect = pygame.Rect(i.rect.x * tile + tile/2 - 5, i.rect.y * tile + tile / 2 - 5, 10, 10)
                pygame.draw.rect(self.surface, (255,0,0), rect)
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
            str_loading_info = ";".join(list(map(Loading_zone_cluster.string, self.loading_zone)))
            room_info = segname + "#" + self.convert_to_letters() + "#" + str_loading_info
            seg.insert(n, room_info)
            result = "?".join(seg)

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

    class Loading_zone_cluster:
        def __init__(self, point_index, segname, posx, posy, sizex, sizey, spawnx, spawny):
            self.rect = pygame.Rect((posx, posy), (sizex, sizey))
            self.linking_index = point_index
            self.spawn_pos = (spawnx, spawny)
            self.segname = segname

        def get_tiles(self):
            out = []
            n=0
            for i in range(self.rect.height):
                k = []
                for f in range(self.rect.width):
                    k.append((f, n))
                out.append(k)
                n+=1
            return out

        def string(self):
            str_rect = ".".join([str(self.rect.x), str(self.rect.y), str(self.rect.w), str(self.rect.h)])
            str_spawn = ".".join([str(self.spawn_pos[0]), str(self.spawn_pos[1])])
            print(self.spawn_pos)
            return ".".join([str(self.linking_index), self.segname, str_rect, str_spawn])


    class Curser:
        def __init__(self, pos, texture):
            tex = pygame.image.load(texture)
            self.texture = pygame.transform.scale(tex ,(tile, tile))
            self.pos = pos
        def change_tile(self, ammount):
            
            if scene.tiles[self.pos[1]][self.pos[0]] != len(tile_types.Tile_type.types) - 1:
                scene.tiles[self.pos[1]][self.pos[0]]+=ammount
            else:
                scene.tiles[self.pos[1]][self.pos[0]] = 0
        def loading_zone(self, segname):
            scene.tiles[self.pos[1]][self.pos[0]]


    curser = Curser((1,1), "Art/curser.png")
    scene = Map((30,12), (0, tile*2))      
    scene.load_room(filename, segname)
    window = pygame.display.set_mode((900,600))
    pygame.font.init()
    print(pygame.font.get_fonts())
    font = pygame.font.SysFont("roboto", 100)
    running = True
    clock = pygame.time.Clock()
    framecount = 0
    last_pressed = 0
    while running:
        clock.tick(30)
        framecount+=1
        if framecount % 100 == 0:
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
    if args[1] == "-list":
        list_segnames(args[2])
    if args[1] == "-l":
        place_loding_zone(args[3], args[4], args[2]) #-l (the segmentname to go to) filename segname

def creat_segment(filename, segname):
    
    tiles = ""
    for i in range(map_size[1]):
        for f in range(map_size[0]):
            tiles += "g"
        tiles += "\n"

    result = segname + "#" + tiles + "#" + "?"

    with open(filename, "a") as fil:
        fil.write(result)

def place_loading_zone():
    pass

def merge_file():
    pass

def list_segnames(filename):
    with open(filename, "r") as fil:
        tex = fil.read()
    
    for i in tex.split("?"):
        print(i.split("#")[0])

def main():
	parse_args(sys.argv, len(sys.argv))

main()
