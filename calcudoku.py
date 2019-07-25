import sys

## Class for the cages in the grid
class Cage:
    def __init__(self, op_and_num):
        self.op_and_num = op_and_num ## Cage operation and number
        self.size = 0 ## Number of cells
        self.cells = [] ## x-y of cells
        self.op = None
        self.num = None
        self.possibilities = [] ## Initial choices
        ## Initial choices are restricted by problematic cells and initial grid
        self.problematic_cells = [] ## Cells in common row or column
        self.good_possibilities = [] ## Choices after restrictions
        ## Choices are initial choices with new restrictions (new grid values)

    ## Introduce a new cell to cage
    def add_cell(self, cell):
        self.cells.append(cell)
        self.size += 1

    '''
    Function that find which groups of cells are problematic
    Added to self.problematic_cells in a specific format:
    ["R" + str(n), CX...] where CX is each column number and n is row number
    ["C" + str(n), RX...] where RX is each row number and n is column number
    '''
    def find_problematic_cells(self):
        rows = ["", "", "", "", "", ""]
        cols = ["", "", "", "", "", ""]
        cells = self.cells
        length = len(cells)


        ## If cell exists in a row then record its column (and vise versa)
        for i in range(length):
            rows[cells[i][0]] += str(i)
            cols[cells[i][1]] += str(i)

        ## If more than one cell in a row; classify it as problematic
        for string in rows:
            if len(string) > 1:
                prob = list(string)
                for num in range(len(prob)):
                    prob[num] = int(prob[num])

                self.problematic_cells.append(prob)

        ## If more than one cell in a column; classify it as problematic
        for string in cols:
            if len(string) > 1:
                prob = list(string)
                for num in range(len(prob)):
                    prob[num] = int(prob[num])

                self.problematic_cells.append(prob)

    ## Check if cage operation and number is valid; and cage size accordingly
    def check_cage(self):
        ## Find problematic cells
        self.find_problematic_cells()

        ## Check if there is no operator
        no_operation = True if len(self.op_and_num) == 1 else False

        ## If there is no operator, check that there is only one cell
        if no_operation:
            self.op = None
            self.num = int(self.op_and_num)
            if self.size != 1:
                return False

            return True


        self.op = self.op_and_num[-1]
        self.num = int(self.op_and_num[:-1])

        ## If division or subtraction; check for two cells
        if (self.op == "/" or self.op == "-") and self.size != 2:
            return False

        ## Otherwise check for 1 or more cells (addition and multiplication)
        if self.size < 1:
            return False

        return True

    ## Add an initial choice to self.possibilities
    def add_possibility(self, poss):
        self.possibilities.append(poss)

    ## Add a choice to self.good_possibilities
    def add_good_possibility(self, poss):
        self.good_possibilities.append(poss)

    ## Returns number of initial possibilities
    def num_of_possibilities(self):
        return len(self.possibilities)

    ## Returns number of good possibilities
    def num_of_good_possibilities(self):
        return len(self.good_possibilities)


'''
====================================================
FUNCTIONS FOR PROCESSING STDIN AND INITIALISING GRID
====================================================
'''

## Gets the format for each cage
def get_grid_format():
    ## Get format from stdin
    grid = []
    for i in range(6):
        line = input().split()
        grid.append(line)

    ## Return format
    return grid

## Gets and initialises all Cage objects
def get_cages(grid_format):
    ## Get op_and_num from stdin
    cages = input().split()
    for i in range(len(cages)):
        cages[i] = Cage(cages[i])

    ## Use grid_format to initialise cage cells and size
    for j in range(6):
        for i in range(6):
            index = int(grid_format[i][j])
            cages[index].add_cell((i, j))


    ## Return list of all cages
    return cages

## Checks that each of the cages have a valid operator
def check_cages(cages):
    ## Calls Cage instance method check_cage()
    for cage in cages:
        condition = cage.check_cage()

        ## If a cage is invalid; exit
        if not condition:
            print("No solution.")
            sys.exit()

