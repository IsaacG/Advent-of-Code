"""Intcode computer."""

import collections
import dataclasses
import enum
import operator
import more_itertools
from typing import Callable, Iterable

from lib import aoc


class State(enum.Enum):
    READY  = enum.auto()
    RUN    = enum.auto()
    IOWAIT = enum.auto()
    STOP   = enum.auto()


OP_CODE_ADD     =  1
OP_CODE_MUL     =  2
OP_CODE_INPUT   =  3
OP_CODE_OUTPUT  =  4
OP_CODE_J_TRUE  =  5  # jump if true
OP_CODE_J_FALSE =  6  # jump if false
OP_CODE_LT      =  7  # less than
OP_CODE_EQ      =  8  # equal
OP_CODE_RELBASE =  9  # set relative base
OP_CODE_STOP    = 99

OP_CODE_NAMES = {
    OP_CODE_ADD:     "ADD",
    OP_CODE_MUL:     "MUL",
    OP_CODE_INPUT:   "INPUT",
    OP_CODE_OUTPUT:  "OUTPUT",
    OP_CODE_J_TRUE:  "J_TRUE",
    OP_CODE_J_FALSE: "J_FALSE",
    OP_CODE_LT:      "LT",
    OP_CODE_EQ:      "EQ",
    OP_CODE_RELBASE: "RELBASE",
    OP_CODE_STOP:    "STOP",
}

PARAMETER_MODE_POSITIONAL = 0
PARAMETER_MODE_IMMEDIATE  = 1
PARAMETER_MODE_RELATIVE   = 2


class Computer:
    """Intcode computer."""

    def __init__(
        self,
        program: str,
        input_q: collections.deque | None = None,
        output_q: collections.deque | None = None,
        debug: bool = False,
    ):
        """Initialize computer 'hardware'."""
        if input_q is None:
            input_q = collections.deque()
        if output_q is None:
            output_q = collections.deque()

        self.input = input_q
        self.output = output_q
        self.program = dict(enumerate(int(i) for i in program.split(",")))
        self.reset()
        self.debug = debug

        self._debug(f"Program: {program}")

        self.operators = {
            OP_CODE_ADD:     (2, 1, operator.add,       self.store),
            OP_CODE_MUL:     (2, 1, operator.mul,       self.store),
            OP_CODE_INPUT:   (0, 1, self.get_input,     self.store),
            OP_CODE_OUTPUT:  (1, 0, lambda x: x,        self.output.append),
            OP_CODE_J_TRUE:  (1, 1, operator.truth,     self.jump),
            OP_CODE_J_FALSE: (1, 1, operator.not_,      self.jump),
            OP_CODE_LT:      (2, 1, operator.lt,        self.store),
            OP_CODE_EQ:      (2, 1, operator.eq,        self.store),
            OP_CODE_RELBASE: (1, 0, lambda x: x,        self.update_relative_base),
            OP_CODE_STOP:    (0, 0, lambda: State.STOP, self.set_state),
        }

    def reset(self) -> None:
        self.memory: dict[int, int] = collections.defaultdict(int)
        self.memory.update(self.program)
        self.ptr = 0
        self.relative_base = 0
        self.input.clear()
        self.output.clear()
        self.state = State.READY

    def __str__(self):
        """Pretty print the memory."""
        out = []
        for chunk in more_itertools.ichunked(enumerate(self.memory), 16):
            chunk = list(chunk)
            out.append("Addr:  " + "  ".join(f"{c[0]:02d}" for c in chunk))
            out.append("Vals:  " + "  ".join(f"{c[1]:02d}" for c in chunk))
        return "\n".join(out)

    def _debug(self, msg: str) -> None:
        if self.debug:
            print(msg)

    def get_input(self) -> int | None:
        """Read input or change state to blocked."""
        if self.input:
            return self.input.popleft()
        self.ptr -= 2
        self.set_state(State.IOWAIT)
        return None

    def get_next(self) -> int:
        """Read one value from ptr and increment ptr."""
        value = self.memory[self.ptr]
        self.ptr += 1
        return value

    def operand(self, param_mode: int) -> int:
        """Load a paramemter from ptr, either immediate or positional mode."""
        value = self.ptr
        self.ptr += 1
        if param_mode == PARAMETER_MODE_POSITIONAL:
            return self.memory[value]
        if param_mode == PARAMETER_MODE_IMMEDIATE:
            return value
        if param_mode == PARAMETER_MODE_RELATIVE:
            # self._debug(f"Look ip operand, {param_mode=}, {value=}, {self.relative_base=} {self.memory[value] + self.relative_base}")
            return self.memory[value] + self.relative_base
        raise ValueError(f"Invalid param mode, {param_mode}")

    @property
    def stopped(self) -> bool:
        return self.state == State.STOP

    def update_relative_base(self, value: int) -> None:
        self.relative_base += value

    def set_state(self, state: State) -> None:
        self.state = state

    def jump(self, value: bool, target: int) -> None:
        """Conditionally set the ptr."""
        if value:
            self.ptr = self.memory[target]

    def store(self, value: int | bool, target: int) -> None:
        """Write a value to memory."""
        if value is None:
            return
        value = int(value)
        self.memory[target] = value
        # self._debug(f" ==> MEM[{target:2}] = {value}")

    def run(self) -> None:
        """Run a program until it stops."""
        if self.state == State.IOWAIT and not self.input:
            return
        self.state = State.RUN
        while self.state == State.RUN:
            self.step()

    def step(self):
        """Run one step."""
        op = self.get_next()
        param_modes, opcode = divmod(op, 100)

        # Read the operand values.
        op_count_compute, op_count_act, compute, act = self.operators[opcode]

        compute_operands = []
        for _ in range(op_count_compute):
            param_modes, this_mode = divmod(param_modes, 10)
            compute_operands.append(self.memory[self.operand(this_mode)])

        act_operands = []
        for _ in range(op_count_act):
            param_modes, this_mode = divmod(param_modes, 10)
            act_operands.append(self.operand(this_mode))

        value = compute(*compute_operands)
        values = [value] + act_operands
        # op_str = f"{OP_CODE_NAMES[opcode]}({', '.join(str(i) for i in compute_operands)})"
        # self._debug(f"{op_str:>16} => {act.__name__}({values})")
        act(*values)

