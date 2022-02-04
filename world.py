import math
import pygame
import tile_types

tile = 30

class Loading_zone_cluster:
    def __init__(self, point_index, segname, posx, posy, sizex, sizey, spawnx, spawny):
        self.rect = pygame.Rect((posx*tile, posy*tile), (sizex*tile, sizey*tile))
        self.linking_index = point_index
        self.spawn_pos = (spawnx*tile, spawny*tile)
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

def get_segname_room(filename, segname):
    with open(filename, "r") as fil:
        text = fil.read()
        
    for i in text.split("?"):
        segments = i.split("#")
        if segments[0].replace("\n", "") == segname:
            break
    else:
        print("no segment name named: ", segname)
        pygame.quit()
        exit()
    return "#".join(segments)    

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
            segments = segments.split("#")
            row = segments[1].split("\n")
            self.tiles=[]
            u=0
            for i in row:
                row_tiles = []
                for f in i:
                    if f[0] == "1" or f[0] == "2" or f[0] == "3":
                        u = int(f[0])
                    else:
                        row_tiles.append(tile_types.Tile_type.find(f).index - u)
                        u = 0
                self.tiles.append(row_tiles)
            
            lz_segs = segments[2].split(";") # lz_segs for loading_zone_segments
            if lz_segs[0]: # only in case of loading zones being present
                func = lambda x: Loading_zone_cluster(int(x[0]), x[1], int(x[2]), int(x[3]), int(x[4]), int(x[5]), int(x[6]), int(x[7]))
                print(list(map(lambda x: x.split("."), lz_segs)))
                self.loading_zone = list(map(func, list(map(lambda x: x.split(".") ,lz_segs))))
                print(self.loading_zone[0].rect, "loading")

        def render(self, window, player):
            self.surface.fill((0,0,0))
            #self.surface.blit(self.backgrund_tile, (0,0))
            y = 0
            for i in self.tiles:
                x = 0
                for f in i:
                    self.surface.blit(tile_types.Tile_type.types[f].texture, (x,y))
                    x += tile
                y += tile
            self.surface.blit(player.texture, player.pos)
            window.blit(self.surface, self.pos)
        
        def save(self, filename, segname):
            with open(filename, "r") as fil:
                tex = fil.read()
            n = 0
            seg = tex.split("?") 
            for i in seg:
                if i.split("#")[0].replace("\n", "") == segname:
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
