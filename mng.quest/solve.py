#!/bin/python
from __future__ import annotations

import collections
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

    def __init__(self, puzzle: int, tests: list[tuple[str, str]] | None = None):
        self.rules = []
        self.tests = []
        self.puzzle = puzzle
        self.states = set()
        for test in tests or []:
            self.test(*test)

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
        rules = [string.Template(rule)]
        for key, vals in fmt.items():
            expanded = []
            for rule in rules:
                if key in rule.get_identifiers():
                    expanded.extend(string.Template(rule.safe_substitute(**{key: val})) for val in vals)
                else:
                    expanded.append(rule)
            rules = expanded
        final = [r.safe_substitute() for r in rules]

        if any("{" in r and "}" in r for r in final):
            raise ValueError(f"Invalid rules: {final}. {fmt=}")
        states = {j for i in final for j in i.split()[1::2]}
        if any(len(s) != 1 for s in states):
            raise ValueError(f"Found invalid state, not one char. {final}")
        states_list = [tuple(i.split()[:2]) for i in final]
        states = set(states_list)
        if len(states) != len(states_list):
            raise ValueError(f"Duplicate state in expanded rules, {states_list}")
        if dupes := self.states & states:
            raise ValueError(f"Duplicate states: {dupes}")
        self.states.update(states)
        self.rules.extend(final)

    def right(self, start: str, inp: str | int, **fmt: typing.Iterable[str | int]) -> None:
        """Add a rule where the state and tape do not change."""
        self.add(start, inp, start, inp, R, **fmt)

    def left(self, start: str, inp: str | int, **fmt: typing.Iterable[str | int]) -> None:
        """Add a rule where the state and tape do not change."""
        self.add(start, inp, start, inp, L, **fmt)

    def halt(self, start: str, inp: str | int, out: str | int | None = None, **fmt: typing.Iterable[str | int]) -> None:
        """Add a rule where the state and tape do not change."""
        if out is None:
            out = inp
        self.add(start, inp, HALT, out, L, **fmt)

    def test(self, inp: str, out: str) -> None:
        self.tests.append((inp, out))

    def check(self) -> None:
        transition_rules = logic_mill.parse_transition_rules(self.program())
        mill = logic_mill.LogicMill(transition_rules)
        for idx, (data, want) in enumerate(self.tests):
            result, steps = mill.run(data, verbose=False)
            if result == want:
                print(f"{self.puzzle:>2}.t{idx:<2} PASS")
            else:
                result, steps = mill.run(data, verbose=True)
                raise RuntimeError(f"{self.puzzle}.t{idx}: FAIL")

    def program(self) -> str:
        return "\n".join(self.rules)

    def parse(self, program: str, **expansions: dict[str, collections.abc.Sequence[int | str]]) -> RuleSet:
        for line in program.strip().splitlines():
            words = line.split("#")[0].strip().split()
            try:
                if not words or words[0] == "#":
                    pass
                elif words[0] == ">":
                    self.right(*words[1:], **expansions)
                elif words[0] == "<":
                    self.left(*words[1:], **expansions)
                else:
                    self.add(*words, **expansions)
            except:
                print(line)
                raise
        return self


def unary_addition() -> RuleSet:
    # 1. Unary Addition
    r = RuleSet(1).parse("""
        # Erase the first | so we can replace the + with |
        INIT   |  M    _   R
        # Go to the + then replace it.
        > M    |
        M      +  HALT |   R
    """)

    r.test(  "|+|",   "||")  # 1+1=2
    r.test("||+||", "||||")  # 2+2=4

    return r


def unary_even_odd() -> RuleSet:
    # 2. Unary Even Odd
    r = RuleSet(2).parse("""
        # Move left to right, tracking even or odd, and clearing bits.
        # When we get to the end, write the state.
        INIT    |    O      _   R
        E       |    O      _   R
        O       |    E      _   R
        $i      _    HALT  $i   R
    """, i="EO")

    r.test( "||", "E")
    r.test("|||", "O")

    return r


