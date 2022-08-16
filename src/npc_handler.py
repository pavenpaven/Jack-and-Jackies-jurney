import pygame
import src.world_handler as world_handler #intressting twist
import src.state as state
import src.npc as npc
import key

def startup():
  text_box.dialog = npc.DIALOG_TEXT[0]
  text_box.advance()

def npc_handler(window, framecount, eventlist) -> state.State:
  graphics(window)
  if check_keys(framecount, eventlist):
    return state.State.OVERWORLD
  return state.State.NPC_DIALOG

  
def graphics(window):
  world_handler.graphics(window)
  window.blit(text_box.surface, text_box.pos)
  
def check_keys(framecount, eventlist):
  if key.is_keydown(eventlist, "x", framecount):
    return text_box.advance()
  return False

pygame.font.init()

NPC_FONT = pygame.font.SysFont("roboto", 50)

class Text_box:
  def __init__(self, rect, outline=2):
    self.surface = pygame.Surface(rect.size)
    self.rect = pygame.Rect((0,0), rect.size)
    self.pos = (rect.x, rect.y)
    self.outline = outline
    self.dialog = []

  def advance(self) -> bool: #returns True if end of Text_box
    if not len(self.dialog):
      return True
    self.surface.fill((0,0,0))
    pygame.draw.rect(self.surface, (255,255,255), self.rect, width=self.outline)
    text_surface=NPC_FONT.render(self.dialog.pop(0), True, (255,255,255))
    text_rect = text_surface.get_rect()
    cpy_rect = self.rect.copy()
    cpy_rect.move((0,0))
    text_rect.center = cpy_rect.center
    self.surface.blit(
      text_surface, (text_rect.x, text_rect.y)
    )
    return False
    

text_box = Text_box(pygame.Rect((350,280), (500, 125)))