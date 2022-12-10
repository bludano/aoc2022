from typing import Iterable, Tuple, List
import os
import pathlib

def get_executions(lines: Iterable[str]) -> Iterable[Tuple[int, int]]:
    executions: List[Tuple[int, int]] = list()
    accepted_ops = ('noop', 'addx')
    cycle_num = 0
    register_val = 1
    for line in lines:
        if line == '':
            continue
        parts = line.split(' ')
        op, *val = parts
        assert op in accepted_ops, f"Expected op from {accepted_ops}, got {op}"
        if op == 'noop':
            cycle_num += 1
            execution = cycle_num, register_val
            executions.append(execution)
        elif op == 'addx':
            for _ in range(2):
                cycle_num += 1
                execution = cycle_num, register_val
                executions.append(execution)
            register_val += int(val[0])
    return executions

def get_signal_strengths_from_executions(executions: Iterable[Tuple[int, int]]) -> Iterable[int]:
    signal_strengths = list()
    for cycle_num, register_val in executions:
        signal_strength = cycle_num * register_val
        signal_strengths.append(signal_strength)
    return signal_strengths

def get_interesting_signal_strengths(signal_strengths: Iterable[int]) -> Iterable[int]:
    def is_interesting_index(i) -> bool:
        return (i % 40) - 20 == -1
    def is_interesting_strength(execution: Tuple[int, int]):
        cycle_num, register_val = execution
        return is_interesting_index(cycle_num)
    return map(lambda x: (x[0]+1, x[1]), filter(is_interesting_strength, enumerate(signal_strengths)))

def get_pixels_from_executions(executions: Iterable[Tuple[int, int]]) -> Iterable[str]:
    pixels = list()
    for current_pixel, e in enumerate(executions):
        _, register_val_ = e
        this_line_current_pixel = current_pixel % 40
        register_val = register_val_ - 1
        sprite_position = tuple(range(register_val, register_val+3))
        #breakpoint()
        if this_line_current_pixel in sprite_position:
            pixel = '#'
        else:
            pixel = '.'
        pixels.append(pixel)
    return pixels

def main():
    filepath = os.environ['SIGNAL_FILE']
    assert pathlib.Path(filepath).exists(), f"Want input, got {filepath}"
    with open(filepath, 'r') as f:
        lines = f.read().split('\n')

    executions = get_executions(lines)

    # part 1
    strengths = get_signal_strengths_from_executions(executions)
    interesting_strengths = get_interesting_signal_strengths(strengths)
    tot_signal_strength = sum(strength for cycle_num, strength in interesting_strengths)
    print(f"Total signal strength: {tot_signal_strength}")

    # part 2
    pixels = get_pixels_from_executions(get_executions(lines))
    #assert 0
    num_pixels = len(pixels)
    num_output_lines = num_pixels // 40
    output_lines = list()
    for output_line in range(num_output_lines):
        output_line = ''.join(pixels[output_line*40:(output_line*40)+40])
        output_lines.append(output_line)
    final_output_lines = '\n'.join(output_lines)
    print(final_output_lines)

if __name__ == '__main__':
    main()
