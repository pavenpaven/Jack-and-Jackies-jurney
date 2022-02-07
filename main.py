import pygame
import math
import sys
import src.tile_types as tile_types
import src.world as world
import src.conf as conf

window = pygame.display.set_mode((900,600))

tile = world.tile

imag = pygame.image.load("Art/Flower_1.png")
imag = pygame.transform.scale(imag, (tile, tile))
imag2 = pygame.image.load("Art/jack.png")
imag2 = pygame.transform.scale(imag2, (20,18 ))
 

def graphics():
  window.fill((0,0,0))
  scene.render(window, jack)
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
      
scene = world.Map((30,12), (0, tile*2))
scene.load_room(conf.conf_search("starting_filename"), conf.conf_search("starting_segname")) #revert to ma
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
  
  def check_loading_zone(self, player_hitbox):
      x = player_hitbox.collidelistall(list(map(lambda x: x.rect, scene.loading_zone)))
      if x:
        x=x[0] #yes
        lz = scene.loading_zone[x]
        scene.load_room("Level/natan", lz.segname)
        self.pos = lz.spawn_pos
        
  def walk(self, vector):
    if vector[0] and vector[1]:
        vector[0] *= math.sqrt(2)/2
        vector[1] *= math.sqrt(2)/2 # just dont ansk
    travel_pos = (self.pos[0] + vector[0]*self.speed , self.pos[1]+vector[1]*self.speed)
    player_hitbox = ((travel_pos[0], travel_pos[1]+20), (travel_pos[0] + self.size[0], travel_pos[1] + (self.size[1]/3)))
    tiles = get_touching_tiles(player_hitbox, scene)
    can_go = True
    for i in tiles:
        if tile_types.Tile_type.types[scene.tiles[i[1]][i[0]]].collision:
            can_go = False
    if can_go:
        self.pos = travel_pos
    self.check_loading_zone(pygame.Rect(player_hitbox[0], (self.size))) 

jack = Player((100,100), "Art/jack.png", (20,28), 5)

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
