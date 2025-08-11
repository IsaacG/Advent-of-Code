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

    def __init__(self, puzzle: int):
        self.rules = []
        self.tests = []
        self.puzzle = puzzle

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


def unary_addition() -> RuleSet:
    # 1. Unary Addition
    r = RuleSet(1)
    # Erase the first | so we can replace the + with |
    r.add(INIT, "|", "M", "_", R)
    # Go to the + then replace it.
    r.right("M", "|")
    r.add("M", "+", HALT, "|", R)

    r.test(  "|+|",   "||")  # 1+1=2
    r.test("||+||", "||||")  # 2+2=4

    return r


def unary_even_odd() -> RuleSet:
    # 2. Unary Even Odd
    r = RuleSet(2)

    # Move left to right, tracking even or odd, and clearing bits.
    # When we get to the end, write the state.
    r.add(INIT,  "|",  "O",  "_", R)
    r.add( "E",  "|",  "O",  "_", R)
    r.add( "O",  "|",  "E",  "_", R)
    r.add("$i",  "_", HALT, "$i", R, i="EO")

    r.test( "||", "E")
    r.test("|||", "O")

    return r


def binary_increment() -> RuleSet:
    # 3. Binary Increment
    r = RuleSet(3)
    r.add(    INIT,   0,     HALT,   1, R)
    r.add(    INIT,   1, "GO_END",   1, R)
    r.right("GO_END",   "$i", i="01")
    # Work right to left, incrementing and tracking a carry bit. "CARRY" means add one.
    r.add("GO_END", "_",  "CARRY", "_", L)
    r.add( "CARRY",   0,     HALT,   1, L)
    r.add( "CARRY",   1,  "CARRY",   0, L)
    r.add( "CARRY", "_",     HALT,   1, L)

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
    r = RuleSet(4)

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
    r = RuleSet(5)

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
    r.add("SKIP", "_", "HALT", "_", R)
    r.add("TRIM", "_", "HALT", "_", R)
    r.add("TRIM", ",", "TRIM", "_", R)
    r.add("TRIM", "|", "TRIM", "_", R)

    r.test("|:|||,|||||,||||||||,||||", "|||"),
    r.test("||:|||,|||||,||||||||,||||", "|||||"),
    r.test("||||:|||,|||||,||||||||,||||", "||||"),

    return r


