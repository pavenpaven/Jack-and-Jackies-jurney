import pygame
import math
import src.world as world
import src.tile_types as tile_types
import src.actor as actor

tile = world.tile

class Player:
  def __init__(self, pos, filename, proporsion, speed):
    self.pos = pos
    self.speed = speed
    self.size = proporsion
    imag = pygame.image.load(filename)
    self.texture = pygame.transform.scale(imag, (proporsion[0], proporsion[1]))

  def render(self):
    pass

  def use_button(self, actors: [actor.Sprite]): #or inherited from Sprite
    actors = list(filter(lambda x:x.interactable, actors))
    
    actors_in_range = list(
      map(
        lambda x: (x, math.sqrt(((self.pos[0]-x.pos[0])**2)+(self.pos[1]-x.pos[1])**2)), actors
      )
    ) #lol creats a list of touples were actors in the scene isn index 0 and distance is index 1

    actors_in_range = list(filter(lambda x: x[1]<tile*1.5, actors_in_range))
    if not actors_in_range:
      return 0
    actors_in_range.sort(key=(lambda x: x[1]))
    actors_in_range[0][0].player_action()
    return 1
    
    
  
  def check_loading_zone(self, player_hitbox, scene):
      x = player_hitbox.collidelistall(list(map(lambda x: x.rect, scene.loading_zone)))
      if x:
        x=x[0] #yes
        lz = scene.loading_zone[x]
        scene.load_room("Level/natan", lz.segname)
        self.pos = lz.spawn_pos
        
  def walk(self, vector, scene):
    if vector[0] and vector[1]:
        vector[0] *= math.sqrt(2)/2
        vector[1] *= math.sqrt(2)/2 # just dont ansk
    travel_pos = (self.pos[0] + vector[0]*self.speed , self.pos[1]+vector[1]*self.speed)
    player_hitbox = ((travel_pos[0], travel_pos[1]+20), (travel_pos[0] + self.size[0], travel_pos[1] + (self.size[1]/3)))
    
    can_go=check_collision(player_hitbox,scene, (pygame.Rect(player_hitbox[0], (self.size[0], self.size[1]/3))))
    
    if can_go:
        self.pos = travel_pos
    self.check_loading_zone(pygame.Rect(player_hitbox[0], (self.size[0], self.size[1]/3)), scene) 


def check_collision(player_hitbox, scene, player_rect):
    tiles = get_touching_tiles(player_hitbox, scene)
    can_go = True
    for i in tiles:
        if tile_types.Tile_type.types[scene.tiles[i[1]][i[0]]].collision:
            can_go = False

    for i in scene.actors:
      if i.collision:  
        if player_rect.colliderect(pygame.Rect(i.pos,i.size)):
          can_go = False
        
    return can_go
  


def get_touching_tiles(rect, sce): #sce for scene idk why
    out = []
    points = [rect[0], rect[1], (rect[0][0], rect[1][1]), (rect[1][0], rect[0][1])]
    for i in points:
        out.append((math.trunc(i[0]/tile), math.trunc(i[1]/tile)))
    return out
