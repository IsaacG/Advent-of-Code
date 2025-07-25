#!/bin/python

import pathlib
import string
import sys

import click
import logic_mill


def letter_mark():
    """Generate state logic to wrap `w` and `ch` in `[]`.

    There are 31 chars to track that all need their own states.
    Auto-generate those state rules.

    Strategy:
    * Begin at start of word.
    * Add an `=` at the end and return to start.
    * Check the letter. Erase. If it's anything other than `c`, change to state $letter.
    * If the letter is `c`, go to MAYBE-CH. Then on the next letter, check for h and go to output-c or output-ch.
    * On state $letter, go to the end, skip a space, then output the letter. For `w`, output `[w]`.
    """
    letters = set(string.ascii_lowercase + "-äöõü")
    extras = set("[]=")
    rules = []
    # Move to the end.
    rules += [f"INIT {letter} INIT {letter} R" for letter in letters]
    # Add a `=` then return to start.
    rules += ["INIT _ GO_START = L"]
    rules += [f"GO_START {letter} GO_START {letter} L" for letter in letters | extras]
    rules += ["GO_START _ START _ R"]
    # Once at the start, copy letter to state.
    rules += [f"START {letter} COPY_{letter} _ R" for letter in letters - {"c"}]
    # `c` gets special handling to detect `ch`.
    rules += ["START c MAYBE_c _ R"]
    rules += ["MAYBE_c h COPY_ch _ R"]
    rules += [f"MAYBE_c {letter} COPY_c {letter} R" for letter in (letters | extras) - {"h"}]
    # Go to the end so we can output the copy.
    rules += [f"COPY_{letter} {other} COPY_{letter} {other} R" for letter in letters | {"ch"} for other in letters | extras]
    # Output the letter then return. `w` and `ch` get special handling.
    rules += [f"COPY_{letter} _ GO_START {letter} L" for letter in letters - {"w"}]
    rules += [
        # `w` => `[w]`
        "COPY_w _ COPY_w1 [ R",
        "COPY_w1 _ COPY_] w R",
        # `ch` => `[ch]`
        "COPY_ch _ COPY_ch1 [ R",
        "COPY_ch1 _ COPY_ch2 c R",
        "COPY_ch2 _ COPY_] h R",
        "COPY_] _ GO_START ] L",
    ]
    # End of input
    rules += ["START = HALT _ R"]
    return "\n".join(rules)


def text_mirror():
    """Generate state logic to reverse text.

    There are 31 chars to track that all need their own states.
    Auto-generate those state rules.

    Strategy:
    * Add a `=` before the word.
    * Copy letter into state. Tombstone letter with `!`.
    * Write letter to the left of the `=`.
    * Return to next letter.
    """
    letters = set(string.ascii_lowercase + "-äöõü")
    extras = set("!=")
    rules = []
    # Add a `=` then find the first letter.
    rules += [f"INIT {letter} ADD_EQ {letter} L" for letter in letters]
    rules += ["ADD_EQ _ F = R"]
    rules += ["FIND_LETTER ! FIND_LETTER ! R"]
    # Copy and tombstone.
    rules += [f"FIND_LETTER {letter} COPY_{letter} ! R" for letter in letters]
    rules += [f"COPY_{i} {j} COPY_{i}{j} ! L" for i in letters for j in letters | {"_"}]
    rules += [f"COPY_{i}{j} {k} COPY_{i}{j} {k} L" for i in letters for j in letters | {"_"} for k in letters | extras]
    # Found an opening. Record letter then return to the start.
    rules += [f"COPY_{i}{j} _ PAST_{j} {i} L" for i in letters for j in letters | {"_"}]
    rules += [f"PAST_{i} _ GO_EQ {i} R" for i in letters | {"_"}]
    rules += [f"GO_EQ {letter} GO_EQ {letter} R" for letter in letters]
    rules += ["GO_EQ = FIND_LETTER = R"]
    # Once there is nothing left to copy, clean up tombstones.
    rules += [
        "FIND_LETTER _ CLEANUP _ L",
        "CLEANUP ! CLEANUP _ L",
        "CLEANUP = HALT _ L",
    ]

    return "\n".join(rules).replace("FIND_LETTER", "F").replace("COPY_", "C")


