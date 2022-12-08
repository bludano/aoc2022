import pytest
from day8 import treehouse
import textwrap

@pytest.fixture
def sample():
    return textwrap.dedent("""\
        30373
        25512
        65332
        33549
        35390
        """)

@pytest.fixture
def sample_file(sample, tmpdir):
    fp = tmpdir / 'tree-grid.txt'
    with open(fp, 'w') as f:
        f.write(sample)
    return fp

def test_treegrid_from_text_does_not_fall_over(sample):
    treehouse.treegrid_from_text(sample)

@pytest.fixture
def grid_and_sizes(sample):
    return treehouse.treegrid_from_text(sample)

def test_treegrid_from_text_has_expected_number_of_trees(grid_and_sizes):
    grid, _, _ = grid_and_sizes
    assert len(grid) == 25

def test_treegrid_from_text_has_expected_column_length(grid_and_sizes):
    _, max_column_index, _ = grid_and_sizes
    assert max_column_index == 4

def test_treegrid_from_text_has_expected_row_length(grid_and_sizes):
    _, _, max_row_index = grid_and_sizes
    assert max_row_index == 4

def test_get_indices_of_trees_at_edge_from_treegrid(grid_and_sizes):
    grid, max_column_index, max_row_index = grid_and_sizes
    trees_at_edge = treehouse.get_indices_of_trees_at_edge_from_treegrid(grid, max_column_index, max_row_index)
    expected_trees_at_edge = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 4), (2, 0), (2, 4), (3, 0), (3, 4), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
    assert sorted(trees_at_edge) == expected_trees_at_edge

def test_get_interior_grid_indices_from_grid_returns_expected_indices(grid_and_sizes):
    interior_grid_indices = treehouse.get_interior_grid_indices_from_grid(*grid_and_sizes)
    expected_interior_grid_indices = {(1, 2), (2, 1), (3, 1), (1, 1), (2, 3), (3, 3), (2, 2), (3, 2), (1, 3)}
    assert interior_grid_indices == expected_interior_grid_indices

def test_get_visible_trees_from_grid_returns_correct_number_of_trees(grid_and_sizes):
    visible_trees = treehouse.get_visible_trees_from_grid(*grid_and_sizes)
    assert len(visible_trees) == 21

def test_get_scenic_scores_from_grid(grid_and_sizes):
    scenic_scores = treehouse.get_scenic_scores_from_grid(*grid_and_sizes)
    expected_scenic_scores = {(1, 1): 1, (1, 2): 4, (1, 3): 1, (2, 1): 6, (2, 2): 1, (2, 3): 2, (3, 1): 1, (3, 2): 8, (3, 3): 3}
    assert scenic_scores == expected_scenic_scores

def test_main(sample_file, monkeypatch, capsys):
    monkeypatch.setenv('TREE_GRID_FILE', str(sample_file))
    treehouse.main()
    written_to_output = capsys.readouterr().out
    assert written_to_output == 'visible trees: 21\nmax scenic score: 8\n'
