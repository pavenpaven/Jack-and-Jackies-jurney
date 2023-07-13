import src.actor as actor
import src.npc as npc
import src.state as state
import Combat.combat_handler as combat_handler
import Combat.jane_abilities as ja
import Combat.combat_scene as cs


#class Enemy(actor.Sprite):
class Enemy(npc.Npc):
    dialog_exit_state = state.State.COMBAT
    combat_scene = None

    def player_action(self):
        combat_handler.SCENE[0] = self.combat_scene
        npc.Npc.player_action(self)

class Jane(Enemy):
    name = "jane"
    combat_scene = cs.Combat_scene([cs.basic("player 1"), cs.basic("player 2")], [cs.vasic("Jane", ja.JANE_MOVES)]) 

actor.SPRITE_CLASSES.append(Jane)
