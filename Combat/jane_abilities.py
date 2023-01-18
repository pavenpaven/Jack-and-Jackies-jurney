import Combat.abilities as ab
import Combat.status_effects as se

class Heal_effect(se.Status_effect):
  DISAPEAR_AFTER_SPECIFIED_TICK = True
  STACK = True
  TICK_FREQUENCY = 1

  def tick_func(self, unit):
    if unit.health < unit.max_health: #becose integer
      unit.health += 1

class Heal(ab.Wait_move):
  NAME = "heal"
  DESCRIPTION = "Applies 4n heal with n statup "
  GLOBAL_COOLDOWN = 2
  TARGET_ALLY = True

  def startup(self, unit, *args):
    self.arg = self.args[0]
    self.heal = 4*self.args[0]
    self.STARTUP_TIME = self.args[0]
    self.COOLDOWN = self.args[0] + 2 + 2

  def mana_cost_of_first_arg(self, arg):
      return arg

  def ontime_func(self, unit, target, tick, *args):
    target.apply_status_effect(Heal_effect(target, self.heal), tick)

class Jar_of_bees(ab.Default_move):
  MANA_COST=0
  NAME="Jar of Bees"
  STARTUP_TIME = 2
  GLOBAL_COOLDOWN = 10
  COOLDOWN = 62
  INTERUPTABLE = True
  INTERUPTING = True
  STUN = 0
  DEFAULT_DAMAGE = 1
  STATUS_EFFECTS = [(se.Poison, 4)]
  TARGET_ALLY = True
  TARGET_ENEMY = True
  DESCRIPTION = "A jar of bees, How and why i wonder? They look pretty angry in there. - Aplies 4 'poison'."

  
JANE_MOVES =[Jar_of_bees, Heal]
