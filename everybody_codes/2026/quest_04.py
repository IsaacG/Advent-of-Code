"""Everyone Codes Event 2026 Day 4."""

import collections

from lib import helpers


def solve(part: int, data: list[int]) -> int:
    """Solve the parts."""
    # id, quest, part, time => data
    if part < 3:
        cumulative_time = collections.defaultdict(int)
        counts = collections.defaultdict(int)

        for id_, _, _, time in data:
            cumulative_time[id_] += time
            counts[id_] += 1
        places = sorted(cumulative_time, key=lambda x: (-counts[x], cumulative_time[x]))
        return sum(idx * cumulative_time[person] for idx, person in enumerate(places, 1))
    
    quests = sorted({quest for _, quest, _, _ in data})
    points = collections.defaultdict(int)
    for q in quests:
        cumulative_time = collections.defaultdict(int)
        parts = sorted({part for i, quest, part, time in data if quest == q})
        for p in parts:
            # Compute who completed the part and in how long.
            completed = set()
            for id_, quest, quest_part, time in data:
                if quest == q and quest_part == p:
                    cumulative_time[id_] += time
                    completed.add(id_)

            # Group by time to handle ties.
            times = collections.defaultdict(set)
            for i in completed:
                times[cumulative_time[i]].add(i)

            # Distribute the points based on rank.
            pot = p * 50
            for _, ids in sorted(times.items()):
                for i in ids:
                    points[i] += pot
                pot = max(0, pot - len(ids))

    # Group by points to sort and handle ties.
    by_points = collections.defaultdict(int)
    for i in points.values():
        by_points[i] += 1

    # Compute ranks and checksum.
    checksum = 0
    rank = 1
    for i in sorted(by_points, reverse=True):
        checksum += rank * i * by_points[i]
        rank += by_points[i]
    return checksum

if __name__ == "__main__":
    helpers.run_solution(globals())
