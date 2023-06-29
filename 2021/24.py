#!/bin/python
"""Advent of Code: Day 24."""

from __future__ import annotations
import collections
import dataclasses
import operator

import input_data
from lib import aoc

OP = {
    "add": operator.add,
    "mul": operator.mul,
    "div": operator.floordiv,
    "mod": operator.mod,
    "eql": operator.eq,
}

SYMBOL = {
    "add": "+",
    "mul": "*",
    "div": "//",
    "mod": "%",
    "eql": "==",
    "neq": "!=",
}


@dataclasses.dataclass
class Node:
    """A node, representing one VM instruction/value."""

    # Used to indicate an input and track input index.
    input_idx: int = None
    # Operator, one of OP. Used in conjunction with parts.
    operator: str = None
    parts: list[Node] = None
    # Literal int value.
    literal: int = None
    # An indexed `z` node with the value in `value`.
    z_idx: int = None
    z_val: Node = None
    # An indexed `eql` node with the value in `value`.
    eql_idx: int = None
    eql_val: Node = None
    eql_evaled: Node = None

    @property
    def is_input(self) -> bool:
        """Return if the Node is an input Node."""
        return self.input_idx is not None

    @property
    def is_literal(self) -> bool:
        """Return if the Node is a literal Node."""
        return self.literal is not None

    @property
    def is_z(self) -> bool:
        """Return if the Node is a z Node."""
        return self.z_idx is not None

    @property
    def is_op(self) -> bool:
        """Return if the Node is an operation Node."""
        return self.operator is not None

    @property
    def is_eql(self) -> bool:
        """Return if the Node is an eql Node."""
        return self.eql_idx is not None

    @property
    def left(self) -> Node:
        """Return the left side of the operation."""
        assert self.is_op
        return self.parts[0]

    @property
    def right(self) -> Node:
        """Return the right side of the operation."""
        assert self.is_op
        return self.parts[1]

    def __str__(self) -> str:
        """Return a string representation of a node."""
        if self.is_literal:
            return f"{self.literal}"
        if self.is_input:
            return f"input_{self.input_idx:02}"
        if self.is_z:
            return f"z_{self.z_idx:02}"
        if self.is_eql:
            return f"eql_{self.eql_idx:02}"
        assert self.is_op
        return f"({self.left} {SYMBOL[self.operator]} {self.right})"

    def eql_range_check_true(self) -> bool:
        """Return is a `eql` operator can be resolved as True.

        Given `a != input` (z_idx == 0) or `(z % 26) + a != input` determine
        if the `eql` is impossible and the inverse `neq` must be True.

        Given that `input` cannot be larger than 9, if `a > 9` then the `neq`
        must be True.
        """
        # assert: x != input
        assert self.operator == "neq"
        assert self.right.is_input
        if self.left.is_literal:
            # lit != input
            a_val = self.left.literal
        elif self.left.operator == "mod":
            # assert: (z % 26) != input
            # aka: (z % 26) + 0 != input
            assert self.left.left.is_z
            assert self.left.right.literal == 26
            a_val = 0
        else:
            # assert: (z % 26) + lit != input
            assert self.left.operator == "add", str(self)
            assert self.left.right.is_literal
            assert self.left.left.operator == "mod"
            assert self.left.left.left.is_z
            assert self.left.left.right.literal == 26
            a_val = self.left.right.literal

        return a_val >= 10

    def eval_node(self) -> Node:
        """Evalute a node, replacing `eql` nodes with their evaluated values."""
        if self.is_z or self.is_literal or self.is_input:
            return self
        if self.is_eql:
            assert self.eql_evaled is not None
            return self.eql_evaled
        assert self.is_op and self.operator != "eql"
        vals = [node.eval_node() for node in self.parts]
        return OP[self.operator](vals[0], vals[1])

    def __add__(self, other: Node) -> Node:
        """Add two Nodes."""
        # 0 + x == x
        if self.literal == 0:
            return other
        # x + 0 == x
        if other.literal == 0:
            return self
        if self.is_literal and other.is_literal:
            return Node(literal=self.literal + other.literal)
        # (x + y) + z = x + (y + z)
        if self.operator == "add" and self.right.is_literal and other.is_literal:
            rhs = Node(literal=self.right.literal + other.literal)
            return Node(operator="add", parts=[self.left, rhs])
        return Node(operator="add", parts=[self, other])

    def __mod__(self, other: Node) -> Node:
        """Apply modulus."""
        # 0 % x == 0
        if self.literal == 0:
            return self
        return Node(operator="mod", parts=[self, other])

    def __mul__(self, other: Node) -> Node:
        """Multiply two Nodes."""
        # 0 * x == 0;  x * 1 == x
        if self.literal == 0 or other.literal == 1:
            return self
        # 1 * x == x; x * 0 == 0
        if self.literal == 1 or other.literal == 0:
            return other
        return Node(operator="mul", parts=[self, other])

    def __floordiv__(self, other: Node) -> Node:
        """Divide two Nodes."""
        if other.literal == 1:
            return self
        return Node(operator="div", parts=[self, other])

    def __eq__(self, other: Node) -> Node:
        """Equallity operator is always followed by a `not`. Return a != Node."""
        return Node(operator="neq", parts=[self, other])

    def div26(self) -> Node:
        """Apply Node // 26."""
        node = self
        if node.is_z:
            node = node.z_val
        # (input + a) // 26 = 0 for small values of a.
        if (
            node.operator == "add"
            and node.left.is_input
            and node.right.is_literal
            and node.right.literal <= 16
        ):
            return Node(literal=0)
        if self.is_input:
            return Node(literal=0)
        # (a * 26) // 26 = a
        if node.operator == "mul" and node.right.literal == 26:
            return node.left
        # (a + b) // 26 = a // 26 + b // 26 ... when a = x * 26.
        if node.operator == "add":
            # assert: z * 26 + x
            assert node.left.operator == "mul" and node.left.right.literal == 26
            return node.left.div26() + node.right.div26()
        if node.operator == "div":
            assert node.right.literal == 26
            return node.left.div26().div26()
        raise RuntimeError(f"Unhandled div26: {node}")

    def mod26(self) -> Node:
        """Apply Node % 26."""
        node = self
        if node.is_z:
            node = node.z_val
        # (input + a) % 26 = (input + a) for small values of a.
        if (
            node.operator == "add"
            and node.left.is_input
            and node.right.is_literal
            and node.right.literal <= 16
        ):
            return node
        if self.is_input:
            return node
        # (a * 26) % 26 == 0
        if node.operator == "mul" and node.right.literal == 26:
            return Node(literal=0)
        # (a + b) % 26 = (a % 26 + b % 26) % 26
        if node.operator == "add":
            return (node.left.mod26() + node.right.mod26()).mod26()
        raise RuntimeError(f"Unhandled mod26: {node}")

    def eval(self):
        """Evaluate a node, for simplified Nodes."""
        if self.is_literal or self.is_input:
            return self
        if self.operator == "add":
            return self.left.eval() + self.right.eval()
        if self.operator == "mod":
            assert self.right == 26
            return self.left.mod26()
        raise RuntimeError(f"Unhandled eval: {self}")


