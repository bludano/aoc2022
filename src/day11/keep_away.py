from typing import Iterable, Tuple, List, Dict, Any
import copy
import os
import pathlib
import math
import functools

def get_monkey_decisions(lines: Iterable[str]) -> Dict[int, Dict[str, Any]]:
    """Parse inputs"""
    monkeys = dict()
    starting_items = list()
    monkey_id = -1
    operation = ""
    test_divisor = 0
    true_throw_monkey_id = -1
    false_throw_monkey_id = -1
    for i, line in enumerate(lines):
        line = line.lstrip()
        if line == '':
            monkey_id += 1
            monkeys[monkey_id] = {
                'starting_items': starting_items,
                'operation': operation,
                'test_divisor': test_divisor,
                'true_throw_monkey_id': true_throw_monkey_id,
                'false_throw_monkey_id': false_throw_monkey_id,
            }
            starting_items = list()
            operation = ""
            test_divisor = 0
            true_throw_monkey_id = -1
            false_throw_monkey_id = -1
        elif line.find('Monkey') > -1:
            pass
        elif line.find('Starting') > -1:
            line_ = line[len('Starting items: '):]
            for item in line_.split(','):
                item = int(item)
                starting_items.append(item)
        elif line.find('Operation') > -1:
            operation = line[len('Operation: new = '):]
        elif line.find('Test') > -1:
            test_divisor = int(line[len('Test: divisible by '):])
        elif line.find('true') > -1:
            true_throw_monkey_id = int(line[len('If true: throw to monkey '):])
        elif line.find('false') > -1:
            false_throw_monkey_id = int(line[len('If false: throw to monkey '):])
        else:
            raise NotImplementedError(f"Unexpected line type at line {i}: {line}")
    if operation != '': # end of file without blank line
        monkey_id += 1
        monkeys[monkey_id] = {
            'starting_items': starting_items,
            'operation': operation,
            'test_divisor': test_divisor,
            'true_throw_monkey_id': true_throw_monkey_id,
            'false_throw_monkey_id': false_throw_monkey_id,
        }
    return monkeys

def lcm_of_divisors(monkeys: Dict[int, Dict[str, Any]]) -> int:
    divisors = [m['test_divisor'] for m in monkeys.values()]
    return functools.reduce(lambda x,y: x*y, divisors, 1)

def execute_rounds(monkeys: Dict[int, Dict[str, Any]], lcm: int, n: int = 1, worry_level_divisor: int = 3) -> Tuple[Dict[int, Dict[str, Any]], List[int]]:
    monkeys = copy.deepcopy(monkeys)
    monkey_ids = monkeys.keys()
    items_inspected = list(0 for _ in range(len(monkey_ids)))
    for _ in range(n):
        for monkey_id in monkey_ids:
            m = monkeys[monkey_id]
            items_inspected[monkey_id] += len(m['starting_items'])
            for item in m['starting_items']:
                new: int
                old: int = item
                new = eval(m['operation'])
                new = new % lcm
                new = new // worry_level_divisor
                test_divisor = m['test_divisor']
                if new % test_divisor == 0:
                    throw_to_monkey_id = m['true_throw_monkey_id']
                else:
                    throw_to_monkey_id = m['false_throw_monkey_id']
                #new = math.gcd(new, test_divisor)
                monkeys[throw_to_monkey_id]['starting_items'].append(new)
            m['starting_items'] = list()
    return monkeys, items_inspected

def monkey_business_level(items_inspected: List[int]) -> int:
    insps = sorted(items_inspected, reverse=True)
    return insps[0] * insps[1]

def main():
    filepath = os.environ['KEEP_AWAY_FILE']
    assert pathlib.Path(filepath).exists(), f"Wamt input, got {filepath}"
    with open(filepath, 'r') as f:
        lines = f.read().split('\n')
    monkeys = get_monkey_decisions(lines)
    lcm = lcm_of_divisors(monkeys)

    # part 1
    _, inspections = execute_rounds(monkeys=monkeys, lcm=lcm, n=20)
    mbl = monkey_business_level(inspections)
    print(f"Monkey business level: {mbl}")

    # part 2
    _, inspections = execute_rounds(monkeys=monkeys, lcm=lcm, n=10000, worry_level_divisor=1)
    mbl = monkey_business_level(inspections)
    print(f"Monkey business level (maximum worry): {mbl}")

if __name__ == '__main__':
    main()