import pytest
from day6 import marker

_test_cases = (
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5, 23),
    ("nppdvjthqldpwncqszvftbrmjlhg", 6, 23),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10, 29),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11, 26),
)

find_first_marker_tcs = tuple(
    (tc[0], tc[1]) for tc in _test_cases
)

@pytest.mark.parametrize(
    "s, expected_first_marker_position", find_first_marker_tcs,
    ids=(tc[0] for tc in find_first_marker_tcs)
)
def test_find_first_marker(s, expected_first_marker_position):
    assert marker.find_first_marker(s) == expected_first_marker_position

find_first_start_of_message_marker_tcs = tuple(
    (tc[0], tc[2]) for tc in _test_cases
)

@pytest.mark.parametrize(
    "s, expected_first_start_of_message_marker_position", find_first_start_of_message_marker_tcs,
    ids=(tc[0] for tc in find_first_marker_tcs)
)
def test_find_first_start_of_message_marker(s, expected_first_start_of_message_marker_position):
    assert marker.find_first_start_of_message_marker(s) == expected_first_start_of_message_marker_position

@pytest.fixture
def signal_file(tmpdir):
    fp = tmpdir / 'signal_file.txt'
    with open(fp, 'w') as f:
        f.write(find_first_marker_tcs[0][0])
    return fp

def test_get_signal_from_file(signal_file):
    assert marker.get_signal_from_file(signal_file) == find_first_marker_tcs[0][0]

def test_main(signal_file, monkeypatch, capsys):
    monkeypatch.setenv('SIGNAL_FILE', str(signal_file))
    marker.main()
    written_to_output = capsys.readouterr().out
    assert written_to_output == 'First marker found after position 5\nFirst start-of-message marker found after position 23\n'