## Initialise grid and fill in all "no operator" cages
def initialise_grid(cages):
    ## Make grid
    grid = []
    for i in range(6):
        grid.append([0, 0, 0, 0, 0, 0])

    ## Fill in all "no operator cages" and remove them from the cages list
    for i in range(len(cages) - 1, -1, -1):
        cage = cages[i]
        if cage.size == 1:
            x, y = cage.cells[0]
            grid[x][y] = cage.num
            cages.remove(cage)

    return grid


'''
====================================================
FUNCTIONS FOR DETERMINING INITIAL CAGE POSSIBILITIES
====================================================
'''

'''
Each function used to find cell possibilities uses a list of numbers between
1 and 6. Each permutation is tested using the appropriate operation and number.
Each permutation is generated by treating the list like a base 7 number - i.e.
increment the first digit by 1 and if it gets bigger than 6 then increment the
next digit by 1 and set the first digit back to 1. The size of the list is equal
to the size of the cage (number of cells).

We then check if these possibilities are valid in the initial grid. We first
find problematic cells - cells in a cage that share the same row or column. We
check the values in these cells and the other values in the same row or grid. If
invalid we remove the possibility.
'''

## Find all possibilities for addition cage
def find_add_possibilities(cage):
    ## Use list of numbers to represent cell values
    ls = [1] * cage.size

    while True:
        ## Check sum; add possibility if valid
        if sum(ls) == cage.num:
            poss = ls[:]
            cage.add_possibility(poss)

        ## Incrementing through permutations
        ls[0] += 1

        for i in range(cage.size):
            if ls[i] > 6:
                if i == cage.size - 1:
                    return None

                ls[i] = 1
                ls[i + 1] += 1

## Find all possibilities for subtraction cage
def find_sub_possibilities(cage):
    ## Use list of numbers to represent cell values
    ls = [1] * cage.size

    while True:
        ## Check subtraction; add possibility if valid
        if ls[0] - ls[1] == cage.num:
            poss = ls[:]
            cage.add_possibility(poss)
        elif ls[1] - ls[0] == cage.num:
            poss = ls[:]
            cage.add_possibility(poss)

        ## Incrementing through permutations
        ls[0] += 1

        for i in range(cage.size):
            if ls[i] > 6:
                if i == cage.size - 1:
                    return None

                ls[i] = 1
                ls[i + 1] += 1

## Find all possibilities for multiplication cage
def find_mult_possibilities(cage):
    ## Use list of numbers to represent cell values
    ls = [1] * cage.size

    while True:
        ## Check product; add possibility if valid
        num = 1
        for i in ls:
            num *= i

        if num == cage.num:
            poss = ls[:]
            cage.add_possibility(poss)

        ## Incrementing through permutations
        ls[0] += 1

        for i in range(cage.size):
            if ls[i] > 6:
                if i == cage.size - 1:
                    return None

                ls[i] = 1
                ls[i + 1] += 1

## Find all possibilities for division cage
def find_div_possibilities(cage):
    ## Use list of numbers to represent cell values
    ls = [1] * cage.size

    while True:
        ## Check division; add possibility if valid
        if cage.num * ls[0] == ls[1]:
            poss = ls[:]
            cage.add_possibility(poss)
        elif cage.num * ls[1] == ls[0]:
            poss = ls[:]
            cage.add_possibility(poss)

        ## Incrementing through permutations
        ls[0] += 1

        for i in range(cage.size):
            if ls[i] > 6:
                if i == cage.size - 1:
                    return None

                ls[i] = 1
                ls[i + 1] += 1

## Check if the initial possibility abides by sudoku rules in its own cage
def check_initial_possibilities(cage, grid):
    filtered_possibilities = []
    for poss in cage.possibilities:
        skip = False

        ## Check the choice against the problematic cells in the cage
        for prob in cage.problematic_cells:
            checking = []

            ## Grab the choice values in the problematic cells
            for num in prob:
                checking.append(poss[num])

            ## If the cell choice is invalid then "skip" this choice
            condition = check_row_or_col(checking)


            if not condition:
                skip = True
                break

        if skip:
            continue

        ## Only add if choice is valid against problematic cells and intial grid
        filtered_possibilities.append(poss)

    ## Reset the cage choices
    cage.possibilities = filtered_possibilities
    cage.good_possibilities = cage.possibilities