def index():
    general = """
INIT       | START      _ R   // Start by dropping the leading `|`. At start of to-remove count.
START      | GO_LIST    _ R   // Go to the list
GO_LIST    | GO_LIST    | R   //
GO_LIST    : GO_FIRST   : R   // In the list. Go to the first number.
GO_FIRST   x GO_FIRST   x R   //
GO_FIRST   | RM_FIRST   x R   // Drop the first number.
RM_FIRST   | RM_FIRST   x R   //
RM_FIRST   , RETURN_I   x L   // Return to the start.
RETURN_I   x RETURN_I   x L   //
RETURN_I   : RETURN_I   : L   //
RETURN_I   | RETURN_I   | L   //
RETURN_I   _ START      _ R   // Got back to the index.
START      : CLEAN_PRE  _ R   // Out of index values. Tidy up before the first element.
CLEAN_PRE  x CLEAN_PRE  _ R   //
CLEAN_PRE  | CLEAN_PRE  | R   // Skip the first element.
CLEAN_PRE  , CLEAN_POST _ R   // Clean remaining elements.
CLEAN_PRE  _ HALT       _ R   // No following items.
CLEAN_POST | CLEAN_POST _ R   //
CLEAN_POST , CLEAN_POST _ R   //
CLEAN_POST _ HALT       _ L   //
"""
    states = 100
    rules = []
    rules += [ "INIT        |  DROP_0      _   R"]
    rules += [f"DROP_{n}      |  DROP_{n+1}      _   R" for n in range(states)]
    rules += [f"DROP_{n}      :  FIND_RM_{n}   _   R" for n in range(states)]
    rules += [f"FIND_RM_0     |  SKIP          |   R"]
    rules += [f"FIND_RM_{n} |  FIND_RM_{n} _   R" for n in range(1, states)]
    rules += [f"FIND_RM_{n+1}   ,  FIND_RM_{n}   _   R" for n in range(1, states)]

    rules += [ "FIND_RM_1   ,  SKIP  _   R"]
    rules += [ "SKIP        |  SKIP        |   R"]
    rules += [ "SKIP        ,  TRIM        _   R"]
    rules += [ "SKIP        _  HALT        _   R"]
    rules += [ "TRIM        _  HALT        _   R"]
    rules += [ "TRIM        ,  TRIM        _   R"]
    rules += [ "TRIM        |  TRIM        _   R"]

    return "\n".join(rules)

def unary_compare():
    """Generate state logic for unary compare.

    General solution:
    Mark `|` as "read" by changing to "x". Read one `|` from both `a` and `b` until one runs out.
    Once one runs out, update the `,` to the result and replace `x` with `|`.
    For minimal steps, start at the `,` and work our way outwards.

    Limited solution: use the state as a counter. Increment on left. Decrement on right.
    """
    general = """
INIT       |  INIT        |  R   // Start at the `,`.
INIT       ,  FIND_LEFT   ,  L   // Look for a left `|`.
FIND_LEFT  x  FIND_LEFT   x  L   //
FIND_LEFT  ,  FIND_LEFT   ,  L   //
FIND_LEFT  _  EQ_OR_LT    _  R   // Ran out of `|` on the left. Check if there is any right left. Either `=` or `<`.
FIND_LEFT  |  FIND_RIGHT  x  R   // Look for a matching right `|`.
FIND_RIGHT x  FIND_RIGHT  x  R   //
FIND_RIGHT ,  FIND_RIGHT  ,  R   //
FIND_RIGHT |  FIND_LEFT   x  L   // Matched. Go back to a left.
FIND_RIGHT _  SET_GT      _  L   // Ran out of `|` on the right. We found one on the left so the left is larger (`>`).
EQ_OR_LT   x  EQ_OR_LT    x  R   // Go to the right to check if it is `=` or `<`.
EQ_OR_LT   ,  EQ_OR_LT    ,  R   // Go to the right to check if it is `=` or `<`.
EQ_OR_LT   |  SET_LT      |  L   // Right has more, ie is bigger. Set `<`.
EQ_OR_LT   _  SET_EQ      _  L   // Right has same. Set `=`.
SET_GT     |  SET_GT      |  L   // Clean up the data.
SET_LT     |  SET_LT      |  L
SET_EQ     |  SET_EQ      |  L
SET_GT     x  SET_GT      |  L
SET_LT     x  SET_LT      |  L
SET_EQ     x  SET_EQ      |  L
SET_GT     ,  SET_GT      >  L
SET_LT     ,  SET_LT      <  L
SET_EQ     ,  SET_EQ      =  L
SET_GT     _  HALT        _  R
SET_LT     _  HALT        _  R
SET_EQ     _  HALT        _  R
"""
    # This can be made shorter by guessing a result on the first pass over the `,`.
    # If the `,` is replaced with `>` on the first pass and `>` turns out to be correct,
    # we can halt without needing to return and update.
    # Try all combinations of guesses for the smallest step count.
    guess = ">"
    rules = []
    # Count the left.
    rules += ["INIT     |   L1   |   R"]
    rules += [f"L{i}     |   L{i + 1}   |   R" for i in range(1, 300)]
    # Switch to the right.
    rules += [f"L{i}     ,   R{i}   {guess}   R" for i in range(1, 300)]
    # Decrement.
    rules += [f"R{i}     |   R{i - 1}   |   R" for i in range(1, 300)]
    # End comparison.
    # Hit zero, still more on right. Right bigger.
    if guess == "<":
        rules += ["R0       |   HALT       |   L"]
    else:
        rules += ["R0       |   SET_<      |   L"]
    # Hit zero, no more on right. Right equal.
    if guess == "=":
        rules += ["R0       _   HALT      _   L"]
    else:
        rules += ["R0       _   SET_=      _   L"]
    # Ran out on the right but did not hit zero. Left bigger.
    if guess == ">":
        rules += [f"R{i}     _   HALT      _   L" for i in range(1, 300)]
    else:
        rules += [f"R{i}     _   SET_>      _   L" for i in range(1, 300)]
    # Return to `,` and update.
    rules += [f"SET_{i}  |   SET_{i}    |   L" for i in "><="]
    rules += [f"SET_{i}  {guess}   HALT       {i} L" for i in "><="]
    return "\n".join(rules)


