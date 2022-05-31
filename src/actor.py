import pygame

tile=30

def load_sprites(segname, filename):
  with open(filename, "r") as fil:
    txt=fil.read()
  
  txt = txt.split(";\n")
  txt = list(map(lambda x:x.split(":"), txt))

  for i in txt:
    print(segname, i[0])
    
  seg = list(filter(lambda x:segname==x[0], txt))
  if not seg==[]:
    seg = seg[0][1].split("\n")
    seg = list(map(lambda x:x.split("-"), seg))
    seg.pop(0)
    for n,i in enumerate(seg):
      x = i[1].split(",")
      seg[n][1] =  (float(x[0])*tile, float(x[1])*tile)

  
    out=[]
    for i in seg:
      for f in SPRITE_CLASSES:
        print(i, f.name)
        if i[0]==f.name:
          if len(i)>2:
            out.append(f(i[1],extra=i[2]))
          else:
            print(f,i[1])
            out.append(f(i[1]))
  else:
    out = []

  return out
  

def re(filename, size):
  x=pygame.image.load(filename)
  return pygame.transform.scale(x, size)

class Sprite:
  texture=re("Art/unknown.png", (1,1))
  size=(1,1)
  collision=False
  def __init__(self, pos,extra=""):
    self.pos = pos
  def render(self, scene):
    scene.blit(self.texture, self.pos)

class Test(Sprite):
  texture=re("Art/Flower_1.png", (20,28))
  name="test"
  size=(1,1)
  collision = True

SPRITE_CLASSES=[Test]