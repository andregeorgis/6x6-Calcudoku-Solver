# 6x6-Calcudoku-Solver

**A python program that can solve 6x6 Calcudoku grids**



[TOC]

## Calcudoku/Sudoku Rules
**Add later if bothered ¯\\\_(ツ)\_/¯**

## Input
The program takes standard input to initialise the grid and cages (see input.txt or storage.txt for examples :stuck_out_tongue:)

Scanning through each row from top to bottom, each new cage is given a new index starting from 0 (top-left cage is given index 0 then next cage in first rowis given index 1 and so on). The first 6 lines of input are the 6 rows of the grid, where each cell is space-separated and indicated by its cage index. The 7th line of input are the cage operations in the order corresponding to their index (and are also space-separated); i.e. the first operation belongs to cage with index 0, the second to cage with index 1 and so on.

Most grids were found using the website [here](<https://newdoku.com/>) since it provided both varying difficulties and solutions for each grid.


## Summary of Strategy
The python program solves each grid by solving for all possibilities of each cage, then filtering through these possibilities. We first collect the cages from input and find all possible permutation of numbers between 1 and 6 that can solve this cage. After this we start filtering the possibilities by checking if the numbers inside the cage alone abide by sudoku rules (if a cage has some cells in a common row or column, do these numbers break sudoku rules?). We also add cages with no operator to the grid instantly and remove them from the program.

We then start the first stage of solving which is filtering cage possibilities against the initial grid (now checking numbers in the cage and in each row and column that the cage is part of). If there ever is only one solution left for a cage, it is added to the grid and this process is repeated with the new grid. This repeats until either the grid has been solved, or we have hit an "equilibrium" - (or we can get a situation where a cage ends up with 0 solutions which means the grid is unsolvable).

An "equilibrium" is a term I have used for whenever a grid has multiple cages each with more than 1 solution (i.e. we have a bunch of cages with a bunch of solutions each and the program currently cannot decide which is the right one). So from here the program begins to "guess" the right solution. The program picks a cage and iterates through each of its possibilities, each time forcing the cage to have that possibility as its only solution. So it adds this "solution" to the grid and then repeats the process before. If one of the other cages ends up with 0 solutions then we have "guessed" wrong and iterate to the next possibility. If the grid gets solved then yay! Sometimes, we hit another "equilibrium" so we need to grab another cage and start guessing with that one. If the grid is solvable this program should exit before this process "ends" - hence if it does end then we can conclude that the grid was unsolvable.

