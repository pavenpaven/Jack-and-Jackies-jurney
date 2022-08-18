import pygame

pygame.font.init()


def display_text(font, size, text) -> pygame.Surface: #size is size requierment for text 
    lines = []
    line = ""
    for i in text.split(" "):
        i+=" "
        if font.size(line+i)[0] > size[0]:
            lines.append(line)
            line=""
        line += i

    if line:
        lines.append(line)
    
    width = max(list(map(lambda x:font.size(x)[0], lines)))
    height = sum(list(map(lambda x:font.size(x)[1], lines)))
    
    if height > size[1]:
        print("Warning text height exeeding bounds")

    surface = pygame.Surface((width, height))
    
    y_offset = 0
    for i in lines:
        surface.blit(font.render(i, True, (255, 255, 255)), (0, y_offset))

        y_offset += font.size(i)[1]

    return surface


class Text_box:
  def __init__(self, rect, font, outline=2):
    self.surface = pygame.Surface(rect.size)
    self.rect = pygame.Rect((0,0), rect.size)
    self.pos = (rect.x, rect.y)
    self.outline = outline
    self.font = font
    self.dialog = []

  def advance(self) -> bool: #returns True if end of Text_box
    if not len(self.dialog):
      return True
    self.surface.fill((0,0,0))
    pygame.draw.rect(self.surface, (255,255,255), self.rect, self.outline)
    text_surface=display_text(self.font, self.rect.size, self.dialog.pop(0))
    text_rect = text_surface.get_rect()
    cpy_rect = self.rect.copy()
    cpy_rect.move((0,0))
    text_rect.center = cpy_rect.center
    self.surface.blit(
      text_surface, (text_rect.x, text_rect.y)
    )
    return False
