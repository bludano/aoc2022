from typing import Tuple, Iterable, List
import copy
import os
import pathlib

def get_lines_from_text(text: str) -> Iterable[str]:
    return text.split('\n')

def get_initial_configuration_and_instructions_from_lines(lines: Iterable[str]) -> Tuple[Iterable[str], Iterable[str], Iterable[int]]:
    found_separator_line = False
    initial_configuration_lines = []
    instruction_lines = []
    indices = []
    for line in lines:
        if line == '':
            found_separator_line = True
            continue
        if found_separator_line:
            instruction_lines.append(line)
        elif '[' not in line and ']' not in line:
            for i, char in enumerate(line):
                if char != ' ':
                    indices.append(i)
        else:
            initial_configuration_lines.append(line)
    return initial_configuration_lines, instruction_lines, indices

def get_initial_stacks_from_config_lines(config_lines: Iterable[str], indices: Iterable[int]) -> List[List[str]]:
    max_initial_crate_height = len(config_lines)
    num_stacks = len(indices)
    stacks = [list() for _ in range(num_stacks)]
    for i in range(max_initial_crate_height, -1, -1):
        for j, index in enumerate(indices):
            try:
                char = config_lines[i][index]
            except IndexError:
                pass
            else:
                #if char not in (' ', '[', ']'):
                if char != ' ':
                    stacks[j].append(char)
    return stacks

def move_item_from_stack_to_stack(stacks: List[List[str]], from_stack: int, to_stack: int, k: int = 1, multi_crate_mover: bool = False) -> List[List[str]]:
    stacks_ = copy.deepcopy(stacks)
    temp_storage = list()
    from_stack_ = from_stack - 1
    to_stack_ = to_stack - 1
    for _ in range(k):
        temp_storage.append(stacks_[from_stack_].pop())
    if not multi_crate_mover:
        stacks_[to_stack_].extend(temp_storage)
    else:
        for _ in range(k):
            stacks_[to_stack_].append(temp_storage.pop())
    return stacks_

def execute_rearrangement(stacks: List[List[str]], rearrangement_str: str, multi_crate_mover: bool = False) -> List[List[str]]:
    command = rearrangement_str.split(' ')
    assert len(command) == 6 and command[0] == 'move' and command[2] == 'from' and command[4] == 'to', \
        f"Instruction not understood, got: {rearrangement_str}"
    k = int(command[1])
    from_stack = int(command[3])
    to_stack = int(command[5])
    return move_item_from_stack_to_stack(stacks=stacks, from_stack=from_stack, to_stack=to_stack, k=k, multi_crate_mover=multi_crate_mover)

def execute_rearrangement_procedure(stacks: List[List[str]], rearrangement_procedure: Iterable[str], multi_crate_mover: bool = False) -> List[List[str]]:
    new_stacks = stacks
    for proc in rearrangement_procedure:
        new_stacks = execute_rearrangement(new_stacks, proc, multi_crate_mover)
    return new_stacks

def get_rearranged_stacks_from_lines(lines: Iterable[str], multi_crate_mover: bool = False) -> List[List[str]]:
    initial_configuration_lines, instruction_lines, indices = get_initial_configuration_and_instructions_from_lines(lines)
    initial_stacks = get_initial_stacks_from_config_lines(initial_configuration_lines, indices)
    final_stacks = execute_rearrangement_procedure(initial_stacks, instruction_lines, multi_crate_mover)
    return final_stacks

def get_top_crate_from_each_stack(stacks: List[List[str]]) -> str:
    top_crates = list()
    for stack in stacks:
        top_crates.append(stack[-1])
    return ''.join(top_crates)

def main():
    filepath = os.environ['CRATE_MANIFEST_FILE']
    assert pathlib.Path(filepath).exists(), f"Expected file to exist: {filepath}"
    with open(filepath, 'r') as f:
        lines = [line.rstrip() for line in f.readlines()]

    # part 1 - without multi-crate mover
    stacks = get_rearranged_stacks_from_lines(lines)
    top_crates = get_top_crate_from_each_stack(stacks)
    print(f"Top crates: {top_crates}")

    # part 2 - with multi crate mover
    stacks_multi = get_rearranged_stacks_from_lines(lines, multi_crate_mover=True)
    top_crates_multi = get_top_crate_from_each_stack(stacks_multi)
    print(f"Top crates (using multi-crate mover): {top_crates_multi}")

if __name__ == '__main__':
    main()
