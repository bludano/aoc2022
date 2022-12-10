import pytest
from day10 import signal
import textwrap

def sample():
    return textwrap.dedent("""\
        addx 15
        addx -11
        addx 6
        addx -3
        addx 5
        addx -1
        addx -8
        addx 13
        addx 4
        noop
        addx -1
        addx 5
        addx -1
        addx 5
        addx -1
        addx 5
        addx -1
        addx 5
        addx -1
        addx -35
        addx 1
        addx 24
        addx -19
        addx 1
        addx 16
        addx -11
        noop
        noop
        addx 21
        addx -15
        noop
        noop
        addx -3
        addx 9
        addx 1
        addx -3
        addx 8
        addx 1
        addx 5
        noop
        noop
        noop
        noop
        noop
        addx -36
        noop
        addx 1
        addx 7
        noop
        noop
        noop
        addx 2
        addx 6
        noop
        noop
        noop
        noop
        noop
        addx 1
        noop
        noop
        addx 7
        addx 1
        noop
        addx -13
        addx 13
        addx 7
        noop
        addx 1
        addx -33
        noop
        noop
        noop
        addx 2
        noop
        noop
        noop
        addx 8
        noop
        addx -1
        addx 2
        addx 1
        noop
        addx 17
        addx -9
        addx 1
        addx 1
        addx -3
        addx 11
        noop
        noop
        addx 1
        noop
        addx 1
        noop
        noop
        addx -13
        addx -19
        addx 1
        addx 3
        addx 26
        addx -30
        addx 12
        addx -1
        addx 3
        addx 1
        noop
        noop
        noop
        addx -9
        addx 18
        addx 1
        addx 2
        noop
        noop
        addx 9
        noop
        noop
        noop
        addx -1
        addx 2
        addx -37
        addx 1
        addx 3
        noop
        addx 15
        addx -21
        addx 22
        addx -6
        addx 1
        noop
        addx 2
        addx 1
        noop
        addx -10
        noop
        noop
        addx 20
        addx 1
        addx 2
        addx 2
        addx -6
        addx -11
        noop
        noop
        noop
    """)

@pytest.fixture
def sample_fx():
    return sample()

@pytest.fixture
def sample_file(sample_fx, tmpdir):
    fp = tmpdir / 'signal-file.txt'
    with open(fp, 'w') as f:
        f.write(sample_fx)
    return fp

executions_test_cases = (
    (20, 21),
    (60, 19),
    (100, 18),
    (140, 21),
    (180, 16),
    (220, 18),
)
@pytest.mark.parametrize(
    "expected_cycle_num, expected_register_val", executions_test_cases, ids=(e[0] for e in executions_test_cases)
)
def test_get_executions(sample_fx, expected_cycle_num, expected_register_val):
    # Arrange

    # Act
    executions = signal.get_executions(sample_fx.split('\n'))
    cycle_num, register_val = executions[expected_cycle_num - 1]

    # Assert
    assert cycle_num == expected_cycle_num
    assert register_val == expected_register_val

signal_strengths_test_cases = (
    (20, 420),
    (60, 1140),
    (100, 1800),
    (140, 2940),
    (180, 2880),
    (220, 3960),
)
@pytest.mark.parametrize(
    "expected_cycle_num, expected_signal_strength", signal_strengths_test_cases, ids=(e[0] for e in signal_strengths_test_cases)
)
def test_get_signal_strengths_from_executions(sample_fx, expected_cycle_num, expected_signal_strength):
    # Arrange
    executions = signal.get_executions(sample_fx.split('\n'))

    # Act
    signal_strengths = signal.get_signal_strengths_from_executions(executions)
    strength = signal_strengths[expected_cycle_num - 1]

    # Assert
    assert strength == expected_signal_strength

def test_get_pixels_from_executions(sample_fx):
    # Act
    executions = signal.get_executions(sample_fx.split('\n'))

    # Arrange
    pixels = signal.get_pixels_from_executions(executions)

    # Assert
    #assert 0

def test_main(sample_file, monkeypatch, capsys):
    monkeypatch.setenv('SIGNAL_FILE', str(sample_file))
    signal.main()
    written_to_output = capsys.readouterr().out
    assert written_to_output == 'Total signal strength: 13140\n##..##..##..##..##..##..##..##..##..##..\n###...###...###...###...###...###...###.\n####....####....####....####....####....\n#####.....#####.....#####.....#####.....\n######......######......######......####\n#######.......#######.......#######.....\n'
