"""Everyone Codes Event 2026 Day 7."""

import collections
import logging
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str, testing: bool) -> int:
    """Solve the parts."""
    limit = 100 if testing else 1000000
    start_strength = 5 if part == 1 else 10

    energy = {}
    connections = {}
    for cloud, _energy, *_conns in data:
        connections[cloud] = _conns
        energy[cloud] = _energy

    def compute_energy(start, energy):
        pulses = {start: {start_strength: 1}}
        exploded = set()

        while pulses:
            next_pulses = collections.defaultdict(lambda: collections.defaultdict(int))
            for cloud, pulse_data in pulses.items():
                if cloud in exploded:
                    continue
                for strength, pulse_count in pulse_data.items():
                    energy[cloud] += strength * pulse_count
                    if strength:
                        for next_cloud in connections[cloud]:
                            next_pulses[next_cloud][strength - 1] += pulse_count
            pulses = next_pulses
            if part == 3:
                explodes = {cloud for cloud, e in energy.items() if e >= limit and cloud not in exploded}
                exploded.update(explodes)
                for cloud in explodes:
                    for next_cloud in connections[cloud]:
                        pulses[next_cloud][10] += 1

        return sum(e for c, e in energy.items() if c not in exploded)

    if part < 3:
        start = max(connections, key=lambda x: len(connections[x]))
        return compute_energy(start, energy.copy())
    return max(compute_energy(start, energy.copy()) for start in connections)


PARSER = parsers.parse_ints


if __name__ == "__main__":
    helpers.run_solution(globals())
