import enum
import Combat.status_effects
import math

#Mana cost is used for ammo and energy to

class Move_type(enum.Enum):
  ATTACK = enum.auto()
  BUFF = enum.auto()

class Default_move:
  MANA_COST=0
  NAME="default"
  TYPE=Move_type.ATTACK
  STARTUP_TIME = 10
  GLOBAL_COOLDOWN = 10
  COOLDOWN = 20
  INTERUPTABLE = True
  INTERUPTING = True
  STUN = 5
  DEFAULT_DAMAGE = 10
  STATUS_EFFECTS = []
  TARGET_ALLY = False
  TARGET_ENEMY = True
  NUM_ARGS = 0
  DESCRIPTION = "Normal attack move"

  def __repr__(self):
    return self.NAME
  
  def __init__(self, unit, *args):
    self.args = args
    self.startup(unit, *args)

  def startup(self, unit, *args):
    pass

  def fundamental_ontime_func(self, unit, target, tick, scene):
    if self.NUM_ARGS:
        a = self.mana_cost_of_first_arg(self.args[0])
        if a:
            self.MANA_COST = a
    if unit.mana < self.MANA_COST:
      raise Exception(f"to little mana for {unit}")
    unit.mana -= self.MANA_COST
    self.ontime_func(unit, target, tick, scene, *self.args)

  def ontime_func(self, unit, target, tick, scene, *args):
    target.take_damage(self.DEFAULT_DAMAGE*unit.strength_multiplier)
    if target.active_move[0].INTERUPTABLE and self.INTERUPTING:
      print(f"move {target.active_move[0]} interupted at tick {tick}")
      target.active_move = (Wait_move(target, (self.STUN)), target.active_move[1], tick)
    for i in self.STATUS_EFFECTS:
      if not i[1]:
        degree = math.ceil(self.DEFAULT_DAMAGE/10) #fix
      target.apply_status_effect(i[0](target, i[1]), tick)

  def mana_cost_of_first_arg(self, arg): #returns None if such function doesnt exist manly because first arg doesnt have to be int
      pass

  @classmethod
  def info(cls):
    a = f"Name: {cls.NAME}"
    if cls.STARTUP_TIME == 0:
      a+="\nStartup time most likly variable see notes and that changes Global inclusive cooldown"
    else:
      a+=f"\nStatup {cls.STARTUP_TIME} ticks"
    a+= f"\nInclusive Global cooldown {cls.STARTUP_TIME + cls.GLOBAL_COOLDOWN}\nCooldown (from initialization) {cls.COOLDOWN}"
    if cls.DEFAULT_DAMAGE != 0:
      a += f"\nDefault damage (before armor) {cls.DEFAULT_DAMAGE}\nTargets Enemies {cls.TARGET_ENEMY}\nTargets allies {cls.TARGET_ALLY}\nInterupting: {cls.INTERUPTING}"
      if cls.INTERUPTING:
        a+=f"\nStun {cls.STUN} ticks"
    
    a += f"\nInteruptable: {cls.INTERUPTABLE}"
    return a + "\n-" +cls.DESCRIPTION
      

class Kick_move(Default_move):
  NAME = "kick"
  STARTUP_TIME = 5
  GLOBAL_COOLDOWN = 20
  COOLDOWN = 40
  STUN = 13
  DEFAULT_DAMAGE = 50

class Wait_move(Default_move):
    NAME = "wait"
    STARTUP_TIME = 0
    GLOBAL_COOLDOWN = 0
    COOLDOWN = 0
    DEFAULT_DAMAGE = 0 # doesnt attack
    TARGET_ENEMY = False
    NUM_ARGS = 1
    DESCRIPTION = "Just waits n ticks"

    def __repr__(self):
      return f"{self.NAME} {self.arg}"

    def startup(self, unit, *args: [int]):
        self.GLOBAL_COOLDOWN = self.args[0]
        self.arg = self.args[0]

    def ontime_func(self, unit, target, tick, scene, *args):
      pass


class Shoot_move(Default_move):
    NAME = "shoot"
    STARTUP_TIME = 3
    GLOBAL_COOLDOWN = 13
    COOLDOWN = 20
    DEFAULT_DAMAGE = 60
    INTERUPTING = False
    DESCRIPTION = "Shoot is a strong move but wastes a 'bullet' and also doesnt interupt"

    def ontime_func(self, unit, target, tick, scene, *args):
      if len(unit.magasine) ==0:
        raise Exception("To few bullets")
      unit.magasine.pop(0) 
      target.take_damage(self.DEFAULT_DAMAGE)

class Reload(Wait_move):
  NAME = "reload"
  GLOBAL_COOLDOWN = 10
  DESCRIPTION = "Reload gives you 'bulletes' with a the startuptime increceing by 2 for every bullet and the cooldown is 2n + 12 wich means that if it doesnt get interupted its Cooldown is 2 in the beggining of the next turn after using it"

  def startup(self, unit, *args):
    self.STARTUP_TIME = 2*self.args[0]
    self.COOLDOWN = 2*self.args[0]+12
    self.arg = self.args[0]

  def ontime_func(self, unit, target, tick, scene, *args):
    for i in range(self.arg):
      if len(unit.magasine) < 6:
        unit.magasine.append(None)

class Gun_bash(Default_move):
  NAME = "gunbash"
  DEFAULT_DAMAGE =45
  STARTUP_TIME = 13
  GLOBAL_COOLDOWN = 5
  COOLDOWN = 45
  STUN = 6
  DESCRIPTION = "Long setup but gives Jack a 'bullet'"

  def ontime_func(self, unit, target, tick, scene, *args):
    if len(unit.magasine) < 6:
      unit.magasine.append(None)
    Default_move.ontime_func(self, unit, target, tick, scene, *args)
  
class Summon(Default_move):
    NAME = "summon"
    STARTUP_TIME = 3
    GLOBAL_COOLDOWN = 10
    COOLDOWN = 30
    
    def ontime_func(self, unit, target, tick, scene, *args):
        pass


LIST_OF_MOVES = [Default_move, Kick_move, Wait_move]

JACK_MOVES = [Shoot_move, Reload, Gun_bash]

def string_to_move_class(str, move_class_list=LIST_OF_MOVES):
  for i in move_class_list:
    if i.NAME == str:
      return i
  raise Exception(f"Im afirad you can't do {str}, Dave.")
