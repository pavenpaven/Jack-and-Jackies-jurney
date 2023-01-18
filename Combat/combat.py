import pygame
import Combat.combat_unit as combat_unit
import Combat.abilities as abilities
import Combat.button as button
import Combat.icon as icon

ENTITY_WIDTH = 200
ENTITY_HIGHT = 50

class Combat_scene: #new constructor som tar in enemies och allies som arrays
    def __init__(self, allies: [combat_unit.Entity], enemies: [combat_unit.Entity]):
        self.pressed_move = None 
        self.surface=pygame.Surface((900,600))

        self.ally_icons = dict(zip(allies, [icon.Icon((10,10+n*ENTITY_HIGHT), (ENTITY_WIDTH, ENTITY_HIGHT), i.texture) for n,i in enumerate(allies)]))
        self.enemy_icons = dict(zip(enemies, [icon.Icon((300,10+n*ENTITY_HIGHT), (ENTITY_WIDTH, ENTITY_HIGHT), i.texture) for n,i in enumerate(enemies)]))
      
        self.entity_turn = allies[0]

        self.button_array = button.get_move_buttons(allies[0], (100,200), self)

    def render(self, scene):
      scene.blit(self.surface, (0,0))

    def update_surface(self):
      self.surface.fill((0,100,0))
      for n,i in enumerate(self.ally_icons.items()): #ally_icons.keys
        i[1].render(i[0], self.surface)

      for n,i in enumerate(self.enemy_icons.items()):
        i[1].render(i[0], self.surface)
      #i[1] is the value i.e icons and i[0] is the key i.e entity

      for i in self.button_array:
        i.render(self.surface)

    def attack_move_handler(self, move, choice, entity):
        is_dead = self.enemies[choice].take_damage(
            move.function(entity))
        self.update_surface()
        print(f"you used  {move.NAME} on the enemy.")
        if is_dead:
            self.enemies.pop(choice)
            print(f"Enemy {choice} is dead")

    def buff_move_handler(self, move, choice, entity):
        move.function(entity, self.players[choice])
        print(f"Used {move.NAME} on {self.players[choice]}")

    def move_handler(self, move, target):
      #this is scaleble zo'o
      if move.TYPE == abilities.Move_type.ATTACK:
        target.take_damage(move.function(self.entity_turn))
        print(f"damaged and now has {target.health}, {move.function(self.entity_turn)}")
      elif move.TYPE == abilities.Move_type.BUFF:
        pass
      print(f"wolo you have used se move {move.NAME} on {target}")
        
        

    def check_mouse(self, pos):
      for i in self.button_array:
        i.check_if_pressed(pos)

      if self.pressed_move.TYPE == abilities.Move_type.ATTACK:
        x = list(filter(lambda x:self.enemy_icons[x].check_press(pos), self.enemy_icons))
        print(x)
        if x:
          self.move_handler(self.pressed_move, x[0])
      elif self.pressed_move.TYPE == abilities.Move_type.BUFF :
        x = list(filter(lambda x:x.icon.check_press(pos), self.players))
        if x:
          self.move_handler(self.pressed_move, x[0])
          
    def on_pressed_move_button(self,move):
      print(self.pressed_move)
      self.pressed_move = move
      print(move.NAME)
      #if pressed move is not None then that indicates that you should press an icon to target either a enemy or a ally might make aoe abilities without targeting. and also other non move buttons wich i don̈́'t want realise as a move. but then again i could make that button array diffrent sence this is made from composing a function with a move and assosiating that funktion with a button i do think that move is a good compromise between purly functions wich kinda wood imply a lot of repetition, and a purly data centered view on moves wich wood be cringe probobly
