#!/bin/python

import pathlib
import string
import sys
import typing

import click
import logic_mill

INIT = "INIT"
HALT = "HALT"
R    = "R"
L    = "L"


class RuleSet:

    def __init__(self):
        self.rules = []

    def add(
        self,
        start: str,
        inp: str | int,
        end: str,
        out: str | int,
        direction: str,
        **fmt: dict[str, typing.Iterable[str | int]],
    ) -> None:
        """Add a new rule, with format support."""
        rule = f"{start} {inp} {end} {out} {direction}"
        if not fmt:
            self.rules.append(rule)
            return
        rules = [string.Template(rule)]
        for key, vals in fmt.items():
            rules = [string.Template(r.safe_substitute(**{key: val})) for val in vals for r in rules]
        self.rules.extend(r.substitute() for r in rules)

    def right(self, start: str, inp: str | int, **fmt: typing.Iterable[str | int]) -> None:
        """Add a rule where the state and tape do not change."""
        self.add(start, inp, start, inp, R, **fmt)

    def left(self, start: str, inp: str | int, **fmt: typing.Iterable[str | int]) -> None:
        """Add a rule where the state and tape do not change."""
        self.add(start, inp, start, inp, L, **fmt)

    def __str__(self) -> str:
        return "\n".join(self.rules)


def unary_addition() -> RuleSet:
    # 1. Unary Addition
    r = RuleSet()
    # Erase the first | so we can replace the + with |
    r.add(INIT, "|", "M", "_", R)
    # Go to the + then replace it.
    r.right("M", "|")
    r.add("M", "+", HALT, "|", R)
    return r


def unary_even_odd() -> RuleSet:
    # 2. Unary Even Odd
    r = RuleSet()
    # Move left to right, tracking even or odd, and clearing bits.
    # When we get to the end, write the state.
    r.add(INIT,  "|",  "O",  "_", R)
    r.add( "E",  "|",  "O",  "_", R)
    r.add( "O",  "|",  "E",  "_", R)
    r.add("$i",  "_", HALT, "$i", R, i="EO")
    return r


def binary_increment() -> RuleSet:
    # 3. Binary Increment
    r = RuleSet()
    r.add(    INIT,   0,     HALT,   1, R)
    r.add(    INIT,   1, "GO_END",   1, R)
    r.right("GO_END",   "$i", i="01")
    # Work right to left, incrementing and tracking a carry bit. "CARRY" means add one.
    r.add("GO_END", "_",  "CARRY", "_", L)
    r.add( "CARRY",   0,     HALT,   1, L)
    r.add( "CARRY",   1,  "CARRY",   0, L)
    r.add( "CARRY", "_",     HALT,   1, L)
    return r


def unary_multiplication() -> RuleSet:
    # 4. Unary Multiplication
    # Unary multiplication a*b can be done by copying the "b" value "a" times.
    # We can do something "a" times by removing one `|` from `a` after each operation.
    # We can copy `b` by looking for a `|`, going to the end and adding a `|` then returning to replace the `|` with another char.
    # Repeat until all `|` are changed, then reset.
    #
    # Start state: reduce `a` by one `|`. Move past `*`. Change to copy mode.
    # Copy mode: change first `|` in `b` to `T`. Move to result. Write `|`. Return to first `|` of `b`. Done copying.
    # Done copying: reset `b` and return to initial state.
    r = RuleSet()
    # Change to start and shift left.
    r.add(INIT, "|", "START", "|", L)
    # Move to first | of a.
    r.right("START", "_")
    # Reduce `a` by one. Go copy `b`.
    r.add("START", "|", "GO_COPY", "_", R)
    # Look for start of `b`.
    r.right("GO_COPY", "|")
    # Start copying `b`.
    r.add("GO_COPY", "*", "COPY", "*", R)
    # Mark a `|` from `b` as copied. Now go add it to the result.
    r.add("COPY", "|", "GO_END_B", "T", R)
    # Find the end of `b`.
    r.right("GO_END_B", "|")
    # Find the end of `c`.
    r.add("GO_END_B", "_", "GO_END_C", "_", R)
    # Find the end of `b`.
    r.right("GO_END_C", "|")
    # Add one to `c`.
    r.add("GO_END_C", "_", "RET_TO_B", "|", L)
    # Return to the first `|` of `b`.
    r.left("RET_TO_B", "$i", i="|_")
    # Return to the first `|` of `b`.
    r.add("RET_TO_B", "T", "COPY", "T", R)
    # Trying to copy from `b` got got a `_`: all done copying `b`. Reset `b`.
    r.add("COPY", "_", "RESET_B", "_", L)
    # Reset `b`.
    r.add("RESET_B", "T", "RESET_B", "|", L)
    # Done resetting `b`. Return to start of `a`.
    r.add("RESET_B", "*", "RET_TO_A", "*", L)
    # Done resetting `b`. Return to start of `a`.
    r.left("RET_TO_A", "|")
    # Back at the start of `a`.
    r.add("RET_TO_A", "_", "START", "_", R)
    # Trying to reduce `a` but out of `|`: all done copying. Drop `b` from output.
    r.add("START", "*", "RM_B", "_", R)
    # Trying to reduce `a` but out of `|`: all done copying. Drop `b` from output.
    r.add("RM_B", "|", "RM_B", "_", R)
    # Done removing `b`. Multiplication completed.
    r.add("RM_B", "_", HALT, "_", R)
    return r


