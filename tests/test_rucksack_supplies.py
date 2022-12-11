import pytest
import textwrap
from day03 import rucksack_supplies

@pytest.fixture
def sample():
    return textwrap.dedent("""\
        vJrwpWtwJgWrhcsFMMfFFhFp
        jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
        PmmdzqPrVvPwwTWBwg
        wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
        ttgJtRGJQctTZtZT
        CrZsJsPPZsGzwwsLwLmpwMDw
    """)

@pytest.fixture
def rucksack_file(sample, tmpdir):
    filepath = tmpdir / 'rucksack_file.txt'
    with open(filepath, 'w') as f:
        f.write(sample)
    return filepath

_test_cases = (
    ('vJrwpWtwJgWrhcsFMMfFFhFp', 'vJrwpWtwJgWr', 'hcsFMMfFFhFp', 'p', 16),
    ('jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL', 'jqHRNqRjqzjGDLGL', 'rsFMfFZSrLrFZsSL', 'L', 38),
    ('PmmdzqPrVvPwwTWBwg', 'PmmdzqPrV', 'vPwwTWBwg', 'P', 42)
)

def test_get_rucksacks_from_file(rucksack_file):
    rucksacks = rucksack_supplies.get_rucksacks_from_file(rucksack_file)
    assert rucksacks[:3] == [tc[0] for tc in _test_cases]

def test_get_three_elf_groups_from_rucksacks(rucksack_file):
    rucksacks = rucksack_supplies.get_rucksacks_from_file(rucksack_file)
    three_elf_groups = rucksack_supplies.get_three_elf_groups_from_rucksacks(rucksacks)
    assert three_elf_groups == [
        ['vJrwpWtwJgWrhcsFMMfFFhFp', 'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL', 'PmmdzqPrVvPwwTWBwg'],
        ['wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn', 'ttgJtRGJQctTZtZT', 'CrZsJsPPZsGzwwsLwLmpwMDw']
    ]

def test_get_badge_item_from_three_elf_group(rucksack_file):
    rucksacks = rucksack_supplies.get_rucksacks_from_file(rucksack_file)
    three_elf_groups = rucksack_supplies.get_three_elf_groups_from_rucksacks(rucksacks)
    assert rucksack_supplies.get_badge_item_from_three_elf_group(three_elf_groups[0]) == 'r'
    assert rucksack_supplies.get_badge_item_from_three_elf_group(three_elf_groups[1]) == 'Z'

def test_get_three_elf_group_badge_priority(rucksack_file):
    rucksacks = rucksack_supplies.get_rucksacks_from_file(rucksack_file)
    three_elf_groups = rucksack_supplies.get_three_elf_groups_from_rucksacks(rucksacks)
    assert rucksack_supplies.get_three_elf_group_badge_priority(three_elf_groups[0]) == 18
    assert rucksack_supplies.get_three_elf_group_badge_priority(three_elf_groups[1]) == 52

def test_get_total_three_elf_group_badge_priority(rucksack_file):
    rucksacks = rucksack_supplies.get_rucksacks_from_file(rucksack_file)
    assert rucksack_supplies.get_total_three_elf_group_badge_priority(rucksacks) == 70

get_rucksack_compartments_test_cases = tuple(
    tc[:3] for tc in _test_cases
)

@pytest.mark.parametrize(
    "input, expected_comp_A, expected_comp_B", get_rucksack_compartments_test_cases, ids=tuple(tc[0] for tc in get_rucksack_compartments_test_cases)
)
def test_get_rucksack_compartments(input, expected_comp_A, expected_comp_B):
    comp_A, comp_B = rucksack_supplies.get_rucksack_compartments(input)
    assert comp_A == expected_comp_A
    assert comp_B == expected_comp_B

get_duplicated_element_test_cases = tuple(
    (tc[0], tc[3]) for tc in _test_cases
)

@pytest.mark.parametrize(
    "input, expected_element", get_duplicated_element_test_cases, ids=tuple(tc[0] for tc in get_duplicated_element_test_cases)
)
def test_get_duplicated_element(input, expected_element):
    element = rucksack_supplies.get_duplicated_element(rucksack_supplies.get_rucksack_compartments(input))
    assert element == expected_element

_item_priority_test_cases = (('a', 1), ('z', 26), ('A', 27), ('Z', 52))

@pytest.mark.parametrize(
    "letter, expected_priority", _item_priority_test_cases, ids=(tc[0] for tc in _item_priority_test_cases)
)
def test_item_priority(letter, expected_priority):
    priority = rucksack_supplies.item_priority[letter]
    assert priority == expected_priority

_rucksack_item_priority_test_cases = tuple(
    (tc[0], tc[4]) for tc in _test_cases
)

@pytest.mark.parametrize(
    "manifest, expected_priority", _rucksack_item_priority_test_cases, ids=(tc[0] for tc in _rucksack_item_priority_test_cases)
)
def test_get_rucksack_item_priority(manifest, expected_priority):
    priority = rucksack_supplies.get_rucksack_item_priority(manifest)
    assert priority == expected_priority

def test_get_total_rucksack_item_priority(rucksack_file):
    rucksacks = rucksack_supplies.get_rucksacks_from_file(rucksack_file)
    total_priority = rucksack_supplies.get_total_rucksack_item_priority(rucksacks)
    assert total_priority == 157

def test_main(rucksack_file, monkeypatch, capsys):
    monkeypatch.setenv('RUCKSACK_FILE', str(rucksack_file))
    rucksack_supplies.main()
    written_to_output = capsys.readouterr().out
    assert written_to_output == "Total priority (part 1): 157\nTotal badge priority (part 2): 70\n"