def binary_increment() -> RuleSet:
    # 3. Binary Increment
    r = RuleSet(3).parse("""
        INIT       0   HALT    1   R
        INIT       1   GO_END  1   R
        > GO_END  $i
        # Work right to left, incrementing and tracking a carry bit. "CARRY" means add one.
        GO_END     _  CARRY    _   L
        CARRY      0  HALT     1   L
        CARRY      1  CARRY    0   L
        CARRY      _  HALT     1   L
    """, i="01")

    r.test(  "1",  "10")  # 1+1=2
    r.test( "10",  "11")  # 2+1=3
    r.test( "11", "100")  # 3+1=4
    r.test("100", "101")  # 4+1=5
    r.test("11010101", "11010110")

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
    r = RuleSet(4).parse("""
        INIT        |    START     |   L      # Change to start and shift left.
        > START     _                         # Move to first | of a.
        START       |   GO_COPY    _   R      # Reduce `a` by one. Go copy `b`.
        > GO_COPY   |                         # Look for start of `b`.
        GO_COPY     *   COPY       *   R      # Start copying `b`.
        COPY        |   GO_END_B   T   R      # Mark a `|` from `b` as copied. Now go add it to the result.
        > GO_END_B  |                         # Find the end of `b`.
        GO_END_B    _   GO_END_C   _   R      # Find the end of `c`.
        > GO_END_C  |                         # Find the end of `b`.
        GO_END_C    _   RET_TO_B   |   L      # Add one to `c`.
        < RET_TO_B  $i                        # Return to the first `|` of `b`.
        RET_TO_B    T   COPY       T   R      # Return to the first `|` of `b`.
        COPY        _   RESET_B    _   L      # Trying to copy from `b` got got a `_`: all done copying `b`. Reset `b`.
        RESET_B     T   RESET_B    |   L      # Reset `b`.
        RESET_B     *   RET_TO_A   *   L      # Done resetting `b`. Return to start of `a`.
        < RET_TO_A  |                         # Done resetting `b`. Return to start of `a`.
        RET_TO_A    _   START      _   R      # Back at the start of `a`.
        START       *   RM_B       _   R      # Trying to reduce `a` but out of `|`: all done copying. Drop `b` from output.
        RM_B        |   RM_B       _   R      # Trying to reduce `a` but out of `|`: all done copying. Drop `b` from output.
        RM_B        _   HALT       _   R      # Done removing `b`. Multiplication completed.
    """, i="|_")

    r.test(   "|*||",        "||")  # 1x2=2
    r.test(  "||*||",      "||||")  # 2x2=4
    r.test( "||*|||",    "||||||")  # 2x3=6
    r.test("|||*|||", "|||||||||")  # 3x3=9

    return r


def find_element_in_unary_array():
    # 5. Find Element in Unary Array
    # Unary index. Minus one index. For each index `|`, remove an element from the array.
    # When we run out of index `|`, remove everything after the first number.
    # == General Solution ==
    r = RuleSet(5).parse("""
        INIT         |   START        _   R       # Start by dropping the leading `|`. At start of to-remove count.
        START        |   GO_LIST      _   R       # Go to the list
        GO_LIST      |   GO_LIST      |   R
        GO_LIST      :   GO_FIRST     :   R       # In the list. Go to the first number.
        GO_FIRST     x   GO_FIRST     x   R
        GO_FIRST     |   RM_FIRST     x   R       # Drop the first number.
        RM_FIRST     |   RM_FIRST     x   R
        RM_FIRST     ,   RETURN_I     x   L       # Return to the start.
        RETURN_I     x   RETURN_I     x   L
        RETURN_I     :   RETURN_I     :   L
        RETURN_I     |   RETURN_I     |   L
        RETURN_I     _   START        _   R       # Got back to the index.
        START        :   CLEAN_PRE    _   R       # Out of index values. Tidy up before the first element.
        CLEAN_PRE    x   CLEAN_PRE    _   R
        CLEAN_PRE    |   CLEAN_PRE    |   R       # Skip the first element.
        CLEAN_PRE    ,   CLEAN_POST   _   R       # Clean remaining elements.
        CLEAN_PRE    _   HALT         _   R       # No following items.
        CLEAN_POST   |   CLEAN_POST   _   R
        CLEAN_POST   ,   CLEAN_POST   _   R
        CLEAN_POST   _   HALT         _   L
    """)

    r.test("|:|||,|||||,||||||||,||||", "|||"),
    r.test("||:|||,|||||,||||||||,||||", "|||||"),
    r.test("||||:|||,|||||,||||||||,||||", "||||"),

    return r

    # == Non-general solution ==
    r = RuleSet(5)
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
    r.halt("SKIP", "_")
    r.halt("TRIM", "_")
    r.add("TRIM", ",", "TRIM", "_", R)
    r.add("TRIM", "|", "TRIM", "_", R)

    return r


