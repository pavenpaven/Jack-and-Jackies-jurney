import pygame

def re(filename, size):
  x=pygame.image.load(filename)
  return pygame.transform.scale(x, size)

class Sprite:
  texture=re("Art/unknown.png", (1,1))
  size=(1,1)
  collision=False
  def __init__(self, pos, size):
    self.pos = pos
  def render(self, scene):
    scene.blit(self.texture, self.pos)