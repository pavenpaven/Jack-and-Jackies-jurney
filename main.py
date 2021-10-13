import pygame
import tile_types

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
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
      last_pressed=framecount
      jack.walk((-1,0))
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
      last_pressed=framecount
      jack.walk((1,0))
    if keys[pygame.K_w] or keys[pygame.K_UP]:
      last_pressed=framecount
      jack.walk((0,-1))
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
      last_pressed=framecount
      jack.walk((0,1))
  return last_pressed
      

class Map:
    def __init__(self, size, pos): #size is a tuple
        self.size = size
        self.pos = pos
        self.surface = pygame.Surface((size[0]*tile, size[1]*tile))
        self.tiles = []
    
    def load_room(self, filename):
        fil = open(filename, "r")
        text = fil.read()
        fil.close()
        segments = text.split("#")
        row = segments[1].split("\n")
        self.tiles=[]
        for i in row:
            row_tiles = []
            for f in i:
                row_tiles.append(tile_types.Tile_type.find(f).index)
            self.tiles.append(row_tiles)
    
    def render(self):
        self.surface.fill((0,0,0))
        y = 0
        for i in self.tiles:
            x = 0
            for f in i:
                self.surface.blit(tile_types.Tile_type.types[f].texture, (x,y))
                x += tile
            y += tile
        self.surface.blit(jack.texture, jack.pos)
        window.blit(self.surface, self.pos)
            
            
    
scene = Map((10,10), (tile*5, tile*2))
scene.load_room("Level/test.txt")
print(scene.tiles)

class Player:
  def __init__(self, pos, filename, proporsion):
    self.pos = pos
    imag = pygame.image.load(filename)
    self.texture = pygame.transform.scale(imag, (proporsion[0], proporsion[1]))

  def render(self):
    pass
  
  def walk(self, vector):
    self.pos=(self.pos[0]+vector[0]*2, self.pos[1]+vector[1]*2)

jack = Player((30,30), "Art/jack.png", (20,28))

def get_touching_tiles(rect, ):
    pass

def main():
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
    last_pressed=check_key(framecount, last_pressed)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        running=False

main()
