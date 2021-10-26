import pygame
import tile_types
import math

window = pygame.display.set_mode((900,600))

tile=30

imag = pygame.image.load("Art/Flower_1.png")
imag = pygame.transform.scale(imag, (tile, tile))
imag2 = pygame.image.load("Art/jack.png")
imag2 = pygame.transform.scale(imag2, (20,18 ))
 

def graphics():
  window.fill((0,0,0))
  scene.render()
  jack.render()
  pygame.display.update()

def check_key(framecount,last_pressed):
  keys = pygame.key.get_pressed()
  pygame.key.set_repeat(1, 100000000)
  if True:
    vec = [0, 0]
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
      last_pressed=framecount
      vec[0]+=-1
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
      last_pressed=framecount
      vec[0]+=1
    if keys[pygame.K_w] or keys[pygame.K_UP]:
      last_pressed=framecount
      vec[1] +=-1
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
      last_pressed=framecount
      vec[1] +=1
    if vec[0] or vec[1]:
        jack.walk(vec)
  return last_pressed
      
def get_segname_room(filename, segname):
    with open(filename, "r") as fil:
        text = fil.read()
    return text
    
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
            self.surface.blit(jack.texture, jack.pos)
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
            
            
    
scene = Map((30,12), (0, tile*2))
scene.load_room("Level/test1", "test")
print(scene.tiles)

class Player:
  def __init__(self, pos, filename, proporsion, speed):
    self.pos = pos
    self.speed = speed
    self.size = proporsion
    imag = pygame.image.load(filename)
    self.texture = pygame.transform.scale(imag, (proporsion[0], proporsion[1]))

  def render(self):
    pass
  
  def walk(self, vector):
    if vector[0] and vector[1]:
        vector[0] *= math.sqrt(2)/2
        vector[1] *= math.sqrt(2)/2 # just dont ansk
    travel_pos = (self.pos[0] + vector[0]*self.speed , self.pos[1]+vector[1]*self.speed)
    player_hitbox = (travel_pos, (travel_pos[0] + self.size[0], travel_pos[1] + self.size[1]))
    tiles = get_touching_tiles(player_hitbox, scene)
    can_go = True
    for i in tiles:
        if tile_types.Tile_type.types[scene.tiles[i[1]][i[0]]].collision:
            can_go = False
    if can_go:
        self.pos = travel_pos

jack = Player((30,30), "Art/jack.png", (20,28), 3)

def get_touching_tiles(rect, sce): #sce for scene idk why
    out = []
    points = [rect[0], rect[1], (rect[0][0], rect[1][1]), (rect[1][0], rect[0][1])]
    for i in points:
        out.append((math.trunc(i[0]/tile), math.trunc(i[1]/tile)))
    return out

def main():
  running = True
  clock = pygame.time.Clock()
  framecount = 0
  last_pressed = 0 
  print(get_touching_tiles(((30,30),(70,100)), scene))
  while running:
    clock.tick(30)
    framecount+=1
    if framecount % 60 == 0:
        print(clock.get_fps())
    graphics()
    last_pressed=check_key(framecount, last_pressed)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        running=False

main()
