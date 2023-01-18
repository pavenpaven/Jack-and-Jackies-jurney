import pygame
import Combat.combat_unit as combat_unit

pygame.font.init()

def is_point_in_rect(rect, pos):
      if rect.left < pos[0] < rect.left + rect.size[0]:
        if rect.top < pos[1] < rect.top + rect.size[1]:
          return True
      return False

class Button:
    FONT = pygame.font.SysFont("roboto", 20) #pygame
    def __init__(self, pos, size, txt, func):
        self.pos = pos
        self.size = size
      
        self.surface = pygame.Surface(size)

        rect=pygame.Rect((0,0), size)
      
        pygame.draw.rect(self.surface, (25,75,80), rect)
        pygame.draw.rect(self.surface, (0,0,0), rect, 2)
      
        self.surface.blit(self.FONT.render(txt, False, (0,0,0)), (2,4))
        self.func = func
    
    def check_if_pressed(self, pos):
      if is_point_in_rect(
        pygame.Rect(self.pos, self.size),
        pos):
        self.func()

    def render(self, scene):
      scene.blit(self.surface,self.pos)


def check_buttons(pos, buttons):
  for i in buttons:
    i.check_if_pressed(pos)

def get_move_buttons(entity: combat_unit.Entity, pos, combat_scene):
  WIDTH = 100
  HIGHT = 20

  c = lambda f, x: lambda: f(x)  # warning skit code #yes -chim # när du ser den här koden bara blunda - paven

  out = []
  for n, i in enumerate(entity.moves):
    f = c(combat_scene.on_pressed_move_button, i)
    out.append(
      Button((pos[0], pos[1] + (n * HIGHT)), (WIDTH, HIGHT),
                    i.NAME, f))

  return out
