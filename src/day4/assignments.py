from typing import TypeVar, Union, Iterable, Tuple
import pathlib
import os

PathT = TypeVar('PathT', bound=pathlib.Path)

def assignment_tuple(text_assignment: str) -> Tuple[int, int]:
    first_last = text_assignment.split('-')
    return (int(first_last[0]), int(first_last[1]))

def elf_assignments_from_file(filepath: Union[PathT, str]) -> Iterable[Tuple[Tuple, Tuple]]:
    p = pathlib.Path(filepath)
    assert p.exists(), f"Elf assignments file not found: {p}"
    with open(p, 'r') as f:
        lines = f.read().splitlines()
    assignment_pairs = (line.split(',') for line in lines)
    return tuple((assignment_tuple(assignment_pair[0]), assignment_tuple(assignment_pair[1])) for assignment_pair in assignment_pairs)

def assignment_contains_fully_wasted_elf(assignment: Tuple[Tuple, Tuple]) -> bool:
    elf_0, elf_1 = assignment
    for elf_leader_sections, elf_helper_sections in ((elf_0, elf_1), (elf_1, elf_0)):
        elf_leader_first_section, elf_leader_last_section = elf_leader_sections
        elf_helper_first_section, elf_helper_last_section = elf_helper_sections
        if elf_helper_first_section >= elf_leader_first_section and elf_helper_last_section <= elf_leader_last_section:
            return True
    return False

def elf_assignments_with_fully_wasted_elf(assignments: Iterable[Tuple[Tuple, Tuple]]) -> Iterable[Tuple[Tuple, Tuple]]:
    return tuple(filter(assignment_contains_fully_wasted_elf, assignments))

def assignment_contains_partially_wasted_elf(assignment: Tuple[Tuple, Tuple]) -> bool:
    elf_0, elf_1 = assignment
    for elf_leader_sections, elf_helper_sections in ((elf_0, elf_1), (elf_1, elf_0)):
        elf_leader_first_section, elf_leader_last_section = elf_leader_sections
        elf_helper_first_section, elf_helper_last_section = elf_helper_sections
        if elf_helper_first_section >= elf_leader_first_section and elf_helper_first_section <= elf_leader_last_section:
            return True
    return False

def elf_assignments_with_partially_wasted_elf(assignments: Iterable[Tuple[Tuple, Tuple]]) -> Iterable[Tuple[Tuple, Tuple]]:
    return tuple(filter(assignment_contains_partially_wasted_elf, assignments))

def count_assignments(assignments: Iterable[Tuple[Tuple, Tuple]]) -> int:
    return len(assignments)

def main():
    elf_assignments = elf_assignments_from_file(os.environ['ELF_ASSIGNMENTS_FILE'])

    # part 1
    fully_wasted_elves = elf_assignments_with_fully_wasted_elf(elf_assignments)
    num_fully_wasted_elves = count_assignments(fully_wasted_elves)
    print(f"{num_fully_wasted_elves} elves available for reassignment")

    # part 2
    partially_wasted_elves = elf_assignments_with_partially_wasted_elf(elf_assignments)
    num_partially_wasted_elves = count_assignments(partially_wasted_elves)
    print(f"{num_partially_wasted_elves} elves could be put to better use")

if __name__ == '__main__':
    main()
