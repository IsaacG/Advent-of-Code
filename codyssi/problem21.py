"""Codyssi Day N."""

import collections
import functools
import logging
import re

log = logging.info


def solve(part: int, data: str, test_number: int) -> int:
    """Solve the parts."""
    blocks = data.split("\n\n")
    moves = tuple(sorted(int(i) for i in blocks[1].split(" : ")[1].split(", ")))
    # If a third block is added, use that for the target part 3 rank.
    bisect_want = 100000000000000000000000000000
    if len(blocks) == 3:
        bisect_want = int(blocks[2])

    # Parse the stairs into a graph, mapping (from_floor, from_stair) to all possible (to_floor, to_stair) values.
    # The weight of every edge is 1.
    graph = collections.defaultdict(list)
    for line in blocks[0].splitlines():
        m = re.fullmatch(r"S(\d+) : (\d+) -> (\d+) : FROM (?:S(\d+)|START) TO (?:S(\d+)|END)", line)
        staircase, start, end, start_conn, end_conn = [int(i) if i else 0 for i in m.groups()]

        # Add an edge from every step in this staircase to the next step.
        for i in range(start, end):
            graph[staircase, i].append((staircase, i + 1))
        if staircase == 1:
            lowest_stair, highest_stair = start, end
            graph_start = (1, lowest_stair)
            graph_end = (1, highest_stair)
        else:
            # Add edges from one startcase to the other.
            graph[start_conn, start].append((staircase, start))
            graph[staircase, end].append((end_conn, end))
        # Part one ignore all other staircases after the first one.
        if part == 1:
            break

    @functools.cache
    def paths_to_end(from_position):
        """Return how many ways there are from this position until the end."""
        if from_position == graph_end:
            return 1
        options = possible_next_nodes(from_position)
        return sum((paths_to_end(option) for option in options), 0)

    @functools.cache
    def possible_next_nodes(from_position):
        """Return all possible next nodes with the different amounts of legal steps per move."""
        options = set()
        for move in moves:
            # Expand the steps taken based on how many positions can be moved in one move.
            positions = {from_position}
            for i in range(move):
                positions = {
                    i
                    for p in positions
                    for i in graph.get(p, [])
                }
            options.update(positions)
        return options

    def bisect(position, distance):
        """Return the path to a specific rank by sorting each next-node and tracking how many paths are down that way."""
        formatted_position = [f"S{position[0]}_{position[1]}"]
        if position == graph_end:
            return formatted_position

        # Find all possible next nodes.
        options = possible_next_nodes(position)
        # Find next nodes with how many paths to the end exist that way. Filter out nodes that won't land us at the end.
        weighted_options = [(o, paths_to_end(o)) for o in options if paths_to_end(o)]
        weighted_options.sort()
        # Count how many paths/ranks we skip until we get to a node that will lead us to our target rank.
        for option, paths in weighted_options:
            # Stop when we find a node that will hit our target rank.
            if distance + paths >= bisect_want:
                return formatted_position + bisect(option, distance)
            distance += paths
        # We cannot hit the target rank. Take the highest rank.
        option, weight = weighted_options[-1]
        return formatted_position + bisect(option, distance - weight)

    if part in [1, 2]:
        return paths_to_end(graph_start)
    return "-".join(bisect(graph_start, 0))


TEST_DATA = ["""\
S1 : 0 -> 6 : FROM START TO END
S2 : 2 -> 3 : FROM S1 TO S1

Possible Moves : 1, 3""",
    """\
S1 : 0 -> 6 : FROM START TO END
S2 : 2 -> 4 : FROM S1 TO S1
S3 : 3 -> 5 : FROM S2 TO S1

Possible Moves : 1, 2""",
    """\
S1 : 0 -> 99 : FROM START TO END
S2 : 8 -> 91 : FROM S1 TO S1
S3 : 82 -> 91 : FROM S1 TO S1
S4 : 90 -> 97 : FROM S2 TO S1
S5 : 29 -> 74 : FROM S1 TO S1
S6 : 87 -> 90 : FROM S3 TO S2
S7 : 37 -> 71 : FROM S2 TO S1
S8 : 88 -> 90 : FROM S6 TO S3
S9 : 34 -> 37 : FROM S2 TO S5
S10 : 13 -> 57 : FROM S1 TO S2

Possible Moves : 1, 3, 5, 6""",
]
TESTS = [
    (1, TEST_DATA[0], 6),
    (1, TEST_DATA[1], 13),
    (1, TEST_DATA[2], 231843173048269749794),
    (2, TEST_DATA[0], 17),
    (2, TEST_DATA[1], 102),
    (2, TEST_DATA[2], 113524314072255566781694),
    (3, TEST_DATA[0], "S1_0-S2_2-S2_3-S1_5-S1_6"),
    (3, TEST_DATA[1], "S1_0-S1_2-S2_3-S3_4-S3_5-S1_6"), # highest rank, 102
    (3, TEST_DATA[2], "S1_0-S1_6-S2_11-S2_17-S2_23-S2_29-S9_34-S9_37-S5_42-S5_48-S5_54-S5_60-S5_66-S5_72-S5_73-S5_74-S1_79-S3_84-S8_88-S8_89-S8_90-S3_90-S3_91-S1_96-S1_99"), # highest
    # Override the target rank.
    (3, TEST_DATA[1] + "\n\n" + "39", "S1_0-S1_1-S1_2-S2_3-S3_4-S3_5-S1_6"),
    (3, TEST_DATA[2] + "\n\n" + "73287437832782344", "S1_0-S1_1-S1_2-S1_3-S1_4-S1_5-S1_6-S1_7-S1_8-S1_9-S1_10-S1_11-S1_12-S1_13-S1_14-S1_15-S1_16-S1_17-S1_18-S1_19-S1_20-S1_21-S1_22-S1_23-S1_24-S1_25-S1_26-S1_29-S5_29-S5_30-S5_35-S5_36-S5_37-S5_38-S5_39-S5_40-S5_45-S5_46-S5_47-S5_48-S5_51-S5_52-S5_53-S5_54-S5_55-S5_58-S5_59-S5_62-S5_63-S5_64-S5_65-S5_66-S5_67-S5_70-S5_71-S5_72-S1_76-S1_79-S1_80-S3_84-S3_85-S3_86-S3_87-S3_90-S1_92-S1_93-S1_94-S1_95-S1_98-S1_99"),  # rank 73287437832782344
]
