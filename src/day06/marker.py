from typing import Union, TypeVar, Callable
import pathlib
import os

PathT = TypeVar('PathT', bound=pathlib.Path)

def make_marker_finder(num_distinct_characters: int) -> Callable[[str], int]:
    def finder(s: str) -> int:
        l = len(s)
        for i, _ in enumerate(s):
            if i > l - (num_distinct_characters-1):
                return -1
            cs = set(s[i:i+num_distinct_characters])
            if len(cs) == num_distinct_characters:
                return i+num_distinct_characters
    return finder

find_first_marker = make_marker_finder(4)
find_first_start_of_message_marker = make_marker_finder(14)

def get_signal_from_file(filepath: Union[PathT, str]) -> str:
    p = pathlib.Path(filepath)
    assert p.exists(), f"Expected file to exist: {filepath}"
    with open(p, 'r') as f:
        signal = f.read()
    return signal

def main():
    signal_file = os.environ['SIGNAL_FILE']
    signal = get_signal_from_file(signal_file)

    # part 1 - find first marker position
    first_marker_position = find_first_marker(signal)
    print(f"First marker found after position {first_marker_position}")

    # part 2 - find first start of message position
    first_start_of_message_position = find_first_start_of_message_marker(signal)
    print(f"First start-of-message marker found after position {first_start_of_message_position}")

if __name__ == '__main__':
    main()
