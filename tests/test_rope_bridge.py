import pytest
import textwrap
from day9 import rope_bridge

def sample():
    return textwrap.dedent("""\
        R 4
        U 4
        L 3
        D 1
        R 4
        D 1
        L 5
        R 2
        """)

@pytest.fixture
def sample_fx():
    return sample()

@pytest.fixture
def sample_file(sample_fx, tmpdir):
    fp = tmpdir / 'motion-file.txt'
    with open(fp, 'w') as f:
        f.write(sample_fx)
    return fp

@pytest.fixture
def initial_motion_series():
    return rope_bridge.MotionSeries()

@pytest.mark.parametrize(
    "move,expected_new_head_position", (
        ("L", (-1, 0)),
        ("R", (1, 0)),
        ("U", (0, 1)),
        ("D", (0, -1)),
    ),
    ids=("L", "R", "U", "D")
)
def test_MotionSeries__move_head_once_from_initial_position_moves_head_to_correct_position(
    initial_motion_series: rope_bridge.MotionSeries,
    move,
    expected_new_head_position
):
    ms = initial_motion_series
    assert ms.current_head_position == (0, 0)
    ms._move_head_once(move)
    assert ms.current_head_position == expected_new_head_position

@pytest.mark.parametrize(
    "move,expected_new_tail_position", (
        zip(("L", "R", "U", "D"), ((0,0) for _ in range(4)))
    ),
    ids=("L", "R", "U", "D")
)
def test_MotionSeries__move_head_once_from_initial_position_keeps_tail_at_origin(
    initial_motion_series: rope_bridge.MotionSeries,
    move,
    expected_new_tail_position
):
    ms = initial_motion_series
    assert ms.current_head_position == (0, 0)
    assert ms._current_knot_position(-1) == (0, 0)
    ms._move_head_once(move)
    assert ms._current_knot_position(-1) == expected_new_tail_position

corrected_tail_position_test_cases = (
    ((0,0), (0,0), (0,0)),
    ((0,0), (0,1), (0,1)),
    ((15,5), (15,5), (15,5)),
    ((15,5), (15,7), (15,6)),
    ((15,5), (16,7), (15,6)),
    ((15,5), (17,7), (16,6)),
    ((-7,5), (-7,7), (-7,6)),
    ((-7,5), (-7,6), (-7,6)),
    ((-7,5), (-9,7), (-8,6)),
    ((-7,5), (-9,6), (-8,5)),
)
@pytest.mark.parametrize(
    "head_position, tail_position, expected_corrected_tail_position",
    corrected_tail_position_test_cases,
    ids=(f"{(tc[0], tc[1])}" for tc in corrected_tail_position_test_cases)
)
def test_MotionSeries__corrected_tail_position_returns_expected_position(
    initial_motion_series: rope_bridge.MotionSeries,
    head_position, tail_position, expected_corrected_tail_position
):
    ms = initial_motion_series
    corrected_tail_position = ms._corrected_tail_position(head_position, tail_position)
    assert corrected_tail_position == expected_corrected_tail_position

def test_execute_motions(sample_fx):
    lines = sample_fx.split('\n')
    ms = rope_bridge.execute_motions(lines)

def test_main(sample_file, monkeypatch, capsys):
    monkeypatch.setenv('MOTION_FILE', str(sample_file))
    rope_bridge.main()
    written_to_output = capsys.readouterr().out
    assert written_to_output == 'number of distinct positions visited by tail: 13\n' \
        'number of distinct positions visited by tail (10 knots): 1\n'