class Day24(aoc.Challenge):
    """Compute which serial numbers are valid for the MONAD.

    This exercise is mostly focused around reverse engineering the "MONAD"
    input program and only minimally about implementing the VM described in the prose.

    The input MONADs have certain characteristics which need to be sussed out and used.
    The MONAD follows the same pattern 14 times:
    * Input is loaded into `w`.
    * The `x` and `y` are set to 0.
    * There are two `eql` statements back to back, `eql x w` then `eql x 0`. Combined,
      this can be treated as `x != w`.
    * The `z` is set to a function of the prior `z` and a conditional on the input.

    Step 1
    ------

    Resolve all 14 `z` values (indicated by `add z y`) in terms of a prior `z`.
    This gives the form:
    z_(n+1) =
        (f(z_(n)) * ((25 * (((z_(n) % 26) + a) != Input_(n+1))) + 1))
        + ((Input_(n+1) + b) * (((z_(n) % 26) + a) != Input_(n+1)))
    where a, b are fixed ints and `f(x) = x` or `f(x) = x // 26`

    Rewritten as a conditional,

    ```
    if ((z_(n) % 26) + a) != Input_(n+1):
        z_(n+1) = 26 * f(z_(n)) + Input_(n+1) + c
    else:
        z_(n+1) = f((z_(n))
    ```

    Step 2
    ------

    Examining the conditionals and bearing in mind that inputs must be [1..9],
    `(z % 26) + a != Input` will be true for all possible inputs if `a > 9`.

    Applying that reduction to the code yields seven instances of:

    ```
    z_(n+1) = z_(n) * 26 + Input_(n+1) + a
    ```

    where `z_(-1) = 0` and `a` is a known int.

    Given that inputs are valid iff `z_13 = 0`, there must be seven instances of:
    `z_(n+1) = z_(n) // 26` to reduce the `z` value to 0. These are found by setting
    the conditional `(z_n % 26) + a = Input_(n+1)`.

    Step 3
    ------

    Given `z_(n+1) = z_(n) * 26 + Input_(n+1) + a` and `z_(n+2) = z_(n+1) // 26`,
    we can reduce `z_(n+2) = z_(n)`. Using this transformation, this allows us to write
    all `z` values in the form `z_(x) = z_(y) * 26 + Input_(z) + a`

    Applying the reduced `z` for to the known equallities,
    `(z_n % 26) + a = Input_(n+1)`, `z % 26` becomes `(z_y * 26 + Input + a) % 26`
    which becomes `(z_y * 26) % 26 + (Input + a) % 26` which further reduces to
    simply `Input + a`. That gives us seven instances of
    `Input_x = Input_y + a`, each with unrelated `x` and `y` values.

    Step 4
    ------

    Recalling that all inputs must be [1..9], `Input_x = Input_y + a` gives a min
    and max value for both `Input` values. This gives upper and lower limits on all
    14 input values.
    """

    DEBUG = False

    TESTS = [
        aoc.TestCase(inputs=v, part=p + 1, want=input_data.DAY24_SOLUTIONS[k][p])
        for k, v in input_data.DAY24.items()
        for p in (0, 1)
    ]
    INPUT_PARSER = aoc.parse_multi_str_per_line

    def part1(self, parsed_input: list[tuple[str, ...]]) -> int:
        """Return the max valid seriel number."""
        ranges = self.solve_ranges(parsed_input)
        return int("".join(str(ranges[i][1]) for i in range(14)))

    def part2(self, parsed_input: list[tuple[str, ...]]) -> int:
        """Return the min valid seriel number."""
        ranges = self.solve_ranges(parsed_input)
        return int("".join(str(ranges[i][0]) for i in range(14)))

    def build_ast(self, monad: list[tuple[str, ...]]) -> tuple[dict[int, Node], dict[int, Node]]:
        """Parse the input Monad and return both the z Nodes and eql Nodes."""
        mem = {v: Node(literal=0) for v in 'wxyz'}

        z_vals = {}
        eql_vals = {}

        input_counter = 0
        z_counter = 0
        eql_counter = 0

        # Parse the input into a Node tree.
        for operation, *operands in monad:
            # All "eql" statements come in pairs of "eql x ?" then "eql x 0" which
            # can be combined and treated as "neq x ?". Skip the negation.
            if operation == "eql" and operands == ["x", "0"]:
                continue

            # Set the memory to the value/instruction.
            if operation == "inp":
                var = operands[0]
                mem[var] = Node(input_idx=input_counter)
                input_counter += 1
            else:
                op_a, op_b = operands
                if op_b in "wxyz":
                    op_b = mem[op_b]
                else:
                    op_b = Node(literal=int(op_b))
                mem[op_a] = OP[operation](mem[op_a], op_b)

            # Replace `add z y` values with special z Nodes and track them.
            if operation == "add" and operands == ["z", "y"]:
                node = Node(z_idx=z_counter, z_val=mem[op_a])
                mem[op_a] = node
                self.debug(f"{node} = {node.z_val}")
                z_vals[z_counter] = node
                z_counter += 1

            # Replace `eql` values with special eql Nodes and track them.
            if operation == "eql":
                node = Node(eql_idx=eql_counter, eql_val=mem[op_a])
                mem[op_a] = node
                eql_vals[eql_counter] = node
                eql_counter += 1

        return z_vals, eql_vals

    def resolve_eqls(self, eql_vals: dict[int, Node]) -> None:
        """Resolve all eql/neq nodes to 0 or 1/.

        Range check the eql Nodes to determine if they can be resolved.
        (input_x + a != input_y for a >= 10) must be True since input < 10.

        If not True, assume False and assert the counts of True and False balance.

        The number of True and False neq Nodes must balance for z_13 == 0
        because we must balance the z_n * 26 with the z_n // 26.

        After resolving, the eqls where we know eql is Tue looks like:

        Input_5 = ((z_03 % 26) + -8)
        Input_7 = ((z_05 % 26) + -11)
        Input_9 = ((z_07 % 26) + -6)
        Input_10 = ((z_08 % 26) + -9)
        Input_12 = ((z_10 % 26) + -5)
        Input_13 = ((z_11 % 26) + -4)
        Input_14 = ((z_12 % 26) + -9)
        """
        for node in eql_vals.values():
            if node.eql_val.eql_range_check_true():
                node.eql_evaled = Node(literal=1)
            else:
                node.eql_evaled = Node(literal=0)
            self.debug(f"{node} {node.eql_val} {node.eql_evaled}")

        count = collections.Counter(node.eql_evaled.literal for node in eql_vals.values())
        assert count[0] == count[1]

    def resolve_z_values(self, z_vals: dict[int, Node]) -> None:
        """Resolve z values using fixed eql values.

        Once all eql Nodes have a fixed 0 or 1 value, the z Nodes can be evaluated
        using the fixed eql value.

        This results in z Nodes having values like:

        z_00 = (Input_1 + 7)
        z_01 = ((z_0 * 26) + (Input_2 + 8))
        z_02 = ((z_1 * 26) + (Input_3 + 16))
        z_04 = (z_3 // 26)
        z_06 = (z_5 // 26)

        Next, (z // 26) can be resolved by referencing prior z values, resulting in:

        z_00 = Input_01 + 7
        z_01 = z_00 * 26 + Input_02 + 8
        z_02 = z_01 * 26 + Input_03 + 16
        z_04 = z_02
        z_06 = z_02
        z_11 = z_01
        z_12 = z_00
        z_13 = 0
        """
        # Update the z Nodes now that the eql Nodes have all been assigned a value.
        for node in z_vals.values():
            # Update z value using the fixed eql values.
            node.z_val = node.z_val.eval_node()
            self.debug(f"{node} = {node.z_val}")

        # Simplify z Nodes of the form z // 26.
        for node in z_vals.values():
            assert node.z_val.operator in ("add", "div"), node.z_val
            if node.z_val.operator == "div":
                assert node.z_val.right == 26
                val = node.z_val.left.div26()
                while val.is_z:
                    val = z_vals[val.z_idx].z_val
                node.z_val = val
            self.debug(f"{node} = {node.z_val}")

    def input_offsets(self, eql_vals: dict[int, Node]) -> dict[int, int]:
        """Return the "offset" of each input.

        For neq Nodes set to 0, ie eql is True, evaluate Nodes to find equalities
        of the form `input_x = input_y + a`. Conversely this gives
        `input_y = input_x + b, b = -a`. Return the "offset" for each input.

        Input_01 = Input_02
        Input_03 = Input_04 + 1
        Input_05 = Input_06 - 3

        => {1: 0, 2: 0, 3: 1, 4: -1, 5: -33, 6: 3}
        """
        # Discard inequalities. Only equalities can be used to assess values.
        eql_vals = [node for node in eql_vals.values() if node.eql_evaled.literal == 0]

        offsets = {}
        for node in eql_vals:
            # neq is True. eql is False. Cannot assign ranges.
            left, right = [p.eval() for p in node.eql_val.parts]
            # assert: input_x + a = input_b
            assert left.operator == "add" and left.left.is_input and left.right.is_literal
            assert right.is_input
            offset = left.right.literal
            offsets[left.left.input_idx] = offset
            offsets[right.input_idx] = -offset
            self.debug(f"{left} = {right}")
        return offsets

    @staticmethod
    def ranges(offsets: dict[int, int]) -> dict[int, tuple[int, int]]:
        """Return valid values for each input (min, max) based on the known offsets."""
        return {
            idx: (max(1, 1 - offset), min(9, 9 - offset))
            for idx, offset in offsets.items()
        }

    def solve_ranges(self, monad: list[tuple[str, ...]]) -> dict[int, tuple[int, int]]:
        """Decompose a MONAD program to derive valid input values."""
        # Build the AST to get the z Nodes and eql Nodes.
        z_vals, eql_vals = self.build_ast(monad)

        # Assign a fixed value (0 or 1) to all eql Nodes.
        self.resolve_eqls(eql_vals)

        # Simplify z Nodes using the fixed eql values.
        self.resolve_z_values(z_vals)

        # Given the known z values and half the equalities fixed, resolve the
        # "offset" of each input from another input. `input_x = input_y + offset`.
        offsets = self.input_offsets(eql_vals)

        # Use the known input offsets to compute the min/max value for each input.
        return self.ranges(offsets)
