import pytest
from day02 import tournament

sample_final_score = (
    ('A', 'Y', 8),
    ('B', 'X', 1),
    ('C', 'Z', 6),
)

@pytest.fixture
def sample_final_score_fx():
    return sample_final_score

sample_final_score_sneaky_strategy = (
    ('A', 'Y', 4),
    ('B', 'X', 1),
    ('C', 'Z', 7),
)

@pytest.fixture
def sample_final_score_sneaky_strategy_fx():
    return sample_final_score_sneaky_strategy

@pytest.fixture
def sample_rounds_file(tmpdir, sample_final_score_fx):
    file = tmpdir / 'rounds_sample.txt'
    to_write = '\n'.join(f"{line[0]} {line[1]}" for line in sample_final_score_fx)
    with open(file, 'w') as f:
        f.writelines(to_write)
    return file

@pytest.mark.parametrize(
    "them, us, expected_final_score", sample_final_score, ids=(f"{tc[0]}{tc[1]}" for tc in sample_final_score)
)
def test_final_score(them, us, expected_final_score):
    assert tournament.final_score[f"{them}{us}"] == expected_final_score

def test_total_final_score(sample_final_score_fx):
    rounds = ((s[0], s[1]) for s in sample_final_score_fx)
    assert tournament.total_final_score(rounds) == 15

def test_total_final_score_sneaky(sample_final_score_sneaky_strategy_fx):
    rounds = ((s[0], s[1]) for s in sample_final_score_sneaky_strategy_fx)
    assert tournament.total_final_score_sneaky(rounds) == 12

def test_rounds_from_file(sample_rounds_file):
    rounds = tournament.rounds_from_file(sample_rounds_file)
    assert rounds == [('A', 'Y'), ('B', 'X'), ('C', 'Z')]

def test_main(sample_rounds_file, monkeypatch, capsys):
    monkeypatch.setenv('TOURNAMENTS_FILE', str(sample_rounds_file))
    tournament.main()
    written_to_output = capsys.readouterr().out
    assert written_to_output == 'Score: 15\nSneaky score: 12\n'

@pytest.mark.parametrize(
    "them, desired_result, expected_final_score", sample_final_score_sneaky_strategy,
    ids=(f"{tc[0]}{tc[1]}" for tc in sample_final_score_sneaky_strategy)
)
def test_round_redirection_map(them, desired_result, expected_final_score):
    assert tournament.sneaky_final_score[f"{them}{desired_result}"] == expected_final_score
