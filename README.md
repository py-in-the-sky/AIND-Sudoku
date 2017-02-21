# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?
A: We know from "Naked Twins" that when two boxes from the same unit permit only the exact same two digits, then no other box in the unit can permit those two digits. We implement this with constraint propagation in the following way. For each unit, we identify all cases of Naked Twins. For each case of Naked Twins, we remember the two boxes and the two digits. We then propagate this information to the other seven boxes in the unit by removing the two digits from their permissible values. Then no box in the unit, except for the two naked-twin squares, permit the twin values.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?
A: This is easy. We simply need to include in `unitlist` the two main diagonals of the Sudoku board (i.e., `[r+c for r,c in zip(rows, cols)]` and `[r+c for r,c in zip(reversed(rows), cols)]`). Then for every box on a main diagonal, `peers` will include the other boxes on the diagonal. The functions `only_choice` and `naked_twins` use the `unitlist` data structure to identify boxes to which they propagate constraints, and the function `eliminate` similarly uses the `peers` data structure. So by including the main diagonals in `unitlist`, we ensure they will be used like any other unit when the code propagates constraints. (See lines 76 and 77 from `solution.py`.)

# Student Personalization

I chose to implement the Hidden Twins strategy. See line 84 in `solution.py` for the implementation, and see line 98 in `solution_test.py` for a unit test of the `hidden_twins` function.

I also wrote a `benchmark` function (see line 270 of `solution.py`) because I wanted to test how additional Sudoku strategies affected the runtime. The benchmarking uses the 11 [hardest](http://norvig.com/hardest.txt) Sudoku grids from Peter Norvig's blog post about his Sudoku solution. For ten iterations, it calls `solve` on each of the Sudoku grids and the reports the average time it takes to solve all 11 Sudoku grids, the number of times each Sudoku strategy is used, and the number of invocations of the `search` function.

I ran the benchmarking once using just the Eliminate and Only Choice strategies; then again with the addition of the Naked Twins Strategy; then again with the addition of the Hidden Twins strategy. The results are below.

* Using Eliminate and Only Choice for constraint propagation:
  * On average 1.56 seconds to solve all 11 grids
  * Only Choice updates the board 1115 times
  * Number of calls to `search`: 110

* Using Eliminate, Only Choice, and Naked Twins for constraint propagation:
  * On average 1.41 seconds to solve all 11 grids
  * Only Choice updates the board 1069 times
  * Naked Twins updates the board 219 times
  * Number of calls to `search`: 111

* Using Eliminate, Only Choice, Naked Twins, and Hidden Twins for constraint propagation:
  * On average 1.56 seconds to solve all 11 grids
  * Only Choice updates the board 1127 times
  * Naked Twins updates the board 184 times
  * Hidden Twins updates the board 289 times
  * Number of calls to `search`: 113

A prelimary look at these results suggests that the addition of Hidden Twins added more work than it saved for the solver: that is, the Hidden Twins made the search space slightly larger (as indicated by `search_invocations` getting larger) and required more overall work to be performed due to the new function, `hidden_twins`, having to be executed for every iteration of the constraint propagation.


### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
