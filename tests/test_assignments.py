import pytest
import textwrap
from day04 import assignments
import pathlib

@pytest.fixture
def demo_data():
    contents = textwrap.dedent("""\
        2-4,6-8
        2-3,4-5
        5-7,7-9
        2-8,3-7
        6-6,4-6
        2-6,4-8
    """)
    return contents

@pytest.fixture
def demo_data_file(tmpdir, demo_data):
    fp = pathlib.Path(tmpdir / 'demo_data.txt')
    with open(fp, 'w') as f:
        f.write(demo_data)
    return fp

assignment_tuple_test_cases = (("1-2", (1,2)), ("3-7", (3,7)), ("42-42", (42,42)))

@pytest.mark.parametrize(
    "input,expected_output",
    assignment_tuple_test_cases,
    ids=(
        tc[0] for tc in assignment_tuple_test_cases
    )
)
def test_assignment_tuple(input, expected_output):
    output = assignments.assignment_tuple(input)
    assert output == expected_output

def test_elf_assignments_from_file(demo_data_file):
    elf_assignments = assignments.elf_assignments_from_file(demo_data_file)
    expected_elf_assignments = ((2, 4), (6, 8)), ((2, 3), (4, 5)), ((5, 7), (7, 9)), ((2, 8), (3, 7)), ((6, 6), (4, 6)), ((2, 6), (4, 8))
    assert elf_assignments == expected_elf_assignments

assignment_contains_fully_wasted_elf_test_cases = (
    (((2, 4), (6, 8)), False),
    (((2, 3), (4, 5)), False),
    (((5, 7), (7, 9)), False),
    (((2, 8), (3, 7)), True),
    (((6, 6), (4, 6)), True),
    (((2, 6), (4, 8)), False),
)

@pytest.mark.parametrize(
    "assignment,expected_wasted_elf",
    (
        (tc[0], tc[1]) for tc in assignment_contains_fully_wasted_elf_test_cases
    ),
    ids=(str(tc[0]) for tc in assignment_contains_fully_wasted_elf_test_cases)
)
def test_assignment_contains_fully_wasted_elf(assignment, expected_wasted_elf):
    wasted_elf = assignments.assignment_contains_fully_wasted_elf(assignment)
    assert wasted_elf == expected_wasted_elf

def test_elf_assignments_with_fully_wasted_elf():
    elf_assignments = ((2, 4), (6, 8)), ((2, 3), (4, 5)), ((5, 7), (7, 9)), ((2, 8), (3, 7)), ((6, 6), (4, 6)), ((2, 6), (4, 8))
    expected_assignments_with_fully_wasted_elf = ((2, 8), (3, 7)), ((6, 6), (4, 6))
    assignments_with_fully_wasted_elf = assignments.elf_assignments_with_fully_wasted_elf(elf_assignments)
    assert assignments_with_fully_wasted_elf == expected_assignments_with_fully_wasted_elf

@pytest.fixture
def assignments_with_fully_wasted_elves():
    return ((2, 8), (3, 7)), ((6, 6), (4, 6))

def test_count_assignments(assignments_with_fully_wasted_elves):
    wasted_elf_count = assignments.count_assignments(assignments_with_fully_wasted_elves)
    assert wasted_elf_count == 2

def test_elf_assignments_with_partially_wasted_elf():
    elf_assignments = ((2, 4), (6, 8)), ((2, 3), (4, 5)), ((5, 7), (7, 9)), ((2, 8), (3, 7)), ((6, 6), (4, 6)), ((2, 6), (4, 8))
    expected_assignments_with_partially_wasted_elf = ((5, 7), (7, 9)), ((2, 8), (3, 7)), ((6, 6), (4, 6)), ((2, 6), (4, 8))
    assignments_with_partially_wasted_elf = assignments.elf_assignments_with_partially_wasted_elf(elf_assignments)
    assert assignments_with_partially_wasted_elf == expected_assignments_with_partially_wasted_elf

def test_main(monkeypatch, demo_data_file, capsys):
    monkeypatch.setenv('ELF_ASSIGNMENTS_FILE', str(demo_data_file))
    assignments.main()
    written_to_output = capsys.readouterr().out
    assert written_to_output == "2 elves available for reassignment\n4 elves could be put to better use\n"
