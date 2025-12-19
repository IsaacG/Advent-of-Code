"""Assembunny Computer Simulator."""

import enum
from lib import aoc


class Operation(enum.IntEnum):
    """Assembunny operations."""
    INC = enum.auto()
    DEC = enum.auto()
    JNZ = enum.auto()
    TGL = enum.auto()
    OUT = enum.auto()
    CPY = enum.auto()


OP_INC = Operation.INC.value
OP_DEC = Operation.DEC.value
OP_JNZ = Operation.JNZ.value
OP_TGL = Operation.TGL.value
OP_OUT = Operation.OUT.value
OP_CPY = Operation.CPY.value

# Toggle transition. Default result and a map, based on arg count.
# For one argument instruction, INC becomes DEC and all else becomes INC.
TOGGLE = {1: (OP_INC, {OP_INC: OP_DEC}), 2: (OP_JNZ, {OP_JNZ: OP_CPY})}


class Assembunny:
    """Assembunny computer emulator."""

    def __init__(self, instructions: list[str | int]):
        """Initialize, parse the instructions."""
        inst = []
        for instruction in instructions:
            inst.append([Operation[instruction[0].upper()].value] + instruction[1:])
        self.instructions = inst
        self.instruction_count = len(instructions)

    def run(self, register_a: int = 0, register_c: int = 0) -> tuple[int, bool]:
        """Run the program, returning register "a" and if a Clock Signal is output."""
        instructions = self.instructions.copy()
        end = self.instruction_count
        register = {i: 0 for i in "bd"}
        register["a"] = register_a
        register["c"] = register_c

        ptr = 0
        prior_states: set[tuple[int, int, int, int, int]] = set()

        def state():
            """Tuple representing the current state of the computer, used for cycle checking.

            The instruction args and immutable, so they do not need to be checked.
            What changes in the state is (1) the register values and (2) the instructions (word 1).
            """
            instruction_state = 0
            for instruction in instructions:
                instruction_state = instruction_state * 8 + instruction[0]
            return (instruction_state,) + tuple(register.values())

        def multiply():
            """Handle a multiplication loop efficiently.

            # a += b * d ==>
                                  for(; d > 0; d--) {
            4: ["cpy", "b", "c"]    for (c = b; c--; c > 0) {  # a += b
            5: ["inc", "a"]           a++
            6: ["dec", "c"]       
            7: ["jnz", "c", "-2"]   }
            8: ["dec", "d"]
            9: ["jnz", "d", "-5"] }
            """
            nonlocal ptr
            var_b, var_c = instructions[ptr][1:]
            var_a = instructions[ptr + 1][1]
            var_d = instructions[ptr + 4][1]
            want = [
                [OP_CPY, var_b, var_c],
                [OP_INC, var_a],
                [OP_DEC, var_c],
                [OP_JNZ, var_c, "-2"],
                [OP_DEC, var_d],
                [OP_JNZ, var_d, "-5"],
            ]
            if instructions[ptr:ptr + 6] != want:
                return False
            register[var_a] += register[var_c] * register[var_d]
            register[var_c] = register[var_d] = 0
            ptr += 5
            return True

        def decrement_or_addition():
            """Handle an addition loop efficiently.

            5: ["dec", "b"]
            6: ["inc", "a"]
            7: ["jnz", "b", "-2"]

            Note, lines 5, 6 could be swapped and are not handled.
            """
            nonlocal ptr
            var_b, var_a = instructions[ptr][1], instructions[ptr + 1][1]
            want = [
                [OP_DEC, var_b],
                [OP_INC, var_a],
                [OP_JNZ, var_b, "-2"],
            ]
            if instructions[ptr:ptr + 3] != want:
                register[var_b] -= 1
                return
            register[var_a] += register[var_b]
            register[var_b] = 0
            ptr += 2

        def value(arg: int | str) -> int:
            return arg if isinstance(arg, int) else register[arg]

        # Clock signal tracker.
        last_out = None

        while ptr < end:
            args: list[str]
            operation, *args = instructions[ptr]

            if operation == OP_CPY:
                register[args[1]] = value(args[0])
                multiply()
            elif operation == OP_INC:
                register[args[0]] += 1
            elif operation == OP_DEC:
                decrement_or_addition()
            elif operation == OP_JNZ:
                if value(args[0]) != 0:
                    ptr += value(args[1]) - 1
            elif operation == OP_OUT:
                out = value(args[0])
                if last_out is None:
                    last_out = out
                elif 1 - out != last_out:
                    # If we generate the wrong signal, abort.
                    return register["a"], False
                else:
                    # Track the output signal.
                    last_out = out
                    # Check for a cycle.
                    new_state = state()
                    if new_state in prior_states:
                        return register["a"], True
                    prior_states.add(new_state)
            elif operation == OP_TGL:
                loc = ptr + value(args[0])
                if 0 <= loc < end:
                    old = instructions[loc]
                    default, alts = TOGGLE[len(old) - 1]
                    old[0] = alts.get(old[0], default)
            # case _:
            #     raise RuntimeError(f"Could not parse {instructions[ptr]}")
            ptr += 1

        return register["a"], False
