import enum
import src.world_handler as world_handler
import src.npc_handler as npc_handler
import Combat.combat_handler as combat_handler
import src.gameover as gameover
import src.title as title
import src.state as st

class previous:
  state = None

def state_handling(state, scene, framecount, event_list, music) -> st.State:
  if state == st.State.OVERWORLD:
    return world_handler.overworld_handler(scene, framecount, event_list, music)
  elif state == st.State.COMBAT:
    if previous.state != state:
      combat_handler.startup(music)
      return combat_handler.combat_handler(scene, framecount, event_list, music)
    return combat_handler.combat_handler(scene, framecount, event_list, music)
  elif state == st.State.NPC_DIALOG:
    if previous.state != state:
      npc_handler.startup()
      return npc_handler.npc_handler(scene, framecount, event_list)# copy line because it wood blink annars i en frame och dialog startar 1 frame snabbare 100 iq lol men det hade inte påverkat en tas pga 2 frame delay att du trycker x.
    else:
      x= npc_handler.npc_handler(scene, framecount, event_list)
      return x
  elif state == st.State.TITLE:
    if previous.state != state:
      title.startup(music)
      return title.title_handler(scene, framecount, event_list)
    return title.title_handler(scene, framecount, event_list)
  elif state == st.State.GAMEOVER:
    if previous.state != state:
      gameover.startup(music)
      return gameover.gameover_handler(scene, framecount, event_list)
    return gameover.gameover_handler(scene, framecount, event_list)
