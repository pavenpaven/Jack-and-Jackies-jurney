import pygame
import pygame_menu
import Combat.combat_unit as combat_unit
import Combat.abilities as abilities
import Combat.combat_scene as combat_scene
import Combat.jackie_abilities as ja
import Combat.jane_abilities as jane


basic = lambda x,*args: combat_unit.Entity(None, abilities.LIST_OF_MOVES+list(args), 200, 100, 3, x)

c = lambda x,f: lambda *y:f(x,*y) 

pygame.init()
pygame.display.init()
window = pygame.display.set_mode((900,600))

tile = 30


def get_info_menu(name, scene: combat_scene.Combat_scene, tick):
    text = f'No topic named {name}'
    for i in scene.players + scene.enemies:
        if name == i.name:
            text = i.info(tick)
    for i in abilities.JACK_MOVES+ja.JACKIE_MOVES+abilities.LIST_OF_MOVES+jane.JANE_MOVES:
        if name==i.NAME:
            text = i.info()
    if name in combat_scene.INFO.keys():
        text = combat_scene.INFO[name]
 

    menu = pygame_menu.Menu(name, 600, 500, theme = pygame_menu.themes.THEME_DEFAULT)
    label = menu.add.label(text, align = pygame_menu.locals.ALIGN_LEFT,max_char=70, font_size = 20, margin=(29,1), padding=0)
    menu.add.button("Back", pygame_menu.events.BACK)
    return menu

def get_move_menu(move, scene, tick, return_move_func, unit):
    move_menu = pygame_menu.Menu(move[0].NAME, 600, 500, theme = pygame_menu.themes.THEME_DEFAULT)
    possible_targets = []
    current_move = [move[0](unit, *[0 for f in range(move[0].NUM_ARGS)])]
    def ch_move(index, arg):
        print(arg)
        list(current_move[0].args)[index] = int(arg)
        args = list(current_move[0].args)
        current_move[0] = move[0](unit, *args)
        
    for f in range(move[0].NUM_ARGS):
        move_menu.add.text_input(f"arg {f+1}: ", onreturn = c(f, ch_move), default = 0)
    if move[0].TARGET_ENEMY:
        possible_targets += scene.enemies
    if move[0].TARGET_ALLY:
        possible_targets += scene.players
    if not possible_targets:
        move_menu.add.button("use", c((current_move[0], None), return_move_func))
    else:
        for f in possible_targets:
            move_menu.add.button(f.name, c((current_move[0], f), return_move_func)) #magic if you didnt know i use c for lambda x,f: lambda *y:f(x,*y) so it bakes in an argument in the function.
    move_menu.add.button("info", get_info_menu(move[0].NAME, scene, tick))
    move_menu.add.button("Back", pygame_menu.events.BACK)

    return move_menu



def player_turn_menu(unit: combat_unit.Entity, scene: combat_scene.Combat_scene, tick: int, return_move_func) -> pygame_menu.Menu:
    menu = pygame_menu.Menu(unit.name, 600, 500, theme = pygame_menu.themes.THEME_SOLARIZED)
    menu.add.label(f"Tick: {tick}", align=pygame_menu.locals.ALIGN_LEFT)
    menu.add.label("\n".join([str(i) for i in scene.players+scene.enemies]), align = pygame_menu.locals.ALIGN_LEFT, font_size=15)
    for i in unit.moves:
        move_menu =  get_move_menu(i, scene, tick, return_move_func, unit)       
        menu.add.button(f"{i[0].NAME}, {max(i[0].COOLDOWN - tick + i[1], 0)}", move_menu, font_size =15)
        
    def search_info(name):
        menu.add.menu_link(get_info_menu(name, scene, tick)).open()


    menu.add.text_input("Info: ", onreturn = search_info)

    return menu



   
if __name__ == "__main__":
    main(clock = pygame.time.Clock())
