"""Everyone Codes Event 2026 Day 17."""

from lib import helpers


DIRECTIONS = {
    (1, 0): ((0, 1), helpers.rotate_clockwise, helpers.rotate_counterclockwise),
    (0, 1): ((1, 0), helpers.rotate_counterclockwise, helpers.rotate_clockwise),
}

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    solid_floor = data.coords["#"]
    start = min(solid_floor)
    end = max(solid_floor)

    # BFS, track steps
    if part == 1:
        todo = [(0, start)]
        seen = {start}
        while todo:
            steps, pos = todo.pop(0)
            if pos == end:
                return steps
            steps += 1
            for neighbor in helpers.neighbors_t(*pos):
                if neighbor not in seen and neighbor in solid_floor:
                    todo.append((steps, neighbor))
                    seen.add(neighbor)

    def walls_for(direction: tuple[int, int], end_dir: tuple[int, int], r1, r2, end: tuple[int, int]) -> int:
        pos = start
        wall_count = 0
        while True:
            direction = r1(*direction)
            while True:
                neighbor = (pos[0] + direction[0], pos[1] + direction[1])
                if wall_count and pos == end:
                    if direction == end_dir:
                        return wall_count
                if neighbor in solid_floor:
                    break
                direction = r2(*direction)
                wall_count += 1
            pos = neighbor

    if part == 2:
        return walls_for((1, 0), (0, -1), helpers.rotate_clockwise, helpers.rotate_counterclockwise, start)

    return min(walls_for(d, *i, end) for d, i in DIRECTIONS.items())


if __name__ == "__main__":
    helpers.run_solution(globals())
