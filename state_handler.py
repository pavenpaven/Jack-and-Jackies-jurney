import enum
import src.world_handler as world_handler
import src.npc_handler as npc_handler
import src.state as st

class previous:
  state = None

def state_handling(state, scene, framecount, event_list) -> st.State:
  if state == st.State.OVERWORLD:
    return world_handler.overworld_handler(scene, framecount, event_list)
  elif state == st.State.COMBAT:
    return combat_handler(scene, framecount, event_list)
  elif state == st.State.NPC_DIALOG:
    if previous.state != state:
      npc_handler.startup()
      return npc_handler.npc_handler(scene, framecount, event_list)# copy line because it wood blink annars i en frame och dialog startar 1 frame snabbare 100 iq lol men det hade inte påverkat en tas pga 2 frame delay att du trycker x.
    else:
      x= npc_handler.npc_handler(scene, framecount, event_list)
      return x

def combat_handler():
  pass