## Find all cage possibilities using functions above
def find_cage_possibilities(cages, grid):
    for cage in cages:
        ## Use right function according to operation
        if cage.op == "+":
            find_add_possibilities(cage)

        if cage.op == "-":
            find_sub_possibilities(cage)

        if cage.op == "*":
            find_mult_possibilities(cage)

        if cage.op == "/":
            find_div_possibilities(cage)

        if cage.num_of_possibilities() == 0:
            print("No solution.")
            sys.exit()

        ## Remove invalid initial choices
        check_initial_possibilities(cage, grid)


'''
========================================
FUNCTIONS FOR GRID SOLVING NICE PROBLEMS
========================================
'''

'''
First take initial grid and filter each cage's possibilities according to the
initial "no operator" values in the grid. If a cage has only one possible
solution, it is added to the grid. If a new cage is added to the grid in the
current iteration then we call the function again with the new grid (this new
cage introduces new restrictions for other cages).

We check that a new cage is added by repeatedly adding every cage that has one
solution in each function call. A counter is used to check how many cages are
added each iteration.
Counter increases: New cage added and function is called again
Counter stays the same: No new cage added and function is exited (hit an
"equilibrium")
Counter decreases: Theoretically impossible :P
'''

## Add cages to the grid if there is only one possible solution
## Repeats until a "equilibrium" is hit or program exits if question complete
def make_grid(cages, grid, old_counter=0):
    ## Used to check if more cages are added this iteration
    counter = 0

    ## Check cages and add if only one solution; increment counter by 1 if so
    for cage in cages:
        check_possibilities(cage, grid)
        if cage.num_of_good_possibilities() == 1:
            counter += 1
            set_good_poss(cage, grid)

    ## Check grid and print if complete
    condition = check_grid(grid)

    if condition:
        print_grid(grid)
        sys.exit()

    else:
        ## If a cage has no solutions then the question is unsolvable
        for cage in cages:
            if cage.num_of_good_possibilities() == 0:
                print("No solution.")
                sys.exit()

        ## If the same amount of cages are added then we've hit an "equilibrium"
        ## so we exit
        if counter == old_counter:
            return "unfinished"

        ## Otherwise we continue
        return make_grid(cages, grid, counter)


## Check if possibilities are still okay with new grid
def check_possibilities(cage, grid):

    ## If there was already only one solution then we don't need to check again
    ## i.e. the grid is already filled in here so it must be correct :)
    if cage.num_of_good_possibilities() == 1:
        return None

    ## Reset the good choices
    already_approved_choices = cage.good_possibilities
    cage.good_possibilities = []

    ## Check each possible choice with the restrictions in the grid passed
    for poss in already_approved_choices:
        ## Check each cell with its respective row and column
        skip = False
        for i in range(cage.size):
            row = cage.cells[i][0]
            col = cage.cells[i][1]

            ## Check against row
            checking = [poss[i]]

            for num in grid[row]:
                if num != 0 and grid[row].index(num) != col:
                    checking.append(num)

            condition = check_row_or_col(checking)

            if not condition:
                skip = True
                break

            ## Check against column
            checking = [poss[i]]

            for row in grid:
                if row[col] != 0 and grid.index(row) != row:
                    checking.append(row[col])

            condition = check_row_or_col(checking)

            if not condition:
                skip = True
                break

        ## If invalid "skip"; otherwise add it as a good choice
        if skip:
            continue

        else:
            cage.good_possibilities.append(poss)





'''
============================================
FUNCTIONS FOR GRID SOLVING NOT NICE PROBLEMS
============================================
'''

