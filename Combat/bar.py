import pygame

class Bar:
  def __init__(self, pos, size):
    self.size = size
    self.pos = pos
    self.surface=pygame.Surface(size)
    
  def update(self, max, current, color):
    rect = pygame.Rect((0,0), self.size)
    rect2 = pygame.Rect((0,0), (self.size[0]*(current/max),self.size[1]))
    
    pygame.draw.rect(self.surface, (255,255,255), rect)
    pygame.draw.rect(self.surface, color, rect2)
    pygame.draw.rect(self.surface, (0,0,0), rect, 2)
  def render(self, scene):
    scene.blit(self.surface, self.pos)