def unary_subtraction() -> RuleSet:
    # 6. Unary Subtraction
    # Subtract. `a-b`. Go to end of b. Remove one from `b`. Move to `a`. Replace one with `x`. Return to end of b.
    # Once `b` is gone, drop `-` and `x`.
    r = RuleSet(6).parse("""
        > INIT     $i                    # Go to the end.
        INIT       _   BEGIN    _   L    # At end of `b`.
        BEGIN      |   GO_SIGN  _   L    # Drop one from `b`. Find `-`.
        < GO_SIGN  |
        GO_SIGN    -   GO_ONE   -   L    # Find a value to drop from `a`.
        GO_ONE     x   GO_ONE   x   L
        GO_ONE     |   INIT     x   R    # Drop one from `a`. Return to end.
        BEGIN      -   CLEAN    _   L    # No more `b`. Tidy up.
        CLEAN      x   CLEAN    _   L
        CLEAN      $j  HALT     $j  R
    """, i="|-x", j="|_")

    r.test("|||||-||", "|||"),  # 5-2=3
    r.test(   "||-||",    ""),  # 2-2=0

    return r


def letter_mark() -> RuleSet:
    # 7. Letter Mark
    """Generate state logic to wrap `w` and `ch` in `[]`.

    There are 31 chars to track that all need their own states.

    Strategy:
    * Begin at start of word.
    * Add an `=` at the end and return to start.
    * Check the letter. Erase. If it's anything other than `c`, change to state $letter.
    * If the letter is `c`, go to MAYBE-CH. Then on the next letter, check for h and go to output-c or output-ch.
    * On state $letter, go to the end, skip a space, then output the letter. For `w`, output `[w]`.
    """
    letters = set(string.ascii_lowercase + "-äöõü")
    extras = set("[]=")
    r = RuleSet(7).parse(
        """
        > INIT       $a                       # Move to the end.
        INIT         _   GO_START   =   L     # Add a `=` then return to start.
        < GO_START   $b                      
        GO_START     _   START      _   R
        START        $c  COPY_$c    _   R     # Once at the start copy letter to state.
        START        c   MAYBE_c    _   R     # `c` gets special handling to detect `ch`.
        MAYBE_c      h   COPY_ch    _   R
        MAYBE_c      $d  COPY_c     $d  R
        > COPY_${e}  $f                       # Go to the end so we can output the copy.
        COPY_${g}    _   GO_START   $g  L     # Output the letter then return. `w` and `ch` get special handling.
        COPY_w       _   COPY_w1    [   R     # `w` => `[w]`
        COPY_w1      _   COPY_]     w   R
        COPY_ch      _   COPY_ch1   [   R     # `ch` => `[ch]`
        COPY_ch1     _   COPY_ch2   c   R
        COPY_ch2     _   COPY_]     h   R
        COPY_]       _   GO_START   ]   L
        START        =   HALT       _   R     # End of input
        """,
        a=letters,
        b=letters | extras,
        c=letters - {"c"},
        d=(letters | extras) - {"h"},
        e=letters | {"ch"},
        f=letters | extras,
        g=letters - {"w"},
    )

    r.test("wõta-wastu-mu-soow-ja-chillitse-toomemäel", "[w]õta-[w]astu-mu-soo[w]-ja-[ch]illitse-toomemäel"),

    return r