def find_element_in_unary_array():
    # 5. Find Element in Unary Array
    # Unary index. Minus one index. For each index `|`, remove an element from the array.
    # When we run out of index `|`, remove everything after the first number.
    # == General Solution ==
    r = RuleSet()
    # Start by dropping the leading `|`. At start of to-remove count.
    r.add("INIT", "|", "START", "_", "R")
    # Go to the list
    r.add("START", "|", "GO_LIST", "_", "R")
    r.add("GO_LIST", "|", "GO_LIST", "|", "R")
    # In the list. Go to the first number.
    r.add("GO_LIST", ":", "GO_FIRST", ":", "R")
    r.add("GO_FIRST", "x", "GO_FIRST", "x", "R")
    # Drop the first number.
    r.add("GO_FIRST", "|", "RM_FIRST", "x", "R")
    r.add("RM_FIRST", "|", "RM_FIRST", "x", "R")
    # Return to the start.
    r.add("RM_FIRST", ",", "RETURN_I", "x", "L")
    r.add("RETURN_I", "x", "RETURN_I", "x", "L")
    r.add("RETURN_I", ":", "RETURN_I", ":", "L")
    r.add("RETURN_I", "|", "RETURN_I", "|", "L")
    # Got back to the index.
    r.add("RETURN_I", "_", "START", "_", "R")
    # Out of index values. Tidy up before the first element.
    r.add("START", ":", "CLEAN_PRE", "_", "R")
    r.add("CLEAN_PRE", "x", "CLEAN_PRE", "_", "R")
    # Skip the first element.
    r.add("CLEAN_PRE", "|", "CLEAN_PRE", "|", "R")
    # Clean remaining elements.
    r.add("CLEAN_PRE", ",", "CLEAN_POST", "_", "R")
    # No following items.
    r.add("CLEAN_PRE", "_", "HALT", "_", "R")
    r.add("CLEAN_POST", "|", "CLEAN_POST", "_", "R")
    r.add("CLEAN_POST", ",", "CLEAN_POST", "_", "R")
    r.add("CLEAN_POST", "_", "HALT", "_", "L")
    # return r

    # == Non-general solution ==
    r = RuleSet()
    states = 100
    rules = []
    r.add(INIT, "|", "DROP_0", "_", R)
    for n in range(states):
        r.add(f"DROP_{n}", "|",  f"DROP_{n+1}", "_", R)
        r.add(f"DROP_{n}", ":", f"FIND_RM_{n}", "_", R)
    r.add("FIND_RM_0", "|", "SKIP", "|", R)
    for n in range(1, states):
        r.add(f"FIND_RM_{n}",   "|", f"FIND_RM_{n}", "_", R)
        r.add(f"FIND_RM_{n+1}", ",", f"FIND_RM_{n}", "_", R)

    r.add("FIND_RM_1", ",", "SKIP", "_", R)
    r.right("SKIP", "|")
    r.add("SKIP", ",", "TRIM", "_", R)
    r.add("SKIP", "_", "HALT", "_", R)
    r.add("TRIM", "_", "HALT", "_", R)
    r.add("TRIM", ",", "TRIM", "_", R)
    r.add("TRIM", "|", "TRIM", "_", R)
    return r


def unary_subtraction() -> RuleSet:
    # 6. Unary Subtraction
    # Subtract. `a-b`. Go to end of b. Remove one from `b`. Move to `a`. Replace one with `x`. Return to end of b.
    # Once `b` is gone, drop `-` and `x`.
    r = RuleSet()
    # Go to the end.
    r.right(INIT, "$i", i="|-x")
    # At end of `b`.
    r.add(INIT, "_", "BEGIN", "_", L)
    # Drop one from `b`. Find `-`.
    r.add("BEGIN", "|", "GO_SIGN", "_", L)
    r.left("GO_SIGN", "|")
    # Find a value to drop from `a`.
    r.add("GO_SIGN", "-", "GO_ONE", "-", L)
    r.add("GO_ONE", "x", "GO_ONE", "x", L)
    # Drop one from `a`. Return to end.
    r.add("GO_ONE", "|", "INIT", "x", R)
    # No more `b`. Tidy up.
    r.add("BEGIN", "-", "CLEAN", "_", L)
    r.add("CLEAN", "x", "CLEAN", "_", L)
    r.add("CLEAN", "$i", HALT, "$i", R, i="|_")
    return r


def letter_mark():
    # 7. Letter Mark
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


def decimal_increment():
    rules = [
        f"INIT     {i}       INIT     {i}  R" for i in range(10)
    ] + [
        f"INIT       _        INC       _  L",
    ] + [
        # Increment 0-8 and end, no carry.
        f"INC      {i}       HALT {i + 1}  R" for i in range(9)
    ] + [
        f"INC        9        INC       0  L",
        f"INC        _       HALT       1  R",
    ]
    return "\n".join(rules)


