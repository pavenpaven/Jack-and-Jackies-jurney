import pygame
import src.actor as actor
import src.state as state

DIALOG_TEXT = [[]] # will only be displayed when in dialog state look npc_handler from state_handler

def load_npc_dialog(segname, filename):
  with open(filename, "r") as fil:
    txt=fil.read()
  
  txt = txt.split(";\n")
  txt = list(map(lambda x:x.split(":"), txt))

  for i in txt:
    print(segname, i[0])
    
  seg = list(filter(lambda x:segname==x[0], txt))
  if not seg==[]:
    return seg

class Npc(actor.Sprite):
  name = "npc"
  texture = actor.re("Art/jane.png", (30,30))
  size = (30,30)
  collision = True
  interactable = True
  
  def startup_process(self, extra):
    x=load_npc_dialog(extra,"Level/npc")
    if x == None:
      print(f"npc name {extra} not found probobly")
      return None
    self.npc_name = extra
    x = x[0][1]
    x.replace("\n", "")
    x = x.split("#")
    x = list(map(lambda x:x.replace("\n",""),x))
    try:
      self.texture = actor.re(x[0].replace("\n", ""), (18,20))
    except:
      print(f"npc {self.npc_name} texture bad {x[0]}")
    self.dialog = x[1:len(x)-1]

  def player_action(self):
    DIALOG_TEXT[0] = self.dialog.copy()
    self.change_state(state.State.NPC_DIALOG)
    
     


actor.SPRITE_CLASSES.append(Npc) #wtf