def text_mirror():
    # 8. Text Mirror
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
    r = RuleSet(8).parse(
        """
        INIT             $a  ADD_EQ         $a  L    # Add a `=` then find the first letter.
        ADD_EQ           _   F              =   R
        > F              !
        F                $a  COPY_$a        !   R    # Copy and tombstone.
        COPY_${a}        $b  COPY_${a}${b}  !   L 
        < COPY_${a}${b}  $c
        COPY_${a}${b}    _   PAST_$b        $a  L    # Found an opening. Record letter then return to the start.
        PAST_${b}        _   GO_EQ          $b  R
        > GO_EQ          $a 
        GO_EQ            =   F              =   R
        F                _   CLEANUP        _   L    # Once there is nothing left to copy clean up tombstones.
        CLEANUP          !   CLEANUP        _   L
        CLEANUP          =   HALT           _   L
        """,
        a=letters,
        b=letters | {"_"},
        c=letters | extras,
    )

    r.test("hello-world", "dlrow-olleh"),

    return r


def unary_comparison() -> RuleSet:
    # 9. Unary Comparison
    """Generate state logic for unary compare.

    General solution:
    Mark `|` as "read" by changing to "x". Read one `|` from both `a` and `b` until one runs out.
    Once one runs out, update the `,` to the result and replace `x` with `|`.
    For minimal steps, start at the `,` and work our way outwards.

    Limited solution: use the state as a counter. Increment on left. Decrement on right.
    """
    r = RuleSet(9).parse(
        """
        > INIT        |                       # Start at the `,`.
        INIT          ,   FIND_LEFT   ,  L    # Look for a left `|`.
        < FIND_LEFT   $i  
        FIND_LEFT     _   EQ_OR_LT    _  R    # Ran out of `|` on the left. Check if there is any right left. Either `=` or `<`.
        FIND_LEFT     |   FIND_RIGHT  x  R    # Look for a matching right `|`.
        #
        > FIND_RIGHT  $i 
        FIND_RIGHT    |   FIND_LEFT   x  L    # Matched. Go back to a left.
        FIND_RIGHT    _   SET_GT      _  L    # Ran out of `|` on the right. We found one on the left so the left is larger (`>`.
        > EQ_OR_LT    $i                      # Go to the right to check if it is `=` or `<`.
        EQ_OR_LT      |   SET_LT      |  L    # Right has more ie is bigger. Set `<`.
        EQ_OR_LT      _   SET_EQ      _  L    # Right has same. Set `=`.
        < SET_$op     |
        SET_$op       x   SET_$op     |  L
        SET_GT        ,   SET_GT      >  L
        SET_LT        ,   SET_LT      <  L
        SET_EQ        ,   SET_EQ      =  L
        SET_$op       _   HALT        _  R
        """,
        i="x,",
        op=["GT", "LT", "EQ"],
    )

    r.test("|||,||||", "|||<||||"),  # 3 > 4
    r.test("||||,|||", "||||>|||"),  # 4 > 3
    r.test( "|||,|||",  "|||=|||"),  # 3 = 3
    r.test( "||||||||||,|||",  "||||||||||>|||"),

    return r

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


def lines_count() -> RuleSet:
    # 10. Lines Count
    letters = set(string.ascii_lowercase + "-äöõü")
    r = RuleSet(10).parse(
        """
        INIT   $i  INIT   !  R
        INIT   +   ADD    +  L
        < ADD  !
        ADD    _   RET    |  R
        ADD    |   INC    |  R
        INC    !   RET    |  R
        > RET  !
        RET    +   INIT   !  R
        INIT   _   CLEAN  _  L
        CLEAN  !   CLEAN  _  L
        CLEAN  |   END    |  R
        CLEAN  _   HALT   |  R
        END    _   HALT   |  R
        """, i=letters)

    r.test("hello+world+how-are-you", "|||"),
    r.test("hello", "|"),

    return r