def unary_subtraction() -> RuleSet:
    # 6. Unary Subtraction
    # Subtract. `a-b`. Go to end of b. Remove one from `b`. Move to `a`. Replace one with `x`. Return to end of b.
    # Once `b` is gone, drop `-` and `x`.
    r = RuleSet(6)

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
    r = RuleSet(7)

    # Move to the end.
    r.right(INIT, "$i", i=letters)
    # Add a `=` then return to start.
    r.add(INIT, "_", "GO_START", "=", L)
    r.left("GO_START", "$i", i=letters | extras)
    r.add("GO_START", "_", "START", "_", R)
    # Once at the start, copy letter to state.
    r.add("START", "$i", "COPY_$i", "_", R, i=letters - {"c"})
    # `c` gets special handling to detect `ch`.
    r.add("START", "c", "MAYBE_c", "_", R)
    r.add("MAYBE_c", "h", "COPY_ch", "_", R)
    r.add(f"MAYBE_c", "$i", "COPY_c", "$i", R, i=(letters | extras) - {"h"})
    # Go to the end so we can output the copy.
    r.right("COPY_${i}", "$j", i=letters | {"ch"}, j=letters | extras)
    # Output the letter then return. `w` and `ch` get special handling.
    r.add("COPY_${i}", "_", "GO_START", "$i", L, i=letters - {"w"})
    # `w` => `[w]`
    r.add("COPY_w", "_", "COPY_w1", "[", R)
    r.add("COPY_w1", "_", "COPY_]", "w", R)
    # `ch` => `[ch]`
    r.add("COPY_ch", "_", "COPY_ch1", "[", R)
    r.add("COPY_ch1", "_", "COPY_ch2", "c", R)
    r.add("COPY_ch2", "_", "COPY_]", "h", R)
    r.add("COPY_]", "_", "GO_START", "]", L)
    # End of input
    r.add("START", "=", "HALT", "_", R)

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
    r = RuleSet(8)

    # Add a `=` then find the first letter.
    r.add(INIT, "$i", "ADD_EQ", "$i", L, i=letters)
    r.add("ADD_EQ", "_", "F", "=", R)
    r.right("F", "!")
    # Copy and tombstone.
    r.add("F", "$i", "COPY_$i", "!", R, i=letters)
    r.add("COPY_${i}", "$j", "COPY_${i}${j}", "!", L, i=letters, j=letters | {"_"})
    r.left("COPY_${i}${j}", "${k}", i=letters, j=letters | {"_"}, k=letters | extras)
    # Found an opening. Record letter then return to the start.
    r.add("COPY_${i}${j}", "_", "PAST_$j", "$i", L, i=letters, j=letters | {"_"})
    r.add("PAST_${i}", "_", "GO_EQ", "$i", R, i=letters | {"_"})
    r.right("GO_EQ", "$i", i=letters)
    r.add("GO_EQ", "=", "F", "=", R)
    # Once there is nothing left to copy, clean up tombstones.
    r.add("F", "_", "CLEANUP", "_", L)
    r.add("CLEANUP", "!", "CLEANUP", "_", L)
    r.add("CLEANUP", "=", "HALT", "_", L)

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
    r = RuleSet(9)

    # Start at the `,`.
    r.right(INIT, "|")
    # Look for a left `|`.
    r.add("INIT", ",", "FIND_LEFT", ",", L)
    r.left("FIND_LEFT", "$i", i="x,")
    # Ran out of `|` on the left. Check if there is any right left. Either `=` or `<`.
    r.add("FIND_LEFT", "_", "EQ_OR_LT", "_", R)
    # Look for a matching right `|`.
    r.add("FIND_LEFT", "|", "FIND_RIGHT", "x", R)
    #
    r.right("FIND_RIGHT", "$i", i="x,")
    # Matched. Go back to a left.
    r.add("FIND_RIGHT", "|", "FIND_LEFT", "x", L)
    # Ran out of `|` on the right. We found one on the left so the left is larger (`>`).
    r.add("FIND_RIGHT", "_", "SET_GT", "_", L)
    # Go to the right to check if it is `=` or `<`.
    r.right("EQ_OR_LT", "$i", i="x,")
    # Right has more, ie is bigger. Set `<`.
    r.add("EQ_OR_LT", "|", "SET_LT", "|", L)
    # Right has same. Set `=`.
    r.add("EQ_OR_LT", "_", "SET_EQ", "_", L)
    # Clean up the data.
    r.left("SET_$i", "|", i=["GT", "LT", "EQ"])
    r.add("SET_$i", "x", "SET_$i", "|", L, i=["GT", "LT", "EQ"])
    r.add("SET_GT", ",", "SET_GT", ">", L)
    r.add("SET_LT", ",", "SET_LT", "<", L)
    r.add("SET_EQ", ",", "SET_EQ", "=", L)
    r.add("SET_$i", "_", "HALT", "_", R, i=["GT", "LT", "EQ"])

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
    r = RuleSet(10)

    r.add(INIT, "$i", INIT, "!", R, i=letters)
    r.add(INIT, "+", "ADD", "+", L)
    r.left("ADD", "!")
    r.add("ADD", "_", "RET", "|", R)
    r.add("ADD", "|", "INC", "|", R)
    r.add("INC", "!", "RET", "|", R)
    r.right("RET", "!")
    r.add("RET", "+", "INIT", "!", R)
    r.add(INIT, "_", "CLEAN", "_", L)
    r.add("CLEAN", "!", "CLEAN", "_", L)
    r.add("CLEAN", "|", "END", "|", R)
    r.add("CLEAN", "_", HALT, "|", R)
    r.add("END", "_", HALT, "|", R)

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
        r.add("INC", i, HALT, i + 1, R)
    # Carry over on a 9.
    r.add("INC", 9, "INC", 0, L)
    r.add("INC", "_", HALT, 1, R)

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
    r.add("COPY_G", "=", "HALT", "_", L,)
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


SOLUTIONS = [
    unary_addition(),
    unary_even_odd(),
    binary_increment(),
    unary_multiplication(),
    find_element_in_unary_array(),
    unary_subtraction(),
    letter_mark(),
    text_mirror(),
    unary_comparison(),
    lines_count(),
    decimal_increment(),
    decimal_addition(),
]


@click.command()
@click.option("-d", "puzzle", type=int, help="Puzzle number")
@click.option("--out", type=click.Path(path_type=pathlib.Path), required=False)
def main(puzzle: int, out: pathlib.Path | None) -> None:
    if puzzle == 0:
        for r in SOLUTIONS:
            r.check()
        return
    if puzzle is None:
        puzzle = len(SOLUTIONS)
    ruleset = SOLUTIONS[puzzle - 1]
    ruleset.check()
    if out:
        out.write_text(ruleset.program())


if __name__ == "__main__":
    main()
