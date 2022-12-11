from typing import Iterable, Tuple, Union, TypeVar
import pathlib
import os

PathT = TypeVar('PathT', bound=pathlib.Path)

my_selection_score = dict(X=1, Y=2, Z=3)

round_score = dict(AX=3, BX=0, CX=6, AY=6, BY=3, CY=0, AZ=0, BZ=6, CZ=3)

final_score = {
    k: round_score[k] + my_selection_score[k[-1]]
    for k in round_score
}

# X: I want to lose
# Y: I want to draw
# Z: I want to win
round_redirection_map = dict(AX='AZ', BX='BX', CX='CY', AY='AX', BY='BY', CY='CZ', AZ='AY', BZ='BZ', CZ='CX')
sneaky_final_score = {
    k: round_score[round_redirection_map[k]] + my_selection_score[round_redirection_map[k][-1]]
    for k in round_redirection_map
}

def total_final_score(rounds: Iterable[Tuple[str, str]]) -> int:
    return sum(final_score[f"{round[0]}{round[1]}"] for round in rounds)

def total_final_score_sneaky(rounds: Iterable[Tuple[str, str]]) -> int:
    return sum(sneaky_final_score[f"{round[0]}{round[1]}"] for round in rounds)

def rounds_from_file(filepath: Union[PathT, str]) -> Iterable[Tuple[str, str]]:
    p = pathlib.Path(filepath)
    assert p.exists(), f"Expected file containing rounds, got {p}"
    with open(p, 'r') as f:
        lines = [tuple(line.rstrip().split(' ')) for line in f.readlines()]
    return lines

def main():
    file = os.environ['TOURNAMENTS_FILE']
    rounds = rounds_from_file(file)

    # part 1 - assume X, Y, Z specify my response
    score = total_final_score(rounds)
    print(f"Score: {score}")

    # part 2 - X, Y, Z specify whether we want to lose, draw, or win
    sneaky_score = total_final_score_sneaky(rounds)
    print(f"Sneaky score: {sneaky_score}")

if __name__ == '__main__':
    main()