def decimal_increment() -> RuleSet:
    # 11. Decimal Increment
    r = RuleSet(11)
    r.right(INIT, "$i", i=range(10))
    r.add(INIT, "_", "INC", "_", L)
    # Increment 0-8 and end, no carry.
    for i in range(9):
        r.halt("INC", i, i + 1)
    # Carry over on a 9.
    r.add("INC", 9, "INC", 0, L)
    r.halt("INC", "_", 1)

    for i in range(0, 111, 7):
        r.test(str(i), str(i + 1))

    return r


def decimal_addition():
    """Add two decimal values.

    1. Add a = on the left, setting up c=a+b
    2. Find the right-most `a` value. Copy `a` into state. If carrying, add 1. Replace with |.
    3. Find the right-most `b` value. Copy `a+b` into state. Replace with _.
    4. Go left then write out `a+b`.

    When a or b is not found, switch into copy mode, copying over remaining letters one by one.
    However, if we're carrying, we need to instead treat it as a carry/add 1.
    """
    # 12. Decimal Addition
    r = RuleSet(12)

    carries = ["", "_C"]  # some states have a carrying and not-carrying state
    # Add a = on the left.
    r.left(INIT, "$i", i=range(10))
    r.add(INIT, "_", "GET_A", "=", R)
    # Copy the right-most digit of `a` into the state.
    r.right("GET_A$j", "$i", i=string.digits + "=", j=carries)
    r.add("GET_A$j", "$i", "PICK_A$j", "$i", L, i="+|", j=carries)
    r.add("PICK_A$j", "|", "PICK_A$j", "|", L, j=carries)
    r.add("PICK_A", "${i}", "GO_B${i}", "|", R, i=range(10))
    for i in range(10):
        r.add("PICK_A_C", i, f"GO_B{i + 1}", "|", R)
    r.add("PICK_A", "=", "COPY", "=", R,)
    r.add("PICK_A_C", "=", "GO_B1", "=", R)
    # Copy `a+b` into state using the right-most digit of `b`.
    r.add("GO_B${i}", "|", "GO_B${i}", "|", R, i=range(11))
    r.add("GO_B${i}", "+", "GET_B${i}", "+", R, i=range(11))
    r.right("GET_B${i}", "${j}", i=range(11), j=range(10))
    r.add("GET_B${i}", "_", "PICK_B${i}", "_", L, i=range(11))
    for i in range(11):
        for j in range(10):
            r.add(f"PICK_B{i}", j, f"ADD{i + j}", "_", L)
    r.add("PICK_B${i}", "+", "COPY_${i}", "_", L, i=range(11))
    # Write out the value of `a+b` into `c`.
    r.left("ADD${i}", "${j}", i=range(20), j=string.digits + "|+=")
    for i in range(10):
        r.add(f"ADD{i}", "_", "GET_A", i % 10, R)
    for i in range(10, 20):
        r.add(f"ADD{i}", "_", "GET_A_C", i % 10, R)
    # When a or b is empty, copy over the remaining prefix.
    r.right("COPY$j", "${i}", i=string.digits + "|+=", j=carries)
    r.add("COPY$j", "_", "COPY_G$j", "_", L, j=carries)
    r.halt("COPY_G", "=", "_")
    r.add("COPY_G_C", "=", "COPY_1", "=", L,)
    r.add("COPY_G$j", "${i}", "COPY_G$j", "_", L, i="_|+", j=carries)
    r.add("COPY_G", "${i}", "COPY_${i}", "_", L, i=range(10))
    for i in range(10):
        r.add("COPY_G_C", i, f"COPY_{i+1}", "_", L)
    r.left("COPY_${i}", "${j}", i=range(11), j=string.digits + "|+=")
    r.add("COPY_${i}", "_", "COPY", "${i}", R, i=range(10))
    r.add("COPY_10", "_", "COPY_C", "0", R)

    for i, j in [(1, 2), (19, 82), (888, 9999999), (999999, 4444)]:
        r.test(f"{i}+{j}", f"{i+j}")

    return r


