import pytest
from day11 import keep_away
import textwrap

def sample():
    return textwrap.dedent("""\
        Monkey 0:
        Starting items: 79, 98
        Operation: new = old * 19
        Test: divisible by 23
            If true: throw to monkey 2
            If false: throw to monkey 3

        Monkey 1:
        Starting items: 54, 65, 75, 74
        Operation: new = old + 6
        Test: divisible by 19
            If true: throw to monkey 2
            If false: throw to monkey 0

        Monkey 2:
        Starting items: 79, 60, 97
        Operation: new = old * old
        Test: divisible by 13
            If true: throw to monkey 1
            If false: throw to monkey 3

        Monkey 3:
        Starting items: 74
        Operation: new = old + 3
        Test: divisible by 17
            If true: throw to monkey 0
            If false: throw to monkey 1
    """)

@pytest.fixture
def sample_fx():
    return sample()

@pytest.fixture
def sample_file(tmpdir, sample_fx):
    fp = tmpdir / 'keep-away.txt'
    with open(fp, 'w') as f:
        f.write(sample_fx)
    return fp

def test_get_monkey_decisions_returns_correct_num_monkeys(sample_fx):
    # Arrange
    lines = sample_fx.split('\n')

    # Act
    monkeys = keep_away.get_monkey_decisions(lines)

    # Assert
    assert len(monkeys) == 4

@pytest.fixture
def monkey_decisions(sample_fx):
    lines = sample_fx.split('\n')
    return keep_away.get_monkey_decisions(lines)

execute_rounds_test_cases = (
    (1,
        (
            (0, [20, 23, 27, 26]),
            (1, [2080, 25, 167, 207, 401, 1046]),
            (2, []),
            (3, []),
        ),
        [2, 4, 3, 5]
    ),
    (4,
        (
            (0, [491, 9, 52, 97, 248, 34]),
            (1, [39, 45, 43, 258]),
            (2, []),
            (3, []),
        ),
        [16, 20, 4, 20]
    ),
    (20,
        (
            (0, [10, 12, 14, 26, 34]),
            (1, [245, 93, 53, 199, 115]),
            (2, []),
            (3, []),
        ),
        [101, 95, 7, 105]
    ),
)

@pytest.mark.parametrize(
    "num_rounds, expected_results, expected_inspections",
    execute_rounds_test_cases,
    ids=(str(tc[0]) for tc in execute_rounds_test_cases)
)
def test_execute_rounds_returns_expected_items(monkey_decisions, num_rounds, expected_results, expected_inspections):
    # Arrange
    lcm = keep_away.lcm_of_divisors(monkey_decisions)

    # Act
    after_rounds, _ = keep_away.execute_rounds(monkey_decisions, lcm=lcm, n=num_rounds)

    # Assert
    for mid, expected_items in expected_results:
        assert after_rounds[mid]['starting_items'] == expected_items

@pytest.mark.parametrize(
    "num_rounds, expected_results, expected_inspections",
    execute_rounds_test_cases,
    ids=(str(tc[0]) for tc in execute_rounds_test_cases)
)
def test_execute_rounds_returns_expected_inspections(monkey_decisions, num_rounds, expected_results, expected_inspections):
    # Arrange
    lcm = keep_away.lcm_of_divisors(monkey_decisions)

    # Act
    _, inspections = keep_away.execute_rounds(monkey_decisions, lcm=lcm, n=num_rounds)

    # Assert
    assert inspections == expected_inspections

def test_monkey_business_level(monkey_decisions):
    # Arrange
    lcm = keep_away.lcm_of_divisors(monkey_decisions)
    _, inspections = keep_away.execute_rounds(monkey_decisions, lcm=lcm, n=20)

    # Act
    mbl = keep_away.monkey_business_level(inspections)

    # Assert
    assert mbl == 10605

def test_main(monkeypatch, sample_file, capsys):
    monkeypatch.setenv('KEEP_AWAY_FILE', str(sample_file))
    keep_away.main()
    written_to_output = capsys.readouterr().out
    assert written_to_output == 'Monkey business level: 10605\nMonkey business level (maximum worry): 2713310158\n'
