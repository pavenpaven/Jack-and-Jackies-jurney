import pygame
import Combat.bar as bar
import Combat.button as button
import Combat.combat_unit as combat_unit 

class Icon:
  def __init__(self, pos, size, texture):
    self.pos = pos
    self.size = size
    self.texture = pygame.transform.scale(
      pygame.image.load(texture), (size[1],size[1]))

  def render(self, entity: combat_unit.Entity, scene):
    scene.blit(self.texture, self.pos)
    bar = self.get_bar(
      (self.pos[0] + self.size[1], self.pos[1] + self.size[1] / 4),
      (self.size[0], self.size[1] / 2), entity.max_health,
      entity.health, (255, 0, 0))
    bar.render(scene)
  
  def get_bar(self, pos, size, max, health, color) -> bar.Bar:
    x = bar.Bar(pos, size)
    x.update(max, health, color)
    return x
    #jag var här, heheheha #jag var också här, hehe

  def check_press(self, mouse_pos) -> bool:
    return button.is_point_in_rect(
      pygame.Rect(self.pos, self.size),
      mouse_pos
    )