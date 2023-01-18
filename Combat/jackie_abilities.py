import Combat.abilities as ab
import Combat.status_effects as se

class Punch(ab.Default_move):
  NAME = "punch"
  STARTUP_TIME = 10
  GLOBAL_COOLDOWN = 10
  COOLDOWN = 40
  STUN = 30
  DEFAULT_DAMAGE = 30

class Curse_status(se.Status_effect):
  NAME = "cursed"
  DISAPEAR_AFTER_SPECIFIED_TICK = False
  STACK = True
  TICK_FREQUENCY = 4

  def __init__(self, unit, *args):
    self.arg = args[0]
    unit.strength_multiplier *= 1 + (10*self.arg/100)

  def tick_func(self, unit):
    unit.health -= self.arg #true damage

  def on_expire():
    unit.strength_multiplier *= 1/(1 + (10*self.arg/100))
    #WARNING only works if strenght isnt set to a value for example let's say that there's a move that sets strength multiplier to 1 aka that would mean that if you aplply curse and then set strength to 1 and then curse expires you would have less than 1

class Curse_move(ab.Default_move):
  NAME="curse"
  STARTUP_TIME = 6
  GLOBAL_COOLDOWN = 8
  COOLDOWN = 28
  INTERUPTABLE = True
  INTERUPTING = False
  STUN = 0
  DEFAULT_DAMAGE = 0
  STATUS_EFFECTS = [(Curse_status, 1)]
  TARGET_ALLY = True
  TARGET_ENEMY = False
  NUM_ARGS = 0
  DESCRIPTION = "Apply 1 'curse' to an ally"


JACKIE_MOVES = [Punch, Curse_move]
