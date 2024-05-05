"""Intcode computer."""

import collections
import dataclasses
import enum
import operator
import more_itertools
from typing import Callable, Iterable

from lib import aoc


class State(enum.Enum):
    INIT = enum.auto()
    RUN  = enum.auto()
    STOP = enum.auto()


class OpCode(enum.IntEnum):
    ADD     =  1
    MUL     =  2
    INPUT   =  3
    OUTPUT  =  4
    J_TRUE  =  5  # jump if true
    J_FALSE =  6  # jump if false
    LT      =  7  # less than
    EQ      =  8  # equal
    STOP    = 99


class Computer:
    """Intcode computer."""

    def __init__(self, program: str):
        """Initialize computer 'hardware'."""
        self.memory = [int(num) for num in program.split(',')]
        self.ptr = 0
        self.io = collections.deque()
        self.state = State.INIT
        self.debug = False

        self._debug(program)

        self.operators = {
            OpCode.ADD:     (2, 1, operator.add,       self.store),
            OpCode.MUL:     (2, 1, operator.mul,       self.store),
            OpCode.INPUT:   (0, 1, self.io.popleft,    self.store),
            OpCode.OUTPUT:  (1, 0, lambda x: x,        self.io.append),
            OpCode.J_TRUE:  (1, 1, operator.truth,     self.jump),
            OpCode.J_FALSE: (1, 1, operator.not_,      self.jump),
            OpCode.LT:      (2, 1, operator.lt,        self.store),
            OpCode.EQ:      (2, 1, operator.eq,        self.store),
            OpCode.STOP:    (0, 0, lambda: State.STOP, self.set_state),
        }

    def __str__(self):
        """Pretty print the memory."""
        out = []
        for chunk in more_itertools.ichunked(enumerate(self.memory), 16):
            chunk = list(chunk)
            out.append('Addr:  ' + '  '.join(f'{c[0]:02d}' for c in chunk))
            out.append('Vals:  ' + '  '.join(f'{c[1]:02d}' for c in chunk))
        return "\n".join(out)

    def _debug(self, msg: str) -> None:
        if self.debug:
            print(msg)

    def get_next(self) -> int:
        """Read one value from ptr and increment ptr."""
        value = self.memory[self.ptr]
        self.ptr += 1
        return value

    def operand(self, immediate: bool) -> int:
        """Load a paramemter from ptr, either immediate or positional mode."""
        value = self.get_next()
        return value if immediate else self.memory[value]

    def set_state(self, state: State) -> None:
        self.state = state

    def jump(self, value: bool, target: int) -> None:
        """Conditionally set the ptr."""
        if value:
            self.ptr = target

    def store(self, value: int | bool, target: int) -> None:
        """Write a value to memory."""
        value = int(value)
        self.memory[target] = value
        # self._debug(f" ==> MEM[{target:2}] = {value}")

    def run(self):
        """Run a program until it stops."""
        self.state = State.RUN
        while self.state == State.RUN:
            self.step()

    def step(self):
        """Run one step."""
        op = self.get_next()
        param_modes, opcode_num = divmod(op, 100)

        # Read the operand values.
        opcode = OpCode(opcode_num)
        op_count_compute, op_count_act, compute, act = self.operators[opcode]

        operands = []
        for _ in range(op_count_compute):
            param_modes, this_mode = divmod(param_modes, 10)
            operands.append(self.operand(bool(this_mode)))
        if op_count_act:
            param_modes, this_mode = divmod(param_modes, 10)
            operands.append(self.operand(this_mode or act == self.store))  # store is always immediate mode.

        # op_str = f"{opcode.name}({', '.join(str(i) for i in operands[:op_count_compute])})"
        value = compute(*(operands[:op_count_compute]))
        values = [value] + operands[op_count_compute:]
        # self._debug(f"{op_str:>16} => {act.__name__}({values})")
        act(*values)

