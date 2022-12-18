from typing import Tuple, Iterable, MutableSet, Optional
import os
import pathlib
import itertools
import collections

def adjacent(c0: Tuple[int, int, int], c1: Tuple[int, int, int]) -> bool:
    """Test whether two coordinates are adjacent - differ by exactly one coordinate"""
    if c0 == c1:
        return False
    matching_coords = 0
    neighbour_coords = 0
    for this, that in zip(c0, c1):
        if this == that:
            matching_coords += 1
        elif abs(this-that) == 1:
            neighbour_coords += 1
    return matching_coords == 2 and neighbour_coords == 1

def adjacent_coordinates(coord: Tuple[int, int, int]) -> Iterable[Tuple[int, int, int]]:
    x_, y_, z_ = coord
    return (
        (x, y, z)
        for x in range(x_-1,x_+2)
        for y in range(y_-1,y_+2)
        for z in range(z_-1,z_+2)
        if adjacent((x, y, z), coord)
    )

def number_of_adjacencies_in_set(s: MutableSet[Tuple[int, int, int]]) -> int:
    c = 0
    for cube in s:
        adj_coords = adjacent_coordinates(cube)
        for coord in adj_coords:
            if coord in s:
                c += 1
    return c

def total_surface_area_of_set(s: MutableSet[Tuple[int, int, int]]) -> int:
    return (6 * len(s)) - number_of_adjacencies_in_set(s)

def interior_space_of_set(s: MutableSet[Tuple[int, int, int]]) -> MutableSet[Tuple[int, int, int]]:
    """Given coordinates for a set of cubes, return 
    a set of coordinates interior within that set, regardless of whether that space has a cube in the input set
    """
    min_x = min(c[0] for c in s)
    min_y = min(c[1] for c in s)
    min_z = min(c[2] for c in s)
    max_x = max(c[0] for c in s)
    max_y = max(c[1] for c in s)
    max_z = max(c[2] for c in s)
    return set(itertools.product(range(min_x+1,max_x), range(min_y+1,max_y), range(min_z+1,max_z)))

def interior_missing_cubes(s: MutableSet[Tuple[int, int, int]]) -> MutableSet[Tuple[int, int, int]]:
    return interior_space_of_set(s) - s

def trapped(cube: Tuple[int, int, int], s: MutableSet[Tuple[int, int, int]]) -> bool:
    """Iteratively check neighbours of the current cube to see if there's a route to the exterior"""
    min_x = min(c[0] for c in s)
    min_y = min(c[1] for c in s)
    min_z = min(c[2] for c in s)
    max_x = max(c[0] for c in s)
    max_y = max(c[1] for c in s)
    max_z = max(c[2] for c in s)
    q = collections.deque([cube])
    visited = set()
    while q:
        c = q.popleft()
        x, y, z = c
        if c in s or c in visited: # this isn't a route out, or we've already covered this route
            continue
        if x<min_x or x>max_x or y<min_y or y>max_y or z<min_z or z>max_z:
            return False
        visited.add(c)
        for neighbour in (
            (x, y, z-1),
            (x, y, z+1),
            (x, y-1, z),
            (x, y+1, z),
            (x-1, y, z),
            (x+1, y, z)
        ):
            q.append(neighbour)
    return True

def trapped_cubes(s: MutableSet[Tuple[int, int, int]]) -> MutableSet[Tuple[int, int, int]]:
    missing_cubes = interior_missing_cubes(s)
    trapped_cubes = set()
    for mc in missing_cubes:
        if trapped(mc, s):
            trapped_cubes.add(mc)
    return trapped_cubes

def coords_from_lines(lines: Iterable[str]) -> MutableSet[Tuple[int, int, int]]:
    cubes = set()
    for line in lines:
        if not line in ('', '\n'):
            line = line.rstrip()
            coords = line.split(',')
            coords = tuple(int(c) for c in coords)
            cubes.add(coords)
    return cubes

def main():
    input_file = os.environ['CUBE_INPUT_FILE']
    assert pathlib.Path(input_file).exists(), f"Want input, got {input_file}"
    with open(input_file, 'r') as f:
        lines = f.readlines()
    cubes = coords_from_lines(lines)

    # part 1 - total surface area of cubes
    surface_area = total_surface_area_of_set(cubes)
    print(f"Part 1 - surface area: {surface_area}")

    # part 2 - total exterior surface area of cubes
    trapped_cubes_ = trapped_cubes(cubes)
    interior_surface_area = total_surface_area_of_set(trapped_cubes_)
    exterior_surface_area = surface_area - interior_surface_area
    print(f"Part 2 - exterior surface area: {exterior_surface_area}")

if __name__ == '__main__':
    main()
