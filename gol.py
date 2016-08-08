import numpy as np
import functools
import itertools

size = (80, 40)
seed_of_creation = np.array([np.random.rand(size[0]) for x in np.arange(size[0])])
all_true = np.array([[True for x in np.arange(size[1])] for y in np.arange(size[1])])

bool_of_seed = seed_of_creation > 0.4

# iterations = []

def move_all_left(array):
    new_array = np.delete(array, 0, 1)
    new_array = np.hstack((new_array, np.array([[False] for x in np.arange(array.shape[1])])))
    return new_array

def move_all_right(array):
    new_array = np.delete(array, -1, 1)
    new_array = np.hstack((np.array([[False] for x in np.arange(array.shape[1])]), new_array))
    return new_array

def move_all_up(array):
    return np.append(np.delete(array, 0, 0), [[False for x in np.arange(array.shape[0])]], axis=0)

def move_all_down(array):
    return np.concatenate(([[False for x in np.arange(array.shape[0])]], np.delete(array, -1, 0)), axis=0)

# @functools.lru_cache()
def iterate_cell(merged_cell):
    """Takes a cell and sum of neighbours and returns True/False if the cell is
    alive/dead. """
    cell = bool(merged_cell & 16)
    sum_of_neighbours = merged_cell - 16 if cell else merged_cell

    if 2 <= sum_of_neighbours <= 3 and cell:
        # if between 2 and 3 nbrs, keep alive
        return True
    elif not cell and sum_of_neighbours == 3:
        # else if 3 nbrs, make alive
        return True
    elif sum_of_neighbours < 2:
        # Else, if lonely, kill
        return False
    elif sum_of_neighbours > 3:
        # Else, if overpopulated, kill
        return False
    else:
        # No reason to keep alive
        return False

def make_merged_cells(array):
    corner_movements = list(itertools.product([move_all_down, move_all_up], [move_all_left, move_all_right]))
    simple_movements = list(itertools.product([move_all_right, move_all_left, move_all_up, move_all_down], [lambda x: x]))
    movements = corner_movements+simple_movements

    arrays = [1*f(g(array)) for f, g in movements]

    arrays.append(16*array)

    return np.sum(arrays, axis=0)


def next_iteration(array):
    return np.vectorize(iterate_cell)(make_merged_cells(array))

def print_grid(grid):
    for i in grid:
        for j in i:
            print("0" if j else "-", end="")
        print()


def produce_iterations(no_of_iterations, initial_seed=None):
    if initial_seed is None:
        initial_seed = bool_of_seed.copy()
    iterations = [initial_seed]
    # When I do this in the interpreter it doesn't break, but when I do it here, it does. Odd.
    #
    # TODO figure out why, and fix it.
    for x in np.arange(no_of_iterations):
        iterations.append(next_iteration(iterations[-1]))
        print_grid(iterations[-1])
        input("Press Enter to continue")

    return iterations[-1]

if __name__ == '__main__':
    import sys
    produce_iterations(int(sys.argv[-1]))
