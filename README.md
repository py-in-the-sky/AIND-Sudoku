# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?
A: We know from "Naked Twins" that when two boxes from the same unit permit only the exact same two digits, then no other box in the unit can permit those two digits. We implement this with constraint propagation in the following way. For each unit, we identify all cases of Naked Twins. For each case of Naked Twins, we remember the two boxes and the two digits. We then propagate this information to the other seven boxes in the unit by removing the two digits from their permissible values. Then no box in the unit, except for the two naked-twin squares, permit the twin values.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?
A: This is easy. We simply need to include in `unitlist` the two main diagonals of the Sudoku board (i.e., `[r+c for r,c in zip(rows, cols)]` and `[r+c for r,c in zip(reversed(rows), cols)]`). Then for every box on a main diagonal, `peers` will include the other boxes on the diagonal. The functions `only_choice` and `naked_twins` use the `unitlist` data structure to identify boxes to which they propagate constraints, and the function `eliminate` similarly uses the `peers` data structure. So by including the main diagonals in `unitlist`, we ensure they will be used like any other unit when the code propagates constraints. (See lines 66 and 67 from `solution.py`.)

# Student Personalization

I chose to implement the Hidden Twins strategy (see line 74 in `solution.py`).

I wanted to test how additional Sudoku strategies affected the runtime, so I added a `benchmark` function at line 245 and used the global variables `only_choice_uses`, `naked_twins_uses`, and `hidden_twins_uses` to see how many times these strategies were used across all eleven Sudoku grids in the benchmark function.

I did several runs using just the Eliminate and Only Choice strategies to propagate constraints; the time to solve all 11 Sudoku grids was roughly 0.53 seconds. Then I conducted several more runs after adding in the Naked Twins strategy; the time to solve all grids went up to roughly 0.54 seconds. And finally, I made several more runs after adding in the Hidden Twins strategy; the time went up to roughly 0.65 seconds.

On the final iteration, using all strategies, Only Choice was used 1127 times to reduce the board; Naked Twins was used 184 times to reduce the board; and Hidden Twins was used 289 times to reduce the boards.

On the other hand, when Eliminate and Only Choice were the only strategies used, surprisingly, Only Choice was used to reduce the board only 1115 times -- fewer than when all strategies were employed.

During the benchmarking runs, I also used the global variable `search_invocations` to keep track of the total number of calls to the `search` function, in order to get a measure of the search space. When Eliminate and Only Choice were the only strategies used, `search_invocations` was 110. When Naked Twins was added, `search_invocations` was 111. When Hidden Twins was added, `search_invocations` was 113.

A prelimary look at these results suggests that the addition of Naked Twins and Hidden Twins added more work than it saved for the solver: that is, the additional strategies made the search space slightly larger (as indicated by `search_invocations` getting larger) and required more overall work to be performed due to two new functions, `naked_twins` and `hidden_twins`, having to be executed for every iteration of the constraint propagation.


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
