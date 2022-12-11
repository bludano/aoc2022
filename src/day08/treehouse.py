from typing import Dict, Tuple, MutableSet
import copy
#import logging
import os
import pathlib

def treegrid_from_text(text) -> Tuple[Dict[Tuple[int, int], int], int, int]:
    """Given tree heights represented as a grid, presented as text in columns and rows, return 
    - the grid
    - the column height
    - the row length
    """
    grid = dict()
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if line == '':
            i -= 1
            continue
        for j, digit_ in enumerate(line):
            digit = int(digit_)
            grid[(i, j)] = digit
    max_i = i
    max_j = j
    return grid, max_i, max_j

def get_indices_of_trees_at_edge_from_treegrid(
    grid: Dict[Tuple[int, int], int],
    max_column_index: int,
    max_row_index: int) -> MutableSet[Tuple[int, int]]:
    trees_at_edge = set()
    for i in range(max_column_index+1):
        trees_at_edge.add((i, 0)) # all trees in leftmost column
        trees_at_edge.add((i, max_column_index)) # all trees in rightmost column
    for j in range(max_row_index+1):
        trees_at_edge.add((0, j)) # all trees in topmost row
        trees_at_edge.add((max_row_index, j)) # all trees in bottommost row
    return trees_at_edge

def get_interior_grid_indices_from_grid(
    grid: Tuple[Dict[Tuple[int, int], int], int, int],
    max_column_index: int,
    max_row_index: int) -> MutableSet[Tuple[int, int]]:
    interior_grid: Dict[Tuple[int, int], int] = copy.deepcopy(grid)
    for i, j in get_indices_of_trees_at_edge_from_treegrid(grid, max_column_index, max_row_index):
        del interior_grid[(i, j)]
    return {k for k in interior_grid.keys()}

def get_visible_trees_from_grid(
    grid: Tuple[Dict[Tuple[int, int], int], int, int],
    max_column_index: int,
    max_row_index: int):
    visible_trees = dict()
    trees_at_edge_indices = get_indices_of_trees_at_edge_from_treegrid(grid, max_column_index, max_row_index)
    # add trees at edge - all visible
    for tree in trees_at_edge_indices:
        visible_trees[tree] = grid[tree]
    interior_tree_indices = sorted(get_interior_grid_indices_from_grid(grid, max_column_index, max_row_index))
    for tree in interior_tree_indices:
        i, j = tree
        tree_height = grid[tree]

        # above
        tree_visible_from_above = True
        for k in range(i):
            other_tree = k, j
            other_tree_height = grid[other_tree]
            if other_tree_height >= tree_height:
                tree_visible_from_above = False
                break

        # below
        tree_visible_from_below = True
        for k in range(i+1, max_column_index+1):
            other_tree = k, j
            other_tree_height = grid[other_tree]
            if other_tree_height >= tree_height:
                tree_visible_from_below = False
                break

        # left
        tree_visible_from_left = True
        for k in range(j):
            other_tree = i, k
            other_tree_height = grid[other_tree]
            if other_tree_height >= tree_height:
                tree_visible_from_left = False
                break

        # right
        tree_visible_from_right = True
        for k in range(j+1, max_row_index+1):
            other_tree = i, k
            other_tree_height = grid[other_tree]
            if other_tree_height >= tree_height:
                tree_visible_from_right = False
                break
        
        tree_visible = (
            tree_visible_from_above or 
            tree_visible_from_below or 
            tree_visible_from_left or 
            tree_visible_from_right
        )
        if tree_visible:
            visible_trees[tree] = grid[tree]

    return visible_trees

def get_scenic_scores_from_grid(
    grid: Tuple[Dict[Tuple[int, int], int], int, int],
    max_column_index: int,
    max_row_index: int) -> Dict[Tuple[int, int], int]:

    interior_tree_indices = sorted(get_interior_grid_indices_from_grid(grid, max_column_index, max_row_index))
    scenic_scores = dict()
    for tree in interior_tree_indices:
        i, j = tree
        tree_height = grid[tree]

        # above
        scenic_score_above = 0
        for k in reversed(range(i)):
            other_tree = k, j
            other_tree_height = grid[other_tree]
            scenic_score_above += 1
            if other_tree_height >= tree_height:
                break

        # below
        scenic_score_below = 0
        for k in range(i+1, max_column_index+1):
            other_tree = k, j
            other_tree_height = grid[other_tree]
            scenic_score_below += 1
            if other_tree_height >= tree_height:
                break
        
        # left
        scenic_score_left = 0
        for k in reversed(range(j)):
            other_tree = i, k
            other_tree_height = grid[other_tree]
            scenic_score_left += 1
            if other_tree_height >= tree_height:
                break
        
        # right
        scenic_score_right = 0
        for k in range(j+1, max_row_index+1):
            other_tree = i, k
            other_tree_height = grid[other_tree]
            scenic_score_right += 1
            if other_tree_height >= tree_height:
                break

        scenic_score = scenic_score_above * scenic_score_below * scenic_score_left * scenic_score_right
        scenic_scores[tree] = scenic_score
    return scenic_scores

def main():
    filepath = os.environ['TREE_GRID_FILE']
    assert pathlib.Path(filepath).exists(), f"Want input, got {filepath}"
    with open(filepath, 'r') as f:
        lines = f.read()
    treegrid = treegrid_from_text(lines)

    # part 1 - visible trees
    visible_trees = get_visible_trees_from_grid(*treegrid)
    print(f"visible trees: {len(visible_trees)}")

    # part 2 - scenic scores
    scenic_scores = get_scenic_scores_from_grid(*treegrid)
    print(f"max scenic score: {max(scenic_scores.values())}")

if __name__ == '__main__':
    main()
