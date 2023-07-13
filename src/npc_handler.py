import pygame
import src.world_handler as world_handler #intressting twist
import src.state as state
import src.npc as npc
import src.enemy_actor
import src.text_box as text_box
import key

def startup():
  text_box.dialog = npc.DIALOG_TEXT[0]
  text_box.advance()

def npc_handler(window, framecount, eventlist) -> state.State:
  graphics(window)
  if check_keys(framecount, eventlist):
    return text_box.dialog_exit_state
  return state.State.NPC_DIALOG

  
def graphics(window):
  world_handler.graphics(window, None) # Do you ever look at someone and wonder "what is going on inside thier head"
  window.blit(text_box.surface, text_box.pos)
 
def check_keys(framecount, eventlist):
  if key.is_keydown(eventlist, "x", framecount):
    return text_box.advance()
  return False

pygame.font.init()
NPC_FONT = pygame.font.SysFont("joystix monospace.ttf", 25)
   

text_box = text_box.Text_box(pygame.Rect((90,280), (720, 125)), NPC_FONT)
