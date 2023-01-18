import Combat.abilities as abilities
import Combat.entity_type as entity_type
import math

class Entity:
    def __init__(self, texture, moves, max_health, max_mana, default_armor, name):
        self.texture=texture
        self.moves = list(map(lambda x: (x, -math.inf), moves))
        self.active_move = (None, None, 0) # tuple of move and when move initiated and target (can be None)
        self.health = max_health
        self.mana = max_mana
        self.armor = default_armor
        self.max_health = max_health
        self.max_mana = max_mana
        self.default_armor = default_armor
        self.magasine = [None, None, None] 
        self.name = name
        self.strength_multiplier = 1
        self.status_effects = [] #tuple with freq cooldown

    def __repr__(self):
        a = f"{self.name} hp: {self.health} "
        if self.active_move[0]:
            a+=f"am: {(self.active_move[0], self.active_move[2])}"
        if self.name == "Jack":
          a+=f"ammo: {len(self.magasine)}"
        if self.name == "Jackie":
          a+=f"energy {self.mana}"
        if self.name == "Jane":
          a+=f"Mana: {self.mana}"
        return a

    def info(self, tick):
      if self.status_effects:
        status_ef = f"\nStatus_effects: {self.status_effects}"
      else:
        status_ef = ""
      if self.active_move[1]:
        target_name = self.active_move[1].name
      else:
        target_name = None
      if self.active_move[0]:
          active = f"\nActive Move: {self.active_move[0], target_name, self.active_move[2]} will hit in {self.active_move[0].STARTUP_TIME + self.active_move[2] - tick} ticks \nand will be done in {self.active_move[0].STARTUP_TIME + self.active_move[0].GLOBAL_COOLDOWN + self.active_move[2] - tick} ticks"     
      else:
          active = ""
      return str(self) +f"\nArmor: {self.armor}\nMoves:\n"+"\n".join([str((i[0].NAME, max(i[0].COOLDOWN - tick + i[1], 0))) for i in self.moves]) + active + f"\nStrength multiplier: {self.strength_multiplier}" + status_ef
      
    def handle_status_effects(self, tick):
      for n,i in enumerate(self.status_effects):
        if tick - i[1] >= i[0].arg and i[0].DISAPEAR_AFTER_SPECIFIED_TICK:
          i[0].on_expire(self)
          self.status_effects.pop(n)
          
        if not (tick - i[1]) % i[0].TICK_FREQUENCY:
          i[0].tick_func(self) # porno #;)
          

    def apply_status_effect(self, status_effect, tick):
      if status_effect.__class__ in [i.__class__ for i in self.status_effects]:
        if status_effect.STACK:
          list(filter(lambda x:x.__class__==status_effect.__class__, self.status_effects))[0].arg += status_effect.arg
        else:
          self.status_effects.append((status_effect, tick))
      else:
        self.status_effects.append((status_effect, tick))
          
  
    @classmethod
    def from_type(cls, type: entity_type.Entity_type):
        return cls(type.texture, type.moves, type.max_health, type.max_mana, type.default_armor)

    def take_damage(self, damage):
        if damage: # attacking 0 would resoult in div by 0
          self.health -= math.ceil(damage / (2**(self.armor/damage))) #usual magic
      
        if self.health < 1:
            print("dead")
            return 1
        return 0

    def get_move_index(self, move) -> (abilities.Default_move, int):
      return list(filter(lambda x:x[1][0]==move, enumerate(self.moves)))[0][0]
