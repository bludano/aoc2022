from typing import Tuple, List, Iterable
import os
import pathlib

class MotionSeries:

    @property
    def knots(self):
        return self._knots

    def _knot_positions_visited(self, knot_id: int) -> List[Tuple[int, int]]:
        return self.knots[knot_id]

    @property
    def head_positions_visited(self):
        return self._knot_positions_visited(knot_id=0)

    @property
    def tail_positions_visited(self):
        return self._knot_positions_visited(knot_id=-1)

    def _current_knot_position(self, knot_id: int) -> Tuple[int, int]:
        return self._knot_positions_visited(knot_id=knot_id)[-1]

    @property
    def current_head_position(self):
        return self._current_knot_position(knot_id=0)

    def __init__(self, num_knots: int = 2):
        self._num_knots = num_knots
        self._knots = list()
        for _ in range(num_knots):
            self._knots.append([(0, 0)])

    def move_head(self, direction: str, positions: int = 1) -> None:
        for _ in range(positions):
            self._move_head_once(direction)

    def _move_head_once(self, direction: str) -> None:
        accepted_directions = ('L', 'R', 'U', 'D')
        assert direction in accepted_directions, f"expected valid direction from {accepted_directions}, got {direction}"

        head_position_x, head_position_y = self.current_head_position

        # move head
        if direction == 'L':
            head_position_x -= 1
        elif direction == 'R':
            head_position_x += 1
        elif direction == 'U':
            head_position_y += 1
        elif direction == 'D':
            head_position_y -= 1
        else:
            raise RuntimeError(f'catch-all, direction: {direction}')

        new_leader_position = head_position_x, head_position_y
        for leader_knot_id in range(self._num_knots - 1):
            follower_knot_id = leader_knot_id + 1
            follower_position_pending_change = self._current_knot_position(follower_knot_id)
            new_follower_position = self._corrected_tail_position(new_leader_position, follower_position_pending_change)
            self._add_knot_position_visited(knot_id=leader_knot_id, position=new_leader_position)
            self._add_knot_position_visited(knot_id=follower_knot_id, position=new_follower_position)
            new_leader_position = new_follower_position

    def _add_knot_position_visited(self, knot_id: int, position: Tuple[int, int]) -> None:
        self._knots[knot_id].append(position)

    @staticmethod
    def _corrected_tail_position(current_head_position: Tuple[int, int], current_tail_position: Tuple[int, int]) -> Tuple[int, int]:
        current_head_position_x, current_head_position_y = current_head_position
        current_tail_position_x, current_tail_position_y = current_tail_position

        # recompute current coordinates, so head is positioned at the origin
        temp_head_position_x, temp_head_position_y = 0, 0
        delta_x = temp_head_position_x - current_head_position_x
        delta_y = temp_head_position_y - current_head_position_y
        temp_tail_position_x = current_tail_position_x + delta_x
        temp_tail_position_y = current_tail_position_y + delta_y

        if abs(temp_tail_position_x) in (0, 1) and abs(temp_tail_position_y) in (0, 1):
            # tail is already close enough, don't adjust
            return current_tail_position

        if abs(temp_tail_position_x) > 2 or abs(temp_tail_position_y) > 2:
            raise ValueError(f"Tail is too far away to be brought adjacent to head in one step --" \
                f" head position: {current_head_position}, tail position: {current_tail_position}")

        position_position_map = {
            (-2, -2): (-1, -1),
            (-2, -1): (-1 ,0),
            (-2, 0): (-1, 0),
            (-2, 1): (-1, 0),
            (-2, 2): (-1, 1),
            (-1, -2): (0, -1),
            (-1, 2): (0, 1),
            (0, -2): (0, -1),
            (0, 2): (0, 1),
            (1, -2): (0, -1),
            (1, 2): (0, 1),
            (2, -2): (1, -1),
            (2, -1): (1, 0),
            (2, 0): (1, 0),
            (2, 1): (1, 0),
            (2, 2): (1, 1),
        }
        adjusted_tail_position_x, adjusted_tail_position_y  = position_position_map[(temp_tail_position_x, temp_tail_position_y)]

        # recompute coordinates in original coordinate system
        return (adjusted_tail_position_x - delta_x, adjusted_tail_position_y - delta_y)

    def __repr__(self):
        return f"{self.__class__.__name__}(num_motions={len(self.head_positions_visited)})"

def execute_motions(lines: Iterable[str], num_knots: int = 2) -> MotionSeries:
    ms = MotionSeries(num_knots=num_knots)
    for line in lines:
        if line == '':
            continue
        direction, positions = line.split(' ')
        ms.move_head(direction, int(positions))
    return ms

def main():
    filepath = os.environ['MOTION_FILE']
    assert pathlib.Path(filepath).exists(), f"Want input, got {filepath}"
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # part 1
    ms = execute_motions(lines)
    positions_visited_by_tail = ms.tail_positions_visited
    distinct_positions_visited_by_tail = set(positions_visited_by_tail)
    print(f"number of distinct positions visited by tail: {len(distinct_positions_visited_by_tail)}")

    # part 2
    ms10 = execute_motions(lines, num_knots=10)
    positions_visited_by_tail_10 = ms10.tail_positions_visited
    distinct_positions_visited_by_tail_10 = set(positions_visited_by_tail_10)
    print(f"number of distinct positions visited by tail (10 knots): {len(distinct_positions_visited_by_tail_10)}")

if __name__ == '__main__':
    main()
