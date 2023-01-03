import pygame as pg
from random import *

WIDTH = 1000
HEIGHT = 800
RESOLUTION = 20
TILE_SIZE = int(HEIGHT/RESOLUTION)
FPS = 60

class Helpers():

    def pixelToGridpos(pixel):
      return int((pixel/HEIGHT)*RESOLUTION)

    def gridposToPixel(gridpos):
      return int((HEIGHT/RESOLUTION)*gridpos)+(TILE_SIZE/2)

    def countMates(x,y,all_tiles):
      count = 0
      for tile in all_tiles:
        mateX = tile.getPosX()
        mateY = tile.getPosY()

        if mateX == x or mateX == x+1 or mateX == x-1:
          if mateY == y or mateY == y+1 or mateY == y-1:
            if x == mateX and y == mateY:
              #print('dont count yourself')
              pass
            else:
              count += tile.getCurrentState()

      #if count == 4: print(str(x)+' ,'+str(y)+' has '+str(count)+' mates')

      return count




class Tile(pg.sprite.Sprite):

  def __init__(self,xCor,yCor):
    self.currentState = 0
    self.futureState = 0
    self.green = 0
    self.xCor = xCor
    self.yCor = yCor
    pg.sprite.Sprite.__init__(self)
    self.image = pg.Surface((TILE_SIZE*.9, TILE_SIZE*.9))
    self.rect = self.image.get_rect()
    self.rect.center = (Helpers.gridposToPixel(xCor),Helpers.gridposToPixel(yCor))
 
  def update(self,all_tiles):
    self.image.fill((0,self.green,0))
    
    if self.green > 5 and self.currentState == 0 : self.green -= 5

    # conways game logic here
    mates = Helpers.countMates(self.xCor,self.yCor,all_tiles)
    if self.currentState == 0:
      if mates == 3:
        self.revive()
    else:
      if mates < 2 or mates > 3:
        self.futureState = 0


  def revive(self):
    self.futureState = 1
    self.green = 160

  def getPosX(self):
    return self.xCor
  def getPosY(self):
    return self.yCor
  def getCurrentState(self):
    return self.currentState
  def setNewState(self):
    self.currentState = self.futureState





class Conway:

  def __init__(self):
    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((WIDTH,HEIGHT))

    pg.display.set_caption("Conway's Py Game")
    clock = pg.time.Clock()

    #grid = [ [0]*RESOLUTION for i in range(RESOLUTION)]

    all_sprites = pg.sprite.Group()
    all_tiles = pg.sprite.Group()

    for i in range (0,RESOLUTION,1):
      for j in range(0,RESOLUTION,1):
        tile = Tile(i,j)
        all_tiles.add(tile)

  
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
                print('Clicked tile has: '+str(Helpers.countMates(tile.getPosX(),tile.getPosY(),all_tiles))+' mates')
          else:
            #print('click in menu area')
            for tile in all_tiles:
              if (randint(0,1)): tile.revive()


      all_sprites.add(all_tiles)

      #Update
      all_sprites.update(all_tiles)
      #update alive/dead state -- MUST BE SEPERATE LOOP
      for tile in all_tiles:  tile.setNewState()

      keys = pg.key.get_pressed()

      # Render
      screen.fill((0,0,0))
      all_sprites.draw(screen)
      pg.display.flip()


Conway()
pg.quit()

