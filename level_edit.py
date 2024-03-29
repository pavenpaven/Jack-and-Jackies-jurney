#!/usr/bin/env python3
import sys
import pygame
import time
import src.tile_types as tile_types
import src.world as world
import src.music as music
MUSIC = music.Music("Level/theme_info")

pygame.font.init()

tile=30
map_size = (30, 12)

def parse_args(args, length):
    if length == 1:
        print("few args")
        exit()
    if args[1][0] == "-":
        parse_mode(args)
    else:
        if length < 3:
            print("too few args")
        open_level_edit(args[1], args[2])

def open_level_edit(filename, segname, is_loading_zone_mode = False,lz_segname=""):
    def check_key():
        quit = False
        for event in  pygame.event.get():
            if event.type == pygame.KEYDOWN:
                vec = [0, 0]
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    last_pressed=framecount
                    vec[0]+=-1
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    last_pressed=framecount
                    vec[0]+=1
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    last_pressed=framecount
                    vec[1] +=-1
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    vec[1] += 1
                if not is_loading_zone_mode:
                    if event.key == pygame.K_x:
                        curser.change_tile(1)
                    if event.key == pygame.K_z:
                        curser.change_tile(-1)
                else:
                    if event.key == pygame.K_x:
                        curser.place_loading_zone()
                n=0
                for j in tile_types.Tile_type.types:
                    if event.key == j.key:
                        scene.tiles[curser.tile_pos[1]][curser.tile_pos[0]] = n
                    n+=1
                curser.tile_pos = (vec[0]+curser.tile_pos[0], vec[1]+curser.tile_pos[1])
                curser.pos = (curser.tile_pos[0]*tile, curser.tile_pos[1]*tile)
                last_pressed=framecount
            if event.type == pygame.QUIT:
                quit = True
        return quit

    def graphics():
        window.fill((0,0,0))
        scene.render(window, curser, MUSIC)
        window.blit(font.render(str(tuple(i/tile for i in curser.pos)), True, (255,255,0)), (10,10))
        pygame.display.update()
            
    class Curser:
        def __init__(self, pos, texture):
            tex = pygame.image.load(texture)
            self.texture = pygame.transform.scale(tex ,(tile, tile))
            self.tile_pos = pos
            self.pos = (pos[0]*tile, pos[1]*tile)
            self.loading_zone_state = 0
        def change_tile(self, ammount):
            
            if scene.tiles[self.tile_pos[1]][self.tile_pos[0]] != len(tile_types.Tile_type.types) - 1:
                scene.tiles[self.tile_pos[1]][self.tile_pos[0]]+=ammount
            else:
                scene.tiles[self.tile_pos[1]][self.tile_pos[0]] = 0
        def place_loading_zone(self, segname):
            pass


    curser = Curser((1,1), "Art/curser.png")
    scene = world.Map((30,12), (0, tile*2), 1) #wtf state 1 lol      
    scene.load_room(filename, segname, MUSIC)
    window = pygame.display.set_mode((900,600))
    pygame.font.init()
    #print(pygame.font.get_fonts())
    font = pygame.font.SysFont("roboto", 30)
    running = True
    clock = pygame.time.Clock()
    framecount = 0
    last_pressed = 0
    while running:
        clock.tick(30)
        framecount+=1
        if framecount % 100 == 0:
            print(clock.get_fps())
        graphics()
        quit=check_key()
        if quit:
            scene.save(filename, segname)
            pygame.quit()
            running=False

def parse_mode(args):
    if args[1] == "-c":
        creat_segment(args[2], args[3], args[4])
    if args[1] == "-list":
        list_segnames(args[2])
    if args[1] == "-l":
        open_level_edit(args[3], args[4], is_loading_zone_mode = True, lz_segname=args[2])

def creat_segment(character, filename, segname):
    
    tiles = ""
    for i in range(map_size[1]):
        for f in range(map_size[0]):
            tiles += character
        tiles += "\n"

    result = segname + "#" + tiles + "#" + "?"

    with open(filename, "a") as fil:
        fil.write(result)

def merge_file():
    pass

def list_segnames(filename):
    with open(filename, "r") as fil:
        tex = fil.read()
    
    for i in tex.split("?"):
        print(i.split("#")[0])

def main():
	parse_args(sys.argv, len(sys.argv))

main()
