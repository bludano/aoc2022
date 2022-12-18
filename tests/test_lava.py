import pytest
import textwrap
from day18 import lava

def sample():
    return textwrap.dedent("""\
        2,2,2
        1,2,2
        3,2,2
        2,1,2
        2,3,2
        2,2,1
        2,2,3
        2,2,4
        2,2,6
        1,2,5
        3,2,5
        2,1,5
        2,3,5

    """)

@pytest.fixture
def sample_fx():
    return sample()

@pytest.fixture
def sample_file(sample_fx, tmpdir):
    fp = tmpdir / 'lava.txt'
    with open(fp, 'w') as f:
        f.write(sample_fx)
    return fp

adjacent_test_cases = (
    ((1,1,1),(1,1,1),False),
    ((1,1,1),(1,1,0),True),
    ((1,1,1),(1,1,2),True),
    ((1,1,1),(1,1,3),False),
)

@pytest.mark.parametrize(
    "c0, c1, expected_result", adjacent_test_cases, ids=(f"c0={tc[0]}, c1={tc[1]}" for tc in adjacent_test_cases)
)
def test_adjacent(c0, c1, expected_result):
    # Arrange

    # Act
    result = lava.adjacent(c0, c1)

    # Assert
    assert result == expected_result

adjacent_coordinates_test_cases = (
    ((1,1,1), ((0,1,1),(2,1,1),(1,0,1),(1,2,1),(1,1,0),(1,1,2),)),
)

@pytest.mark.parametrize(
    "input_coord, expected_adjacent_coords", adjacent_coordinates_test_cases, ids=(str(tc[0]) for tc in adjacent_coordinates_test_cases)
)
def test_adjacent_coordinates(input_coord, expected_adjacent_coords):
    # Arrange

    # Act
    adj_coords = set(lava.adjacent_coordinates(input_coord))

    # Assert
    assert adj_coords == set(expected_adjacent_coords)

number_of_adjacencies_in_set_test_cases = (
    (set(((0,0,0),)), 0, 6),
    (set(((0,0,0),(0,0,0))), 0, 6),
    (set(((0,0,0),(0,0,1))), 2, 10),
    (set(((0,0,0),(0,0,1),(0,1,1))), 4, 14),
    (set(((0,0,0),(0,0,1),(0,1,1),(-1,-1,-1))), 4, 20),
    (set(((0,0,0),(1,0,0),(0,0,1),(1,0,1))), 8, 16),
    (set(((0,0,0),(1,0,0),(1,0,1),(2,2,2))), 4, 20),
)

@pytest.mark.parametrize(
    "input_set, expected_number_of_adjacencies, expected_surface_area",
    number_of_adjacencies_in_set_test_cases
)
def test_number_of_adjacencies_in_set(input_set, expected_number_of_adjacencies, expected_surface_area):
    # Arrange

    # Act
    number_of_adjacencies = lava.number_of_adjacencies_in_set(input_set)

    # Assert
    assert number_of_adjacencies == expected_number_of_adjacencies

@pytest.mark.parametrize(
    "input_set, expected_number_of_adjacencies, expected_surface_area",
    number_of_adjacencies_in_set_test_cases
)
def test_total_surface_area_of_set(input_set, expected_number_of_adjacencies, expected_surface_area):
    # Arrange

    # Act
    surface_area = lava.total_surface_area_of_set(input_set)

    # Assert
    assert surface_area == expected_surface_area

def test_interior_space_of_set(sample_fx):
    # Arrange
    coords = lava.coords_from_lines(sample_fx.split('\n'))

    # Act
    interior_space = lava.interior_space_of_set(coords)

    # Assert
    assert interior_space == {(2, 2, 3), (2, 2, 4), (2, 2, 5), (2, 2, 2)}

def test_interior_missing_cubes(sample_fx):
    # Arrange
    coords = lava.coords_from_lines(sample_fx.split('\n'))

    # Act
    missing_cubes = lava.interior_missing_cubes(coords)

    # Assert
    assert missing_cubes == {(2, 2, 5)}

def test_trapped_cubes(sample_fx):
    # Arrange
    coords = lava.coords_from_lines(sample_fx.split('\n'))

    # Act
    trapped_cubes = lava.trapped_cubes(coords)

    # Assert
    assert trapped_cubes == {(2, 2, 5)}


def test_main(sample_file, monkeypatch, capsys):
    # Arrange
    monkeypatch.setenv('CUBE_INPUT_FILE', str(sample_file))

    # Act
    lava.main()

    # Assert
    written_to_output = capsys.readouterr().out
    assert written_to_output == 'Part 1 - surface area: 64\nPart 2 - exterior surface area: 58\n'
