"""Everyone Codes Event 2026 Day N."""

import math
import heapq
import collections
import functools
import itertools
import logging
import platform
import z3

try:
    from lib import helpers
    from lib import parsers
except ModuleNotFoundError as e:
    if platform.python_implementation() != "PyPy":
        raise

log = logging.info

def solve(part: int, data: str, testing: bool) -> int:
    """Solve the parts."""
    if testing and part == 0:
        return 0

    mines = data.coords["@"]
    poi = mines | data.coords["S"] | data.coords["E"]
    space = data.coords["."] | poi
    start = data.coords["S"].copy().pop()
    end = data.coords["E"].copy().pop()

    @functools.cache
    def p1_distance(src, dst, incoming):
        q = collections.deque([(0, src, incoming)])
        seen = {}
        while q:
            steps, pos, incoming = q.popleft()
            steps += 1
            for n in helpers.neighbors_t(*pos):
                if n == dst:
                    return steps, pos
                if n in space and n != incoming and n not in seen:
                    q.append((steps, n, pos))


    @functools.cache
    def p1_solve_for(src, remaining, incoming):
        if not remaining:
            return p1_distance(src, end, incoming)[0]

        best = 1e100
        for i in remaining:
            d, via = p1_distance(src, i, incoming)
            cost = p1_solve_for(i, frozenset(remaining - {i}), via)
            best = min(best, d + cost)
        return best

    if part == 1:
        return p1_solve_for(start, frozenset(mines), None)

    needed_sulphur = 2026 if part == 2 else 202620262026

    start_x = start[0]
    center_y = start[1]
    end_x = end[0]

    forks = {x for x in range(start[0], end[0]) if (x, center_y + 1) in space}
    Loop = collections.namedtuple("Loop", "steps sulfur x1 x2 dy width height")
    half_loops = collections.defaultdict(list)
    exits = set()
    for x in sorted(forks):
        for dy in [-1, 1]:
            if (x, dy) in exits:
                continue
            min_y, max_y = 1e10, 0
            steps, sulfur = 0, 0
            direction = (0, dy)
            pos = (x, center_y)
            while not steps or pos[1] != center_y:
                for d in [direction, helpers.rotate_clockwise(*direction), helpers.rotate_counterclockwise(*direction)]:
                    n_pos = pos[0] + d[0], pos[1] + d[1]
                    direction = d
                    if n_pos in space:
                        break
                assert n_pos in space
                steps += 1
                pos = n_pos
                if pos in mines:
                    sulfur += 1
                min_y, max_y = min(min_y, pos[1]), max(max_y, pos[1])
            # print(x, min_y, max_y)
            if sulfur:
                half_loops[x].append(Loop(steps=steps, sulfur=sulfur, x1=x, x2=pos[0], dy=dy, width=pos[0] - x, height= max(max_y - center_y, center_y - min_y)))
            exits.add((pos[0], dy))
    grouped_half_loops = []
    todo = set(half_loops)
    while todo:
        first = min(todo)
        last = half_loops[first][0].x2
        group = {loop for x in todo for loop in half_loops[x] if x < last}
        grouped_half_loops.append(group)
        todo -= {loop.x1 for loop in group}

    grouped_full_loops = []
    for group in grouped_half_loops:
        loop_group = []
        for l in group:
            loop_group.append(Loop(steps=l.steps + l.width, sulfur=l.sulfur, x1=l.x1, x2=l.x1, dy=l.dy, width=l.width, height=l.height))
        for a, b in itertools.permutations(group, r=2):
            steps = a.steps + b.steps + abs(a.x2 - b.x2)
            loop_group.append(Loop(steps=steps, sulfur=a.sulfur + b.sulfur, x1=a.x1, x2=b.x1, dy=0, width=max(a.width, b.width), height=a.height + b.height))
        if False:
            for l in loop_group:
                print(l)
            print()
        grouped_full_loops.append(loop_group)

    best_loops = {}
    for group in grouped_full_loops:
        for l in group:
            steps = l.steps + abs(l.x1 - l.x2)
            if l.sulfur not in best_loops:
                best_loops[l.sulfur] = steps
            elif steps < best_loops[l.sulfur]:
                best_loops[l.sulfur] = steps

    best_loop = max((l for g in grouped_full_loops for l in g), key=lambda x: x.sulfur / (x.steps + abs(x.x1 - x.x2)))

    print(f"{best_loop=}")
    if False:
        # We never want to take a loop if l.sulfur >= best_loop.sulfur. That's not efficient.
        filtered_grouped_full_loops = []
        for group in grouped_full_loops:
            filtered_group = []
            for l in group:
                if l.sulfur < best_loop.sulfur:
                    filtered_group.append(l)
            filtered_grouped_full_loops.append(filtered_group)
        grouped_full_loops = filtered_grouped_full_loops

    loops_taken = needed_sulphur // best_loop.sulfur - 10
    steps_taken = loops_taken * (best_loop.steps + abs(best_loop.x1 - best_loop.x2))
    sulfur_taken = loops_taken * best_loop.sulfur

    loop_cap = math.ceil(needed_sulphur / best_loop.sulfur)
    step_cap = end_x - start_x + loop_cap * (best_loop.steps + abs(best_loop.x1 - best_loop.x2))
    if part == 3:
        step_cap += 1000

    log("Sulfur taken: %d", sulfur_taken)

    assert len(grouped_half_loops) == len(grouped_full_loops) == 3
    for gs in [grouped_half_loops, grouped_full_loops]:
        for g in gs:
            for l in g:
                assert l.sulfur > 0

    todo = [(steps_taken, sulfur_taken, 0, start[0])]
    ls = 0
    seen = {}
    while todo:
        steps, sulfur, group, x = heapq.heappop(todo)
        if ls < sulfur:
            ls = sulfur
            log("%d %d %d", ls, steps, len(todo))
        if x == end_x:
            assert sulfur >= needed_sulphur and part == 2 or sulfur == needed_sulphur
            return steps
        assert group < 3, f"{sulfur=}, {steps=}, {group=}, {x=}, {end_x=}"
        # Option 1: move straight to the next section.
        if group == 2:
            if sulfur >= needed_sulphur and part == 2 or sulfur == needed_sulphur:
                n_steps = steps + end_x - x
                if n_steps <= step_cap:
                    heapq.heappush(todo, (steps + end_x - x, sulfur, group + 1, end_x))
        else:
            heapq.heappush(todo, (steps, sulfur, group + 1, x))
        # Option 2: take a half-loop and move to the next section.
        for l in grouped_half_loops[group]:
            n_steps = steps + abs(x - l.x1) + l.steps
            n_x = l.x2
            n_sulfur = sulfur + l.sulfur
            if group == 2:
                if n_sulfur < needed_sulphur:
                    continue
                if part == 3 and n_sulfur != needed_sulphur:
                    continue
                n_steps += end_x - n_x
                n_x = end_x
            if n_sulfur <= step_cap:
                if seen.setdefault((n_sulfur, group + 1, n_x), n_steps + 1) > n_steps:
                    seen[n_sulfur, group + 1, n_x] = n_steps
                    heapq.heappush(todo, (n_steps, n_sulfur, group + 1, n_x))
        # Option 3: take a loop.
        if sulfur < needed_sulphur:
            for l in grouped_full_loops[group]:
                n_steps = steps + abs(x - l.x1) + l.steps
                n_x = l.x2
                n_sulfur = sulfur + l.sulfur
                if n_sulfur <= step_cap:
                    if part != 3 or n_sulfur <= needed_sulphur:
                        if seen.setdefault((n_sulfur, group, n_x), n_steps + 1) > n_steps:
                            seen[n_sulfur, group, n_x] = n_steps
                            heapq.heappush(todo, (n_steps, n_sulfur, group, n_x))
    return
                




    # Manually chart a course to the best loop (10 steps, 2 sulphur).
    # Pick up 4 sulphur on the way to/from the loop.
    # Loop 2026 - 4 times.
    assert start == (0, 11) and end == (93, 11)
    loop = [(36,13), (37,12)]
    wants = [(11,10), *loop, (72,13)]
    assert all(i in mines for i in wants)
    path = [start, *wants, end]
    total = 0
    for a, b in itertools.pairwise(path):
        d, _ = p1_distance(a, b, None)
        total += d

    loop_len = 0
    incoming = None
    for a, b in [loop, reversed(loop)]:
        d, incoming = p1_distance(a, b, incoming)
        loop_len += d
    loops_needed = (needed_sulphur - 4) // 2
    return total + loop_len * loops_needed

    needed_sulphur = 202620262026
    center = start[1]
    # All the x-values of a 4-way junction
    forks = [x for x in range(start[0], end[0]) if (x, start[1] + 1) in space]
    # Walk each half loop. Find the start/end, the number of steps and the number of sulphur.
    half_loops = {}
    ends = set()
    for x in forks:
        for dy in [-1, 1]:
            loop_start = (x, center + dy)
            pos = loop_start
            if pos in ends:
                continue
            sulphur = 0
            steps = 0
            prior = (x, center)
            while pos[1] != center:
                if pos in mines:
                    sulphur += 1
                steps += 1
                pos, prior = (set(helpers.neighbors_t(*pos)) - {prior} & space).pop(), pos
            ends.add(prior)
            width = prior[0] - loop_start[0] - 1
            extra_steps = steps - width  # cost of taking this detour vs going straight
            half_loops[loop_start] = (prior, sulphur, steps, extra_steps)

    # Group the loops into the three sections using a DSU.
    loop_groups = []
    for (x, y) in half_loops:
        for dx in [2, 3, 4]:
            if (x + dx, y) in half_loops:
                helpers.add_to_disjoint_sets(loop_groups, {(x, y), (x + dx, y)})
        if (x, y + 2) in half_loops:
            helpers.add_to_disjoint_sets(loop_groups, {(x, y), (x, y + 2)})

    # For each of the three sections, combine pairs of half loops to form full loops.
    full_loops = []
    for loop_group in loop_groups:
        for a, b in itertools.combinations(loop_group, r=2):
            steps = half_loops[a][2] + half_loops[b][2] + 2 + 2 * abs(a[0] - b[0])
            sulphur = half_loops[a][1] + half_loops[b][1]
            full_loops.append((a, b, steps, sulphur))

    # As we go from S to E, detour through the best half loop in each section
    best_half_loop = [
        max(loop_group, key=lambda x: half_loops[x][1] / half_loops[x][3])
        for loop_group in loop_groups
    ]
    half_detours = sum(half_loops[i][1] for i in best_half_loop)
    remaining = needed_sulphur - half_detours
    print(f"{half_detours=}")

    
    # Find the loop that yields the best sulphur per step. Use this loop to load up on sulphur.
    best = max(full_loops, key=lambda x: x[3] / x[2])
    loops_around = remaining // best[3]
    remaining = remaining - best[3] * loops_around
    print(f"{remaining=} after best loop")

    if False:
        min_extra = None
        for i in itertools.product(*loop_groups):
            i = list(i)
            s = sum(half_loops[j][1] for j in i)
            c = sum(half_loops[j][3] for j in i)
            if s == remaining and (min_extra is None or s < min_extra):
                min_extra = s

        steps = end[0] - start[0]
        steps += min_extra
        steps += best[2] * loops_around
        # assert steps not in {265502412385, 265502412305, 265502412292}
        # return steps

    hallways = [
        # sulphur, steps
        [(half_loops[i][1], half_loops[i][3]) for i in loop_group] + [(0, 0)]
        for loop_group in loop_groups
    ]
    full_loops = [(sulphur, steps) for a, b, steps, sulphur in full_loops]
    # Pick one from each of the three hallways plus n each of loops.
    ns = [z3.Int(f"{i}") for i in range(len(full_loops))]

    best = None
    for i in itertools.product(*hallways):
        i = list(i)
        sulphur = sum(sulphur for sulphur, steps in i)
        hl_steps = sum(steps for sulphur, steps in i)
        t = needed_sulphur - sulphur
        print(needed_sulphur, sulphur, t)
        steps = z3.Int("steps")

        opt = z3.Optimize()
        opt.add(t == z3.Sum(n * fl[0] for n, fl in zip(ns, full_loops)))
        opt.add(steps == z3.Sum(n * fl[1] for n, fl in zip(ns, full_loops)))
        opt.minimize(steps)
        if opt.check() == z3.sat:
            print(opt.model()[steps])
    










# PARSER = parsers.parse_one_str
TEST_DATA = [
    "The examples do not play nice",
]
TESTS = [
    (1, TEST_DATA[0], 0),
    # (2, TEST_DATA[0], 0),
    # (3, TEST_DATA[0], 0),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
