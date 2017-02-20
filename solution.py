from collections import defaultdict


assignments = []


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # For each unit, propagate the naked-twins constraint.
    for unit in unitlist:
        # 1) Find all instances of naked twins.
        twins_index = defaultdict(list)
        # twins_index is a mapping from pairs of digits to boxes that contain only those pairs of digits.
        # Example: { '89': ['A1', 'A3'], ... }
        for box in unit:
            if len(values[box]) == 2:
                twins_index[values[box]].append(box)
        twins = ((digit_pair, boxes)
                 for digit_pair,boxes in twins_index.items()
                 if len(boxes) >= 2)  # Collect all digit pairs that appear more than once in the unit.

        # 2) Eliminate the naked twins as possibilities for their peers.
        for (digit1, digit2), boxes in twins:
            box1, box2 = boxes[0], boxes[1]
            # We take just the first two boxes. If there are more than two boxes that contain the
            # pair of digits, then the excess boxes will each end up with no permissible digits.
            # This is fine: this invalid state will be caught upstream by reduce_puzzle.
            for unit_peer in (set(unit) - {box1, box2}):
                values[unit_peer] = values[unit_peer].replace(digit1, '')
                values[unit_peer] = values[unit_peer].replace(digit2, '')

    return values


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]


### Constants

digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
boxes = cross(rows, cols)  # Row-wise: ['A1', 'A2', ..., 'I8', 'I9']
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [[r+c for r,c in zip(rows, cols)], [r+c for r,c in zip(reversed(rows), cols)]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


### Personalization

def hidden_twins(values):
    """Eliminate values using the hidden twins strategy.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the hidden twins eliminated from peers.
    """
    # For each unit, propagate the hidden-twins constraint.
    for unit in unitlist:
        # 1) Find all instances of hidden twins.
        digits_index = defaultdict(list)
        for box in unit:
            for d in digits:
                if d in values[box]:
                    digits_index[d].append(box)
        twins_index = defaultdict(list)
        for digit,boxes in digits_index.items():
            if len(boxes) == 2:
                twins_index[tuple(boxes)].append(digit)
        twins = ((''.join(digit_list), boxes)
                 for boxes,digit_list in twins_index.items()
                 if len(digit_list) == 2)

        # 2) Assign the hidden twins to their boxes.
        for digit_pair, boxes in twins:
            for box in boxes:
                values[box] = digit_pair

    return values


def sudoku_strategies(values):
    """Use all Sudoku strategies to eliminate possibilities and assign digits.
    This is where constraint propagation happens.

    This function simply wraps eliminate, only_choice, naked_twins, and any other
    Sudoku strategy and calls them all in order on values.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary.
    """
    # strategies = (eliminate, only_choice)
    # strategies = (eliminate, only_choice, naked_twins)
    strategies = (eliminate, only_choice, naked_twins, hidden_twins)

    for strat in strategies:
        values = strat(values)

    return values

###


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    return {box: (digits if val == '.' else val) for box,val in zip(boxes, grid)}


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    filled_in_digits = ((box, vals) for box,vals in values.items() if len(vals) == 1)

    for box,digit in filled_in_digits:
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
            # If values[peer] is empty, then we're in an invalid state.

    return values


def only_choice(values):
    for u in unitlist:
        for d in digits:
            d_places = [box for box in u if d in values[box]]

            if len(d_places) == 1:
                box = d_places[0]
                assign_value(values, box, d)

    return values


def reduce_puzzle(values):
    stalled = False

    while not stalled:
        solved_values_before = sum(len(vals) == 1 for vals in values.values())
        vaues = sudoku_strategies(values)  # Use Sudoku strategies to solve for boxes and propagate constraints.
        solved_values_after = sum(len(vals) == 1 for vals in values.values())

        # If no new values were added, stop the loop.
        stalled = (solved_values_before == solved_values_after)

        # Sanity check, return False if there is a box with zero available values:
        if any(len(vals) == 0 for vals in values.values()):
            return False

    return values


def search(values):
    # First, reduce the puzzle using the previous function.
    values = reduce_puzzle(values)

    if values is False:  # Base case: board in invalid state.
        return False
    elif all(len(vals) == 1 for vals in values.values()):  # Base case: board solved.
        return values

    # Choose one of the unfilled squares with the fewest possibilities.
    _, best_box = min((len(vals), box) for box,vals in values.items() if len(vals) > 1)

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a
    # value (not False), return that answer! Otherwise, return False.
    for digit in values[best_box]:
        new_sudoku = values.copy()
        assign_value(new_sudoku, best_box, digit)
        solution = search(new_sudoku)

        if solution is not False:
            return solution

    return False


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