def line_count():
    letters = set(string.ascii_lowercase + "-äöõü")
    rules = [
        f"INIT {i} INIT ! R" for i in letters
    ] + [
        f"INIT  + ADD   +  L",
        f"ADD   ! ADD   !  L",
        f"ADD   _ RET   |  R",
        f"ADD   | INC   |  R",
        f"INC   ! RET   |  R",
        f"RET   ! RET   !  R",
        f"RET   + INIT  !  R",
        f"INIT  _ CLEAN _  L",
        f"CLEAN ! CLEAN _  L",
        f"CLEAN _ HALT  |  R",
        f"CLEAN | END   |  R",
        f"END   _ HALT  |  R",
    ]
    return "\n".join(rules)

SOLUTIONS = [
    """
// Move to the right. Replace + with |.
INIT | M _ R
M | M | R
M + HALT | R
""",
    # even or odd
    """
// Move left to right, tracking even or odd, and clearing bits.
// When we get to the end, write the state.
INIT | O _ R
O | E _ R
E | O _ R
O _ HALT O R
E _ HALT E R
""",
    """
INIT   1   GO_END   1   R
INIT   0   HALT     1   R
GO_END 1   GO_END   1   R
GO_END 0   GO_END   0   R
// Work right to left, incrementing and tracking a carry bit. "CARRY" means add one.
GO_END _   CARRY    _   L
CARRY  0   HALT     1   L
CARRY  1   CARRY    0   L
CARRY  _   HALT     1   L
""",
    # Unary multiplication a*b can be done by copying the "b" value "a" times.
    # We can do something "a" times by removing one `|` from `a` after each operation.
    # We can copy `b` by looking for a `|`, going to the end and adding a `|` then returning to replace the `|` with another char.
    # Repeat until all `|` are changed, then reset.
    #
    # Start state: reduce `a` by one `|`. Move past `*`. Change to copy mode.
    # Copy mode: change first `|` in `b` to `T`. Move to result. Write `|`. Return to first `|` of `b`. Done copying.
    # Done copying: reset `b` and return to initial state.
    """
INIT      | START     | L   // Change to start and shift left.
START     _ START     _ R   // Move to first | of a.
START     | GO_COPY   _ R   // Reduce `a` by one. Go copy `b`.
GO_COPY   | GO_COPY   | R   // Look for start of `b`.
GO_COPY   * COPY      * R   // Start copying `b`.
COPY      | GO_END_B  T R   // Mark a `|` from `b` as copied. Now go add it to the result.
GO_END_B  | GO_END_B  | R   // Find the end of `b`.
GO_END_B  _ GO_END_C  _ R   // Find the end of `c`.
GO_END_C  | GO_END_C  | R   // Find the end of `b`.
GO_END_C  _ RET_TO_B  | L   // Add one to `c`.
RET_TO_B  | RET_TO_B  | L   // Return to the first `|` of `b`.
RET_TO_B  _ RET_TO_B  _ L   // Return to the first `|` of `b`.
RET_TO_B  T COPY      T R   // Return to the first `|` of `b`.
COPY      _ RESET_B   _ L   // Trying to copy from `b` got got a `_`: all done copying `b`. Reset `b`.
RESET_B   T RESET_B   | L   // Reset `b`.
RESET_B   * RET_TO_A  * L   // Done resetting `b`. Return to start of `a`.
RET_TO_A  | RET_TO_A  | L   // Done resetting `b`. Return to start of `a`.
RET_TO_A  _ START     _ R   // Back at the start of `a`.
START     * RM_B      _ R   // Trying to reduce `a` but out of `|`: all done copying. Drop `b` from output.
RM_B      | RM_B      _ R   // Trying to reduce `a` but out of `|`: all done copying. Drop `b` from output.
RM_B      _ HALT      _ R   // Done removing `b`. Multiplication completed.
    """,
    # Unary index. Minus one index. For each index `|`, remove an element from the array.
    # When we run out of index `|`, remove everything after the first number.
    index(),
    # Subtract. `a-b`. Go to end of b. Remove one from `b`. Move to `a`. Replace one with `x`. Return to end of b.
    # Once `b` is gone, drop `-` and `x`.
    """
INIT      | INIT       | R   // Go to the end.
INIT      - INIT       - R   //
INIT      x INIT       x R   //
INIT      _ BEGIN      _ L   // At end of `b`.
BEGIN     | GO_SIGN    _ L   // Drop one from `b`. Find `-`.
GO_SIGN   | GO_SIGN    | L   //
GO_SIGN   - GO_ONE     - L   // Find a value to drop from `a`.
GO_ONE    x GO_ONE     x L   //
GO_ONE    | INIT       x R   // Drop one from `a`. Return to end.
BEGIN     - CLEAN      _ L   // No more `b`. Tidy up.
CLEAN     x CLEAN      _ L
CLEAN     | HALT       | R
CLEAN     _ HALT       _ R
""",
    letter_mark(),
    text_mirror(),
    unary_compare(),
    line_count(),
]