'''
In some questions, we are left with some cages that do not reduce to only having
1 valid possibility (bunch of cages each with 2 or more choices). In this
situation we are forced to make a guess.

Firstly we grab the cage with the smallest amount of possibilities left (not
including cages with one solution). We then iterate through the possibilities
of this chosen cage, each time forcing the cage to have one valid possibility
(the current possibility). There are three outcomes:
Finished (program exits): The picked possibility is correct and everything is
smooth sailing
Broke: We have picked a very wrong possibility and another cage has no possible
solutions - if so we go to the next possibility
"Equilibrium": The picked possibility is looking good but we have hit another
equilibrium despite the new restriction - we call the function again with a new
cage

This process should only end if the question is unsolvable. If one cage breaks
for all of its possibilities, then the cage is ignored and we iterate to the
next possibility of the previous cage picked.

Since we might hit an "equilibrium" multiple times in a single question, we will
have multiple cages where we are forcing a single possibility. Therefore I opted
to use a list and index as a "global" reference to all cages rather than have a
local cage in each function call (was having a bunch of issues when dealing with
a local cage).

I opt to choose cages with less possibilities in an attempt to reduce the run
time (would rather iterate through 2 possibilities - 50 50 chance - than a cage
with 5+ possibilities). This might not be the best approach - i.e. I could try
and find the most "influential" cage to introduce more restrictions but :P :P :P
'''

## Same as make_grid but adding a few small changes
def make_grid_modified(cages, grid, cage_min_list, old_counter):
    ## Used to check if more cages are added this iteration
    counter = 0

    ## Check cages and add if only one solution; increment counter by 1 if so
    for cage in cages:
        check_possibilities_modified(cage, grid, cage_min_list)

        if cage.num_of_good_possibilities() == 1:
            counter += 1
            set_good_poss(cage, grid)

    ## Check grid and print if complete
    condition = check_grid(grid)

    if condition:
        print_grid(grid)
        sys.exit()

    else:
        ## If a cage has no solutions then the current forced possibilit(y/ies)
        ## (is/are) wrong
        for cage in cages:
            if cage.num_of_good_possibilities() == 0:
                return "broke"

        ## If the same amount of cages are added then we've hit an "equilibrium"
        if counter == old_counter:
            return "unfinished"

        ## Otherwise we continue
        return make_grid_modified(cages, grid, cage_min_list, counter)


## Controls this whole "guessing" process
def make_grid_hard(cages, grid, cage_min_list, index):
    cage_min = cage_min_list[index]
    possibilities = cage_min.good_possibilities[:]
    cages_index = cages.index(cage_min)

    ## Iterate through each possibility
    for poss in possibilities:
        ## Force the current possibility to be the correct solution
        cages[cages_index].good_possibilities = [poss]
        cage_min.good_possibilities = [poss]

        ## Set the cage
        set_good_poss(cages[cages_index], grid)

        ## Start making the grid
        condition = make_grid_modified(cages, grid, cage_min_list, 0)

        ## If possibility is wrong we reset grid and iterate to next possibility
        if condition == "broke":
            for cage in cages:
                if cage not in cage_min_list:
                    remove_poss(cage, grid)
                    cage.good_possibilities = cage.possibilities

            continue

        ## If unfinished ("equilibrium") we pick a new cage to "guess" with
        else:
            cage_min_new = None

            for cage in cages:
                ## Find the first incomplete cage that hasn't been picked
                if (cage not in cage_min_list) and (not cage_min_new) and (cage.num_of_good_possibilities() > 1):
                    cage_min_new = cage

                ## Once a cage has been found, start looking for the optimum one
                if (cage.num_of_good_possibilities() > 1) and (cage.num_of_good_possibilities() < cage_min_new.num_of_good_possibilities()):
                    cage_min_new = cage

            ## Add this cage to the end of the list and call this function again
            ## using this new cage
            cage_min_list.append(cage_min_new)
            make_grid_hard(cages, grid, cage_min_list, index + 1)



    ## If all possibilities are wrong - i.e. the possibility in the previous
    ## cage is wrong, remove this cage from the list and grid
    remove_poss(cage_min, grid)
    cage_min_list.pop(index)
    ## We also want to reset its possibilities
    cages[cages_index].good_possibilities = possibilities


