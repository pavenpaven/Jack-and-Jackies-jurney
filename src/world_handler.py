import pygame
import src.player as player
import src.world as world
import src.actor as actor
import src.conf as conf
import src.state as state
import key

tile = world.tile

def overworld_handler(window, framecount, event_list) -> state.State:
  scene.state = state.State.OVERWORLD
  graphics(window)
  check_key(event_list, framecount)
  return scene.state
  

def graphics(window):
  scene.render(window, jack)

def check_key(event_list, framecount):
  keys = pygame.key.get_pressed()
  pygame.key.set_repeat(1, 100000000)
  if True: #wtf
    vec = [0, 0]
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
      vec[0]+=-1
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
      vec[0]+=1
    if keys[pygame.K_w] or keys[pygame.K_UP]:
      vec[1] +=-1
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
      vec[1] +=1
    if vec[0] or vec[1]:
        jack.walk(vec, scene)
  if key.is_keydown(event_list, "x", framecount):
    jack.use_button(scene.actors)

  if key.is_keydown(event_list, "o", framecount) and is_cheats_on:
      world_commands()

is_cheats_on = conf.conf_search("cheats")=="True"

def world_commands():
    command = input("Enter a command: ")
    if command.startswith("load "):
        scene.load_room(conf.conf_search("starting_filename"), command.split(" ")[1])

scene = world.Map((30,12), (0, tile*2), state.State.OVERWORLD)
scene.load_room(conf.conf_search("starting_filename"), conf.conf_search("starting_segname")) #revert to ma
#print(scene.tiles)

imag = pygame.image.load("Art/Flower_1.png")
imag = pygame.transform.scale(imag, (tile, tile))
imag2 = pygame.image.load("Art/jack.png")
imag2 = pygame.transform.scale(imag2, (20,18))  # lots of globals its essentialy a object or singleton because of the name space idk maybe i should make a class



jack = player.Player((100,100), "Art/jack.png", (20,28), float(conf.conf_search("speed")))
