from typing import Tuple, Iterable, TypeVar, Union, List
import string
import pathlib
import os

PathT = TypeVar('PathT', bound=pathlib.Path)

def get_rucksacks_from_file(filepath: Union[PathT, str]) -> Iterable[str]:
    p = pathlib.Path(filepath)
    assert p.exists(), f"Expected file to exist, got {filepath}"
    with open(p, 'r') as f:
        lines = [line.rstrip() for line in f.readlines()]
    return lines

def get_three_elf_groups_from_rucksacks(rucksacks: Iterable[str]) -> Iterable[List[str]]:
    three_elf_groups = []
    for i, rucksack in enumerate(rucksacks):
        if i % 3 == 0:
            current_group = []
        current_group.append(rucksack)
        if i % 3 == 2:
            three_elf_groups.append(current_group)
    if not i % 3 == 2:
        raise RuntimeError(f"Insufficient elfs to populate final three-elf group")
    return three_elf_groups

def get_badge_item_from_three_elf_group(three_elf_group: List[str]) -> str:
    A, B, C = three_elf_group
    A = set(A)
    B = set(B)
    C = set(C)
    for elem in A:
        if elem in B and elem in C:
            return elem
    raise RuntimeError(f"Expected one item to exist in all three rucksacks in three-elf group")

def get_rucksack_compartments(rucksack_manifest: str) -> Tuple[str, str]:
    total_number_of_items = len(rucksack_manifest)
    assert total_number_of_items % 2 == 0, f"Expected rucksack with even number of items across both apartments, got {total_number_of_items}"
    middle = int(total_number_of_items / 2)
    compartment_A = rucksack_manifest[:middle]
    compartment_B = rucksack_manifest[middle:]
    return (compartment_A, compartment_B)

def get_duplicated_element(compartment_pair: Tuple[str, str]) -> str:
    A, B = compartment_pair
    A = set(A)
    B = set(B)
    for checking, against in ((A, B), (B, A)):
        for elem in checking:
            if elem in against:
                return elem
    raise RuntimeError(f"Expected duplicated element, not found after exhaustive search, compartments: {compartment_pair}")

item_priority = {
    letter: i+1
    for i, letter in enumerate(string.ascii_letters)
}

def get_rucksack_item_priority(rucksack_manifest: str) -> int:
    compartments = get_rucksack_compartments(rucksack_manifest)
    duplicated_element = get_duplicated_element(compartments)
    priority = item_priority[duplicated_element]
    return priority

def get_total_rucksack_item_priority(rucksacks: Iterable[str]) -> int:
    return sum(get_rucksack_item_priority(rucksack) for rucksack in rucksacks)

def get_three_elf_group_badge_priority(three_elf_group: List[str]) -> int:
    return item_priority[get_badge_item_from_three_elf_group(three_elf_group)]

def get_total_three_elf_group_badge_priority(rucksacks: Iterable[str]) -> int:
    return sum(get_three_elf_group_badge_priority(rucksack) for rucksack in get_three_elf_groups_from_rucksacks(rucksacks))

def main():
    filepath = os.environ['RUCKSACK_FILE']
    assert pathlib.Path(filepath).exists(), f"Expected file to exist, got {filepath}"

    rucksacks = get_rucksacks_from_file(filepath)

    # part 1 - total priority of items in rucksacks
    total_priority = get_total_rucksack_item_priority(rucksacks)
    print(f"Total priority (part 1): {total_priority}")

    # part 2 - total badge priority of three-elf groups
    total_badge_priority = get_total_three_elf_group_badge_priority(rucksacks)
    print(f"Total badge priority (part 2): {total_badge_priority}")

if __name__ == '__main__':
    main()
