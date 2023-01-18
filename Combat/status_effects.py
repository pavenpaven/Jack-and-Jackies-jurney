import enum

auto = enum.auto
class Type(enum.Enum):
  FIRE = auto()
  WATER = auto()
  POISON = auto()
  ROCK = auto()
  NORMAL = auto()
  EXPLOTION = auto()

class Status_effect:
    NAME = ""
    DISAPEAR_AFTER_SPECIFIED_TICK = True
    STACK = True
    TICK_FREQUENCY = 1

    def __init__(self, unit, *args):
      self.arg = args[0]

    def tick_func(self, unit):
      pass
    
    def on_hit(self, unit):
      pass

    def on_expire(self, unit):
      pass

class Poison(Status_effect):
  NAME = "poison"
  DISAPEAR_AFTER_SPECIFIED_TICK = True
  STACK = True
  TICK_FREQUENCY = 4

  def __init__(self, unit, *args):
    self.arg = args[0]
    self.old_arg = self.arg
    self.poison = self.arg

  def tick_func(self, unit):
    self.poison += self.arg - self.old_arg
    self.old_arg = self.arg
    unit.health -= self.poison
    self.poison -= self.TICK_FREQUENCY
    
    
    
  

STATUS_EFFECT_COMBINATION = []
