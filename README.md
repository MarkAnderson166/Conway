# Conway

Basic implementation of Conway's game of life.  
  
*Any live cell with fewer than two live neighbours dies, as if by underpopulation.  
*Any live cell with two or three live neighbours lives on to the next generation.  
*Any live cell with more than three live neighbours dies, as if by overpopulation.  
*Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.  
  
Considering making a bigger game with tkinter just to see how far I can push it.  
This project is purely to remember tkinter syntax and create movment within the tkinter canvas.  

## result

refresh rate not good enough for what I had in mind,  
This works, but it was pointless.  

TODO:  
Crashes at the point of stagnation, might fix it one day.  
Some dead cells aren't deleting properly - didn't find why.  

# Conway 2  

Same as above, but using pygame library instead of tkinter.
Looks cool, countMates() needs to pass around HUGE data to work. needs refactor  
  
TODO:  
add seperate global [][] to avoid passing around list of objects  
menu buttons  
