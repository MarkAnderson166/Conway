import pygame as pg
from random import *

import numpy as np
pg.mixer.init(size=32)


HEIGHT = 800
RESOLUTION = 100
TILE_SIZE = int(HEIGHT/RESOLUTION)
FPS = 60

global MUSICTEST
global MUSICTEST2
MUSICTEST = 0
MUSICTEST2 = 0

global GRID_FUTURE
global GRID_CURRENT
global COLOR

GRID_CURRENT = [ [0]*RESOLUTION for i in range(RESOLUTION)]
GRID_FUTURE =  [ [0]*RESOLUTION for i in range(RESOLUTION)]
COLOR = randint(0,2)

class Helpers():

  def pixelToGridpos(pixel):
    return int((pixel/HEIGHT)*RESOLUTION)

  def gridposToPixel(gridpos):
    return int((HEIGHT/RESOLUTION)*gridpos)+(TILE_SIZE/2)

  def countMates(x,y):
    count = 0
    for i in range(x-1, x+2, 1):
      for j in range(y-1, y+2, 1):
        if i == x and j == y:
          continue
        try:
          if GRID_CURRENT[i][j] == 1:
            count += 1
        except IndexError:
              continue
    return count


  def soundTest(freq):
    global MUSICTEST, MUSICTEST2
    MUSICTEST = 60
    if MUSICTEST2 % 4 == 0:
      freq = 523
      print('C!')
    MUSICTEST2 += 1
    pg.mixer.Sound(np.sin(2 * np.pi * np.arange(10000) * freq / 44100).astype(np.float32)).play(0)



class Tile(pg.sprite.Sprite):

  def __init__(self,xCor,yCor):
    self.currentState = 0
    self.col = 0
    self.xCor = xCor
    self.yCor = yCor
    pg.sprite.Sprite.__init__(self)
    self.image = pg.Surface((TILE_SIZE*.9, TILE_SIZE*.9))
    self.rect = self.image.get_rect()
    self.rect.center = (Helpers.gridposToPixel(xCor),Helpers.gridposToPixel(yCor))
 
  def update(self):
    global GRID_FUTURE
    global COLOR
    
    if   COLOR == 0:
      self.image.fill((self.col,0,0))
    elif COLOR == 1:
      self.image.fill((0,self.col,0))
    elif COLOR == 2:
      self.image.fill((0,0,self.col))
    elif COLOR == 3:
      self.image.fill((self.col,self.col,0))
    elif COLOR == 4:
      self.image.fill((0,self.col,self.col))
    else:
      self.image.fill((self.col,0,self.col))
    
    if self.col > 5 and self.currentState == 0 : self.col = self.col*.8

    # conways game logic here
    mates = Helpers.countMates(self.xCor,self.yCor)
    if self.currentState == 0:
      if mates == 3:
        self.revive()
    else:
      if mates < 2 or mates > 3:
        GRID_FUTURE[self.xCor][self.yCor] = 0

  def revive(self):
    global GRID_FUTURE
    GRID_FUTURE[self.xCor][self.yCor] = 1
    self.col = 200

  def getPosX(self):
    return self.xCor
  def getPosY(self):
    return self.yCor
  def getCurrentState(self):
    return self.currentState
  def setNewState(self):
    self.currentState = GRID_CURRENT[self.xCor][self.yCor]



class Conway:

  def __init__(self):
    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((HEIGHT*1.2,HEIGHT))

    pg.display.set_caption("Conway's Py Game")
    clock = pg.time.Clock()

    all_sprites = pg.sprite.Group()
    all_tiles = pg.sprite.Group()
    for i in range (0,RESOLUTION,1):
      for j in range(0,RESOLUTION,1):
        tile = Tile(i,j)
        all_tiles.add(tile)
    all_sprites.add(all_tiles)

  
    # main loop

    running = True
    while running:
      clock.tick(FPS)
    
      for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN:
          mouseX = Helpers.pixelToGridpos(pg.mouse.get_pos()[0])
          mouseY = Helpers.pixelToGridpos(pg.mouse.get_pos()[1])
          if pg.mouse.get_pos()[0] < HEIGHT:
            for tile in all_tiles:
              if (mouseX == tile.getPosX() and mouseY == tile.getPosY()):
                tile.revive()
                print('Clicked tile has: '+str(Helpers.countMates(tile.getPosX(),tile.getPosY()))+' mates')
          elif pg.mouse.get_pos()[1] < HEIGHT/2:
            print('click in menu area - spray')
            for tile in all_tiles:
              if (randint(0,1)): tile.revive()
          else:
            print('click in menu area - COLORS!')
            global COLOR
            COLOR = randint(0,6)
            cMajor = [261,293,329,349,392,440,493,523,587,659,698,784,880,987,1046]
            Helpers.soundTest(choice(cMajor))



      #Update
      all_sprites.update()
      
      #update alive/dead state -- MUST BE SEPERATE LOOP
      global GRID_CURRENT
      GRID_CURRENT = [row[:] for row in GRID_FUTURE]  
      for tile in all_tiles:  tile.setNewState()

        # as long as notes play within 60 seconds of each other,
        # every 4th note will be a C.
      global MUSICTEST
      global MUSICTEST2
      if MUSICTEST > 0:
        MUSICTEST -= 1
      else:
        MUSICTEST2 = 0

      keys = pg.key.get_pressed()

      # Render
      screen.fill((0,0,0))
      all_sprites.draw(screen)
      pg.display.flip()


Conway()
pg.quit()
