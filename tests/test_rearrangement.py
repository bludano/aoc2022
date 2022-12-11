import pytest
import textwrap
from day05 import rearrangement

@pytest.fixture
def sample():
    return textwrap.dedent("""\
            [D]    
        [N] [C]    
        [Z] [M] [P]
         1   2   3 

        move 1 from 2 to 1
        move 3 from 1 to 3
        move 2 from 2 to 1
        move 1 from 1 to 2
    """)

@pytest.fixture
def sample_manifest_file(sample, tmpdir):
    filepath = tmpdir / 'sample-manifest-file.txt'
    with open(filepath, 'w') as f:
        f.write(sample)
    return filepath

def test_get_initial_configuration_and_instructions_from_lines(sample):
    lines = rearrangement.get_lines_from_text(sample)
    initial_configuration_lines, instruction_lines, indices = rearrangement.get_initial_configuration_and_instructions_from_lines(lines)
    assert indices == [1, 5, 9]

@pytest.fixture
def sample_initial_config(sample):
    lines = rearrangement.get_lines_from_text(sample)
    initial_configuration_lines, _, indices = rearrangement.get_initial_configuration_and_instructions_from_lines(lines)
    return initial_configuration_lines, indices
    
def test_get_initial_stacks_from_config_lines(sample_initial_config):
    initial_configuration_lines, indices = sample_initial_config
    initial_stacks = rearrangement.get_initial_stacks_from_config_lines(initial_configuration_lines, indices)
    assert initial_stacks == [['Z', 'N'], ['M', 'C', 'D'], ['P']]

@pytest.mark.parametrize(
    "initial_stacks, from_stack, to_stack, k, expected_final_stacks", (
        ([['A', 'B', 'C'], ['D', 'E']], 1, 2, 1, [['A', 'B'], ['D', 'E', 'C']]),
        ([['A', 'B', 'C'], ['D', 'E'], ['F', 'G']], 3, 1, 1, [['A', 'B', 'C', 'G'], ['D', 'E'], ['F']]),
        ([['A', 'B', 'C'], ['D', 'E']], 1, 2, 3, [[], ['D', 'E', 'C', 'B', 'A']]),
    )
)
def test_move_item_from_stack_to_stack(initial_stacks, from_stack, to_stack, k, expected_final_stacks):
    new_stacks = rearrangement.move_item_from_stack_to_stack(initial_stacks, from_stack, to_stack, k=k)
    assert new_stacks == expected_final_stacks

@pytest.mark.parametrize(
    "initial_stacks, from_stack, to_stack, k, expected_final_stacks", (
        ([['A', 'B', 'C'], ['D', 'E']], 1, 2, 1, [['A', 'B'], ['D', 'E', 'C']]),
        ([['A', 'B', 'C'], ['D', 'E'], ['F', 'G']], 3, 1, 1, [['A', 'B', 'C', 'G'], ['D', 'E'], ['F']]),
        ([['A', 'B', 'C'], ['D', 'E']], 1, 2, 3, [[], ['D', 'E', 'A', 'B', 'C']]),
    )
)
def test_move_item_from_stack_to_stack_multi_crate_mover(initial_stacks, from_stack, to_stack, k, expected_final_stacks):
    new_stacks = rearrangement.move_item_from_stack_to_stack(initial_stacks, from_stack, to_stack, k=k, multi_crate_mover=True)
    assert new_stacks == expected_final_stacks

@pytest.mark.parametrize(
    "initial_stacks, rearrangement_str, expected_final_stacks", (
        ([['A', 'B', 'C'], ['D', 'E']], 'move 1 from 1 to 2', [['A', 'B'], ['D', 'E', 'C']]),
        ([['A', 'B', 'C'], ['D', 'E'], ['F', 'G']], 'move 1 from 3 to 1', [['A', 'B', 'C', 'G'], ['D', 'E'], ['F']]),
        ([['A', 'B', 'C'], ['D', 'E']], 'move 3 from 1 to 2', [[], ['D', 'E', 'C', 'B', 'A']]),
    )
)
def test_execute_rearrangement(initial_stacks, rearrangement_str, expected_final_stacks):
    new_stacks = rearrangement.execute_rearrangement(stacks=initial_stacks, rearrangement_str=rearrangement_str)
    assert new_stacks == expected_final_stacks

@pytest.mark.parametrize(
    "initial_stacks, rearrangement_procedure, expected_final_stacks", (
        ([['A', 'B', 'C'], ['D', 'E']], ['move 1 from 1 to 2'], [['A', 'B'], ['D', 'E', 'C']]),
        ([['A', 'B', 'C'], ['D', 'E'], ['F', 'G']], ['move 1 from 3 to 1', 'move 1 from 2 to 3'], [['A', 'B', 'C', 'G'], ['D'], ['F', 'E']]),
        ([['A', 'B', 'C'], ['D', 'E']], ['move 3 from 1 to 2', 'move 1 from 2 to 1'], [['A'], ['D', 'E', 'C', 'B']]),
    )
)
def test_execute_rearrangement_procedure(initial_stacks, rearrangement_procedure, expected_final_stacks):
    new_stacks = rearrangement.execute_rearrangement_procedure(initial_stacks, rearrangement_procedure)
    assert new_stacks == expected_final_stacks

def test_get_rearranged_stacks_from_lines(sample):
    lines = rearrangement.get_lines_from_text(sample)
    new_stacks = rearrangement.get_rearranged_stacks_from_lines(lines)
    assert new_stacks == [['C'], ['M'], ['P', 'D', 'N', 'Z']]

def test_get_top_crate_from_each_stack(sample):
    lines = rearrangement.get_lines_from_text(sample)
    new_stacks = rearrangement.get_rearranged_stacks_from_lines(lines)
    top_crates = rearrangement.get_top_crate_from_each_stack(new_stacks)
    assert top_crates == 'CMZ'

def test_main(monkeypatch, sample_manifest_file, capsys):
    monkeypatch.setenv('CRATE_MANIFEST_FILE', str(sample_manifest_file))
    rearrangement.main()
    written_to_output = capsys.readouterr().out
    assert written_to_output == 'Top crates: CMZ\nTop crates (using multi-crate mover): MCD\n'