def unary_array_sort():
    """Sort a unary array."""
    # 13. Unary Array Sort
    r = RuleSet(
        13, [
            ("||,|,|||||,||||||||", "|,||,|||||,||||||||"),
            ("|,|", "|,|"),
            ("|||,|||||||,|||||", "|||,|||||,|||||||"),
            ("|,|,|,|,|,|,|,|,|,|", "|,|,|,|,|,|,|,|,|,|"),
            ("||||,||,|,|||", "|,||,|||,||||"),
            ("||,|||||,|,|||||||||,||,|||||||||,|||||,||,|,||||", "|,|,||,||,||,||||,|||||,|||||,|||||||||,|||||||||"),
        ]
    )
    r.halt(INIT, "_")
    r.add(INIT, "|", "RESET", "|", L)
    r.add("RESET", "_", "CHECK", "_", R)
    # Check if this is the last element in the array. If it is, halt.
    r.right("CHECK", "|")
    r.halt("CHECK", "_")
    r.add("CHECK", ",", "CHECKED", ",", L)
    r.left("CHECKED", "|")
    r.add("CHECKED", "$c", "COUNT_0", "$c", R, c=",_")
    # There are two or more elements. Count the first. Subtract the second.
    # If the first is larger, we need to shift left the `,` by the difference.
    for i in range(380):
        r.add(f"COUNT_{i}", "|", f"COUNT_{i + 1}", "|", R)
        r.halt(f"COUNT_{i}", "_")
        r.add(f"COUNT_{i}", ",", f"SUB_{i}", ",", R)
        if i:
            r.add(f"SUB_{i}", "|", f"SUB_{i - 1}", "|", R)
            r.add(f"SUB_{i}", ",", f"G_{i}", ",", L)
            r.add(f"SUB_{i}", "_", f"G_{i}", "_", L)
    for i in range(1, 270):
        r.left(f"G_{i}", "|", )
        r.add(f"G_{i}", ",", f"M_{i - 1}", "|", L)
        r.add(f"M_{i}", "|", f"M_{i - 1}", "|", L)
    r.add("M_0", "|", "RESET", ",", L)
    r.add("SUB_0", "|", "NEXT_L", "|", L)
    r.add("SUB_0", ",", "NEXT_L", ",", L)
    r.halt("SUB_0", "_")
    r.left("NEXT_L", "|")
    r.add("NEXT_L", ",", "CHECK", ",", R)
    r.left("RESET", "$c", c="|,")



    assert len({i.split()[0] for i in r.rules}) <= 1024, len({i.split()[0] for i in r.rules})

    return r


SOLUTIONS = [
    unary_addition,
    unary_even_odd,
    binary_increment,
    unary_multiplication,
    find_element_in_unary_array,
    unary_subtraction,
    letter_mark,
    text_mirror,
    unary_comparison,
    lines_count,
    decimal_increment,
    decimal_addition,
    unary_array_sort,
]


@click.command()
@click.option("-d", "puzzle", type=int, help="Puzzle number")
@click.option("--out", type=click.Path(path_type=pathlib.Path), required=False)
def main(puzzle: int, out: pathlib.Path | None) -> None:
    if puzzle == 0:
        for r in SOLUTIONS:
            r().check()
        return
    if puzzle is None:
        puzzle = len(SOLUTIONS)
    ruleset = SOLUTIONS[puzzle - 1]()
    ruleset.check()
    if out:
        out.write_text(ruleset.program())


if __name__ == "__main__":
    main()
