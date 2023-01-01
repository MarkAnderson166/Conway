import tkinter as tk
import random

HEIGHT = 850
WIDTH = 800
SIZE = int(WIDTH/20)


root = tk.Tk()
root.title("Conways game of life")
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()


global grid, newGrid, running
running = 1
grid = [ [0]*SIZE for i in range(SIZE)]

#random 1's
for r in range (SIZE):
  for c in range (SIZE):
    grid[r][c] = random.randint(0,1)
  

# ------------------------------------------------- #
# -------- GUI and Text functions start here ------ #
# ------------------------------------------------- # 


def drawBox(r,c,color):
  root.update()
  canvas.delete("box"+str(r)+str(c))
  if color != 'dead':
    canvas.create_rectangle(1+c*20, 1+r*20, 20+c*20, 20+r*20, fill=color, tag="box"+str(r)+str(c))

  root.update()


def drawString(textMes):
    # Draws the little messages in the bottom left
    # ie. 'I'm afraid I can't do that Dave'
  canvas.delete("drawString")
  root.update()
  canvas.create_text(10,HEIGHT-25, tag="drawString",
    anchor="sw", font="Times 11", text=textMes)
  root.update()


def dlcJoke(jokeNumber):
  jokes =["There isn't really any DLC for this", 
          "How could this possibly have DLC?", 
          "If only I could monetise this", 
          "this button is never going to do anything",
          "this button is only a joke",
          "Please insert disc 21",
          "DLC requires Voodoo 2 3DFX",
          "I'm afraid I can't do that Dave", 
          "DLC requires Soundblaster 2 or greater" ]
  drawString(jokes[random.randint(0,len(jokes)-1)])

def startStop(x):
  global running
  running = x


#def step():
#  root.after(1,canvas.delete("box"))
#  for r in range (SIZE):
#    for c in range (SIZE):
#      drawBox(r,c)
#  gameLogic()


def makeGUI():
      # buttons
  buttonReset=tk.Button(root, bg='aqua', text="Start", width=8, height=1, command=lambda:startStop(1))
  buttonReset.place(x=(WIDTH/9)*5, y=HEIGHT-35)
  buttonSolve=tk.Button(root, bg='green', text="Stop", width=8, height=1, command=lambda:startStop(0))
  buttonSolve.place(x=(WIDTH/9)*6, y=HEIGHT-35)
  buttonDLC=tk.Button(root, bg='yellow', text="$ DLC $", width=8, height=1, command=lambda:dlcJoke(1))
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
# --------            functions start here ------ #
# ------------------------------------------------- # 

def gameLogic():
  global grid, newGrid

  newGrid = [ [0]*SIZE for i in range(SIZE) ]

  for r in range (SIZE):
    for c in range (SIZE):

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

      if grid[r][c] == 1 and count < 2:
        newGrid[r][c] = 0
        drawBox(r,c,"dead")
      if grid[r][c] == 1 and count == 2:
        newGrid[r][c] = 1
        drawBox(r,c,"orange")
      if grid[r][c] == 1 and count == 3:
        newGrid[r][c] = 1
        drawBox(r,c,"red")
      if grid[r][c] == 1 and count > 3:
        newGrid[r][c] = 0
        drawBox(r,c,"dead")
      if grid[r][c] == 0 and count == 3:
        newGrid[r][c] = 1
        drawBox(r,c,"yellow")
        

  grid = [row[:] for row in newGrid]  


# ------------------------------------------------- # 




def addBox(event):
  newGrid[int(event.y/20)][int(event.x/20)] = 1
  drawBox(int(event.y/20),int(event.x/20),"black")
canvas.bind('<Button-1>', addBox)

makeGUI()

while(1):

  gameLogic()
  


root.mainloop()