## Check if possibilities are still okay with new grid (slightly modified)
def check_possibilities_modified(cage, grid, cage_min_list):
    ## If the cage is being forcefully added we don't want to mess with this
    if cage in cage_min_list:
        return None

    ## Reset the good choices and grab all possible choices
    choices = cage.possibilities
    cage.good_possibilities = []

    ## If the cage has been properly placed then we know its correct and don't
    ## want to mess with it either
    row = cage.cells[0][0]
    col = cage.cells[0][1]

    if grid[row][col] != 0:
        poss = get_poss(cage, grid)
        cage.good_possibilities.append(poss)
        return None

    ## Check each possible choice with the restrictions in the grid passed
    for poss in choices:
        skip = False
        ## Check each cell with its respective row and column
        for i in range(cage.size):
            row = cage.cells[i][0]
            col = cage.cells[i][1]

            ## Check against row
            checking = [poss[i]]

            for num in grid[row]:
                if num != 0 and grid[row].index(num) != col:
                    checking.append(num)

            condition = check_row_or_col(checking)

            if not condition:
                skip = True
                break

            ## Check against column
            checking = [poss[i]]

            for row in grid:
                if row[col] != 0 and grid.index(row) != row:
                    checking.append(row[col])

            condition = check_row_or_col(checking)

            if not condition:
                skip = True
                break

        ## If invalid "skip"; otherwise add it as a good choice
        if skip:
            continue
        else:
            cage.good_possibilities.append(poss)



'''
==================================
FUNCTIONS USED AS TOOLS THROUGHOUT
==================================
'''

## Checks if a row or column abides by sudoku rules (and each cell is nonzero -
## unknown cell is given value 0)
def check_row_or_col(ls):
    for i in range(0, len(ls)):
        for j in range(i + 1, len(ls)):
            if ls[i] == ls[j] or ls[i] == 0 or ls[j] == 0:
                return False


    return True

## Sets single cage solution to the grid (using Cage.possibilities)
def set_poss(cage, grid):
    for num in range(len(cage.cells)):
        x = cage.cells[num][0]
        y = cage.cells[num][1]

        grid[x][y] = cage.possibilities[0][num]

## Sets single cage solution to the grid (using Cage.good_possibilities instead)
def set_good_poss(cage, grid):
    for num in range(len(cage.cells)):
        x = cage.cells[num][0]
        y = cage.cells[num][1]

        grid[x][y] = cage.good_possibilities[0][num]

## Gets the solution of a cage from the grid
def get_poss(cage, grid):
    ls = []
    for num in range(len(cage.cells)):
        x = cage.cells[num][0]
        y = cage.cells[num][1]

        ls.append(grid[x][y])

    return ls

## Removes the solution of a cage from the grid
def remove_poss(cage, grid):
    for num in range(len(cage.cells)):
        x = cage.cells[num][0]
        y = cage.cells[num][1]

        grid[x][y] = 0

## Check if the grid is complete
def check_grid(grid):

    for row in grid:
        condition = check_row_or_col(row)
        if not condition:
            return False

    for i in range(6):
        col = [grid[i][0], grid[i][1], grid[i][2], grid[i][3], grid[i][4], grid[i][5]]
        condition = check_row_or_col(col)
        if not condition:
            return False

    return True

## Print grid nicely
def print_grid(grid):
    for row in grid:
        for i in range(6):
            row[i] = str(row[i])
        print(' '.join(row))




if __name__ == "__main__":
    ## Get information from stdin
    grid_format = get_grid_format()
    cages = get_cages(grid_format)

    ## Initialise cages and grid
    check_cages(cages)
    grid = initialise_grid(cages)
    find_cage_possibilities(cages, grid)

    ## Try and answer without guessing
    make_grid(cages, grid)

    ## Choose the optimum cage to "guess" with
    cage_min = cages[0]

    for cage in cages:
        ## First priority is least number of possibilities (except 1 solution)
        if cage.num_of_good_possibilities() < cage_min.num_of_good_possibilities() and cage.num_of_good_possibilities() > 1:
            cage_min = cage

        ## Second priority is largest size of cage
        if cage.num_of_good_possibilities() == cage_min.num_of_good_possibilities() and cage.size > cage_min.size:
            cage_min = cage

    ## Start "guessing"
    make_grid_hard(cages, grid, [cage_min], 0)

    ## Question is unsolvable :p
    print("No solution.")