TESTS = [
    [
        (  "|+|",   "||"),  # 1+1=2
        ("||+||", "||||"),  # 2+2=4
    ],
    [
        ( "||", "E"),
        ("|||", "O"),
    ],
    [
        (  "1",  "10"),  # 1+1=2
        ( "10",  "11"),  # 2+1=3
        ( "11", "100"),  # 3+1=4
        ("100", "101"),  # 4+1=5
        ("11010101", "11010110"),
    ],
    [
        (   "|*||",        "||"),  # 1x2=2
        (  "||*||",      "||||"),  # 2x2=4
        ( "||*|||",    "||||||"),  # 2x3=6
        ("|||*|||", "|||||||||"),  # 3x3=9
    ],
    [
        ("|:|||,|||||,||||||||,||||", "|||"),
        ("||:|||,|||||,||||||||,||||", "|||||"),
        ("||||:|||,|||||,||||||||,||||", "||||"),
    ],
    [
        ("|||||-||", "|||"),  # 5-2=3
        (   "||-||",    ""),  # 2-2=0
    ],
    [
        ("wõta-wastu-mu-soow-ja-chillitse-toomemäel", "[w]õta-[w]astu-mu-soo[w]-ja-[ch]illitse-toomemäel"),
    ],
    [
        ("hello-world", "dlrow-olleh"),
    ],
    [
        ("|||,||||", "|||<||||"),  # 3 > 4
        ("||||,|||", "||||>|||"),  # 4 > 3
        ( "|||,|||",  "|||=|||"),  # 3 = 3
        ( "||||||||||,|||",  "||||||||||>|||"),
    ],
    [
        ("hello+world+how-are-you", "|||"),
        ("hello", "|"),
    ],
]


def run_tests(puzzle: int) -> None:
    program = SOLUTIONS[puzzle - 1]
    tests = TESTS[puzzle - 1]
    transition_rules = logic_mill.parse_transition_rules(program)
    mill = logic_mill.LogicMill(transition_rules)
    for idx, (data, want) in enumerate(tests):
        result, steps = mill.run(data, verbose=False)
        if result == want:
            print(f"{puzzle:>2}.t{idx}: PASS")
        else:
            result, steps = mill.run(data, verbose=True)
            raise RuntimeError(f"{puzzle}.t{idx}: FAIL")


@click.command()
@click.option("-d", "puzzle", type=int, help="Puzzle number")
@click.option("--out", type=click.Path(path_type=pathlib.Path), required=False)
def main(puzzle: int, out: pathlib.Path | None) -> None:
    if puzzle == 0:
        for i in range(1, len(SOLUTIONS) + 1):
            run_tests(i)
    elif puzzle is None:
        run_tests(len(SOLUTIONS))
    else:
        run_tests(puzzle)
    if out:
        out.write_text(SOLUTIONS[puzzle])


if __name__ == "__main__":
    main()
