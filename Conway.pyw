import tkinter as tk
import random

WIDTH = 600
HEIGHT = WIDTH+50
SIZE = int(WIDTH/20)

root = tk.Tk()
root.title("Conways game of life")
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

global grid, newGrid, running
running = 0
grid = [ [0]*SIZE for i in range(SIZE)]
  

# ------------------------------------------------- #
# -------- GUI 
# ------------------------------------------------- # 

def makeGUI():
      # buttons
  buttonReset=tk.Button(root, bg='aqua', text="Start", width=8, height=1, command=lambda:startStop(1))
  buttonReset.place(x=(WIDTH/9)*5, y=HEIGHT-35)
  buttonSolve=tk.Button(root, bg='green', text="Stop", width=8, height=1, command=lambda:startStop(0))
  buttonSolve.place(x=(WIDTH/9)*6, y=HEIGHT-35)
  buttonDLC=tk.Button(root, bg='yellow', text="Spray", width=8, height=1, command=lambda:spray())
  buttonDLC.place(x=(WIDTH/9)*7, y=HEIGHT-35)
  buttonExit=tk.Button(root, bg='red', text="Exit", width=8, height=1, command=root.destroy)
  buttonExit.place(x=(WIDTH/9)*8, y=HEIGHT-35)

    # draw static text
  canvas.create_text(10,HEIGHT-15, anchor="nw",font="Times 11",text= "Conways Game of Life")

    # draw grid lines
  for i in range (0, WIDTH+1, 20):
    canvas.create_line(i, 0, i, WIDTH)
    canvas.create_line(0, i, WIDTH, i )
  canvas.create_line(2, 2, 2, WIDTH)
  canvas.create_line(2, 2, WIDTH, 2 )


# ------------------------------------------------- #
# --------  'helper'  functions
# ------------------------------------------------- # 

def drawBox(r,c,):
  root.update()
  canvas.create_rectangle(1+c*20, 1+r*20, 20+c*20, 20+r*20, fill='grey', tag="box"+str(r)+str(c))
  root.update()

  # -- buggy - tkinter is bad at this (threading thing)
def startStop(x):
  global running
  running = x
  if x:
    print('resuming')
    loopConway()
  else:
    print('paused with '+str(sum(sum(grid,[])))+' nodes alive')

  # -- mouse
def addBox(event):
  newGrid[int(event.y/20)][int(event.x/20)] = 1
  grid[int(event.y/20)][int(event.x/20)] = 1
  drawBox(int(event.y/20),int(event.x/20))
canvas.bind('<Button-1>', addBox)

def spray():
  if running == 0:
    print('adding live nodes')
    for r in range (SIZE):
      for c in range (SIZE):
        grid[r][c] = random.randint(0,1)
        if grid[r][c]==1:drawBox(r,c)
  else:
    print('pause before spraying')

# ------------------------------------------------- #
# -------- Logic 
# ------------------------------------------------- # 


def gameLogic():
  global grid, newGrid

  newGrid = [ [0]*SIZE for i in range(SIZE) ]

  for r in range (SIZE):
    for c in range (SIZE):

      # - count mates
      count = 0
      for i in range(r-1, r+2, 1):
        for j in range(c-1, c+2, 1):
          if i == r and j == c:
            continue
          try:
            if grid[i][j] == 1:
              count += 1
          except IndexError:
                continue

      # - apply logic after count
      if grid[r][c] == 1 and ( count < 2 or count > 3 ):
        newGrid[r][c] = 0
        canvas.delete("box"+str(r)+str(c))
      if grid[r][c] == 1 and ( count == 2 or count == 3 ):
        newGrid[r][c] = 1

      if grid[r][c] == 0:
        if count == 3:
          newGrid[r][c] = 1
          drawBox(r,c)
        else:
          newGrid[r][c] = 0
          canvas.delete("box"+str(r)+str(c))


  grid = [row[:] for row in newGrid]  


# ------------------------------------------------- #
# -------- Run 
# ------------------------------------------------- # 


makeGUI()
spray()

def loopConway():
  global running
  while( running ):
    root.after(50,gameLogic())


loopConway()
root.mainloop()