def decimal_addition():
    rules = [
        f"INIT     {i}       INIT     {i}  L" for i in string.digits
    ] + [
        f"INIT       _       GET_A      =  R"
    ] + [
        f"GET_A    {i}       GET_A    {i}  R" for i in string.digits + "="
    ] + [
        f"GET_A_C    {i}       GET_A_C    {i}  R" for i in string.digits + "="
    ] + [
        f"GET_A      +       PICK_A     +  L",
        f"GET_A      |       PICK_A     |  L",
        f"PICK_A     |       PICK_A     |  L",
        f"GET_A_C    +       PICK_A_C   +  L",
        f"GET_A_C    |       PICK_A_C   |  L",
        f"PICK_A_C   |       PICK_A_C   |  L",
    ] + [
        f"PICK_A   {i}       GO_B{i}    |  R" for i in range(10)
    ] + [
        f"PICK_A_C   {i}       GO_B{i+1}    |  R" for i in range(10)
    ] + [
        f"PICK_A       =       COPY      =  R",
        f"PICK_A_C     =       GO_B1     =  R"
    ] + [
        f"GO_B{i}    |       GO_B{i}    |  R" for i in range(11)
    ] + [
        f"GO_B{i}    +       GET_B{i}  +  R" for i in range(11)
    ] + [
        f"GET_B{i} {j}      GET_B{i} {j} R" for i in range(11) for j in range(10)
    ] + [
        f"GET_B{i}  _       PICK_B{i}  _ L" for i in range(11)
    ] + [
        f"PICK_B{i}  {j}      ADD{int(i)+int(j)}    _ L" for i in range(11) for j in string.digits
    ] + [
        f"PICK_B{i}    +      COPY_{i}              _ L" for i in range(11)
    ] + [
        f"ADD{i}  {j}      ADD{i}    {j} L" for i in range(20) for j in string.digits + "|+="
    ] + [
        f"ADD{i}    _      GET_A     {i % 10} R" for i in range(10)
    ] + [
        f"ADD{i}    _      GET_A_C     {i % 10} R" for i in range(10, 20)
    ] + [
        f"COPY    {i}      COPY     {i}    R" for i in string.digits + "|+="
    ] + [
        f"COPY_C  {i}      COPY_C   {i}    R" for i in string.digits + "|+="
    ] + [
        f"COPY      _      COPY_G     _    L",
        f"COPY_C    _      COPY_C_G   _    L",
        f"COPY_G    =      HALT       _    L",
        f"COPY_C_G  =      COPY_1     =    L",
    ] + [
        f"COPY_G  {i}      COPY_G     _    L" for i in "_|+"
    ] + [
        f"COPY_C_G {i}     COPY_C_G   _    L" for i in "_|+"
    ] + [
        f"COPY_G  {i}      COPY_{i}   _    L" for i in range(10)
    ] + [
        f"COPY_C_G {i}     COPY_{i+1}   _    L" for i in range(10)
    ] + [
        f"COPY_{i} {j}     COPY_{i}  {j}   L" for i in range(11) for j in string.digits + "|+="
    ] + [
        f"COPY_{i}  _      COPY      {i}   R" for i in range(10)
    ] + [
        f"COPY_{10} _      COPY_C      0   R"
    ] + [
    ]
    return "\n".join(rules)


SOLUTIONS = [
    unary_addition(),
    unary_even_odd(),
    binary_increment(),
    unary_multiplication(),
    find_element_in_unary_array(),
    unary_subtraction(),
    letter_mark(),
    text_mirror(),
    unary_compare(),
    line_count(),
    decimal_increment(),
    decimal_addition(),
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
    [(str(i), str(i + 1)) for i in range(0, 111, 7)],
    [
        (f"{i}+{j}", f"{i+j}") for i, j in [
            (1, 2), (19, 82), (888, 9999999), (999999, 4444)
        ]
    ]
]


def run_tests(puzzle: int) -> None:
    program = str(SOLUTIONS[puzzle - 1])
    tests = TESTS[puzzle - 1]
    transition_rules = logic_mill.parse_transition_rules(program)
    mill = logic_mill.LogicMill(transition_rules)
    for idx, (data, want) in enumerate(tests):
        result, steps = mill.run(data, verbose=False)
        if result == want:
            print(f"{puzzle:>2}.t{idx:<2} PASS")
        else:
            result, steps = mill.run(data, verbose=True)
            raise RuntimeError(f"{puzzle}.t{idx}: FAIL")


@click.command()
@click.option("-d", "puzzle", type=int, help="Puzzle number")
@click.option("--out", type=click.Path(path_type=pathlib.Path), required=False)
def main(puzzle: int, out: pathlib.Path | None) -> None:
    if puzzle is None:
        puzzle = len(SOLUTIONS)
    if puzzle == 0:
        for i in range(1, len(SOLUTIONS) + 1):
            run_tests(i)
        return
    run_tests(puzzle)
    if out:
        out.write_text(str(SOLUTIONS[puzzle - 1]))


if __name__ == "__main__":
    main()
