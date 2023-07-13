import pygame
import src.state as state
import Combat.graphics as graphics
import Combat.combat_scene as combat_scene
from Combat.combat_scene import basic as basic
import Combat.jackie_abilities as ja
import Combat.jane_abilities as jane


SCENE = [None] #maybe should've put in class these globals
TICK = [0]
SUBTICK = [0]
PLAYER = [None]
class U:
    PLAYER_MOVE = None
    @classmethod
    def return_func(cls, x):
        cls.PLAYER_MOVE = x
MENU = [None]

SCENE[0] = combat_scene.Combat_scene([basic("Player")], [basic("Enemy")]) 


def post_graphics(window, menu, events):
  menu.update(events)
  menu.draw(window)

def player_move(clock, unit, scene, tick):
  running = True
  framecount = 0
  last_pressed = 0
  class U:
    move_target = (None, None)
    @classmethod
    def return_move_target(cls, mv_target):
        cls.move_target = mv_target
        print(mv_target)
  menu = player_turn_menu(unit, scene, tick, U.return_move_target)
  while running:
    clock.tick(30)
    framecount+=1
    if U.move_target[0]:
        return U.move_target
    
    event_list = pygame.event.get()
    for event in event_list:
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()
        running = False

    post_graphics(menu, event_list)

c = lambda x,f: lambda *y:f(x,*y)

def startup(music):
    TICK[0] = 0
    SUBTICK[0] = 0

def combat_handler(window, framecount, eventlist, music):
    while not PLAYER[0]:
        if SCENE[0].win:
            return state.State.OVERWORLD
        if SCENE[0].lose:
            return state.State.GAMEOVER
        (TICK[0], SUBTICK[0], PLAYER[0]) = SCENE[0].simulate_sub_tick(TICK[0], SUBTICK[0], U.PLAYER_MOVE)
        U.PLAYER_MOVE = None
    if not MENU[0]:
        MENU[0] = graphics.player_turn_menu(PLAYER[0], SCENE[0], TICK[0], U.return_func) 
    post_graphics(window, MENU[0], eventlist)
    if U.PLAYER_MOVE:
        PLAYER[0] = None
        MENU[0] = None

    return state.State.COMBAT  
