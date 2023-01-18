from dataclasses import dataclass
import os
import pickle
import Combat.abilities as abilities

@dataclass
class Entity_type:
  texture: str #filename
  moves: [abilities.Default_move]
  max_health: int
  max_mana: int
  default_armor: int
  #this is true beuty jag kan inte stava

FILENAME = "Combat/entity_data.txt"
# i know global shit but it's so frestande
with open(FILENAME, "rb") as fil:
  if not os.stat(FILENAME).st_size == 0:
    try:
      entity_data = pickle.load(fil)
    except:
      raise Exception("File Combat/entity_data.txt is corrupt!")
  else:
    entity_data = dict()
