import random
import Combat.combat_unit as combat_unit
import Combat.abilities as abilities
import Combat.jackie_abilities as ja
import Combat.jane_abilities as jane

print()
print("***  type /help for help  ***")
print()

basic = lambda x,*args: combat_unit.Entity(None, abilities.LIST_OF_MOVES+list(args), 200, 100, 3, x)
def vasic(name, *args, **kwargs):
    b = abilities.LIST_OF_MOVES + list(args)
    if "hp" in kwargs:
        hp = kwargs["hp"]
    else:
        hp = 200
    for i in kwargs:
        if i in list(map(lambda x:x.NAME, b)):
            b.remove(list(filter(lambda x:x.NAME == i, b))[0])
    return combat_unit.Entity(None, b, hp, 100, 3, name)


INFO = {"heal": "heal is a status effect wich lasts n ticks and heals 1 hp every tick also stacks","stun": "time for stun", "bullet": "Bullets Can have diffrent elemental effects depending on which type of bullet.", "curse": "curse is a status effect that stacks and for every curse deals 1 damage every 3 ticks and gives 10x strength wich is a 10x% increese in non-true damage aka damage not from status effects"}

class Combat_scene:
    def __init__(self, players, enemies):
        self.players = players
        self.enemies = enemies

    def simulate_tick(self, tick: int, player_turn_func):
        list_of_entities = self.players + self.enemies
        random.shuffle(list_of_entities)
        for i in list_of_entities:
            i.handle_status_effects(tick)
            move = i.active_move[0]
            target = i.active_move[1]
            activated_tick = i.active_move[2]
            if move == None:
                self.turn(i, tick, player_turn_func)
            else:
                if tick - activated_tick == move.STARTUP_TIME:
                    move.fundamental_ontime_func(i, target, tick)
                if tick - activated_tick >= move.STARTUP_TIME + move.GLOBAL_COOLDOWN:
                    self.turn(i, tick, player_turn_func)
          
        for n,i in enumerate(self.players):
          if i.health<1:
            self.players.pop(n)
        for n,i in enumerate(self.enemies):
          if i.health<1:
            self.enemies.pop(n)

        if self.players == []:
          print("you loose")
          return 0
        if self.enemies == []:
          print("you win")
          return 0
        return 1
        
        
    
    def player_turn(self, unit:combat_unit.Entity, tick: int):
        print()
        print(f"Your turn {unit}")
        print(f"Tick is {tick}")
        print("Allies: \n  " + '\n  '.join(list(map(str, self.players))))
        print("Enemies: \n  " + '\n  '.join(list(map(str, self.enemies))))
        print([(i[0].NAME, max(i[0].COOLDOWN - tick + i[1], 0)) for i in unit.moves])
      
        while True:
          choice = input(": ")
          if choice.startswith("/"):
            self.command(choice[1:len(choice)], tick)
          else:
            if choice in list(map(lambda x:x[0].NAME, unit.moves)):
                break
            else:
                print(f"{choice} not in moveset")
          
        move = list(filter(lambda x:x[0].NAME==choice, unit.moves))[0][0]
        args = []
        for i in range(move.NUM_ARGS):
            args.append(int(input(f"Args {i}: ")))
        x = self.enemies[0]
        if move.TARGET_ENEMY or move.TARGET_ALLY:
            while True:
              name = input()
              u = list(map(lambda x:list(map(lambda y:y.name, x[0])) if x[1] else [], [(self.enemies, move.TARGET_ENEMY), (self.players, move.TARGET_ALLY)]))
              if name in u[0] + u[1]:
                u = list(map(lambda x:list(map(lambda y:(y, y.name), x[0])) if x[1] else [], [(self.enemies, move.TARGET_ENEMY), (self.players, move.TARGET_ALLY)]))
                u = u[0] + u[1]
                x = list(filter(lambda x:x[1]==name, u))[0][0]
                break
        
        return (move(unit, *args), x)

    
    def enemy_turn(self, unit:combat_unit.Entity, tick: int):
        while True:
            move = random.choice(unit.moves)[0](unit, (1))
            x = list(filter(lambda x:x[1][0] == move.__class__, enumerate(unit.moves)))[0]
            if tick - x[1][1] >= move.COOLDOWN:
              print(f"{unit} used {move} on tick {tick}")  
              return (move, random.choice(self.players))


    def turn(self, unit: combat_unit.Entity, tick: int, player_turn_func):
        if unit in self.players:
            move_target = player_turn_func(unit, self, tick)
        else:
            move_target = self.enemy_turn(unit, tick)
        if move_target[0].TARGET_ENEMY or move_target[0].TARGET_ALLY:
            unit.active_move = (move_target[0], move_target[1], tick)
            list(filter(lambda x:x, enumerate(unit.moves)))
        else:
            unit.active_move = (move_target[0], None, tick)
        a = unit.get_move_index(move_target[0].__class__)
        unit.moves[a] = (unit.moves[a][0], tick)

    def command(self, choice, tick):
      if choice.startswith("info"):
        if not len(choice.split(" ")) > 1:
          print("Expected an argument to info")
        else:
          name = " ".join(choice.split(" ")[1:len(choice)])
          for i in self.players + self.enemies:
            if name == i.name:
              print(i.info(tick))
          for i in abilities.JACK_MOVES+ja.JACKIE_MOVES+abilities.LIST_OF_MOVES+jane.JANE_MOVES:
            if name==i.NAME:
              print(i.info())
          if name in INFO.keys():
            print(INFO[name])
      
      if choice.startswith("help"):
        print("Right now it is your turn as one of the characters. You see 'your turn *** hp: **' with ammo if it's jack. You see the current tick, your allies thier hp and thier current move and when they initiated that move. you also se the enemies. And a list of moves with a number symbolising thier cooldown in ticks. type /info **** to get information of a move a ally or occationally a consept. And type the name of a move then enter followed by either a number symbolizing the index of the enemy you want to attack starting from 0 so the first one would be 0 the secound would be 1. If you used a move that needs an argument passed to it then you will se a 'Arg 0' then just type the argument you want to pass to it for exampe wait will wait n tick. A document for the combat is found here https://docs.google.com/document/d/1x-0Ejy4nsjPT7E-BCkBu8EH6SJNT3h1H-qViem3JEG0/edit?usp=sharing")

if __name__ == "__main__":
    Combat_scene([basic("Jack",*abilities.JACK_MOVES), basic("Jackie", *ja.JACKIE_MOVES), vasic("Jane", *jane.JANE_MOVES, kick=False)], [vasic(f"Enemy {i}", hp=400) for i in range(4)])
