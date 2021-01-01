"""Intcode computer."""

import asyncio
import enum
import more_itertools
from typing import Iterable, List, Optional, Tuple

from lib import aoc


class ParameterMode(enum.IntEnum):
  POS = 0  # Position Mode
  IMM = 1  # Immediate Mode


OPS = {}


class Operation:
  """Base Operation class."""

  _PARAMETER = 'execute'

  def __init__(self, comp: 'Computer'):
    self.comp = comp
    self.ptr = comp.ptr
    self.memory = comp.memory

    param_count = self.len - 1
    instruction = self.read_n(comp.ptr, param_count + 1)
    self.op = instruction[0]
    self._params = instruction[1:]

  def param_mode(self, param: int) -> ParameterMode:
    mask = 10 ** (param + 1)
    param_mode = (self.op // mask) % 10
    return ParameterMode(param_mode)

  def read_from(self, param: int) -> int:
    """Read a value specified by a given parameter.

    Based on the op mask, the value might be read in position mode or immediate mode.
    """
    if self.param_mode(param) == ParameterMode['POS']:  # position mode
      assert isinstance(self.read(self._params[param - 1]), int)
      return self.read(self._params[param - 1])
    else:  # 1 == immediate mode
      assert isinstance(self._params[param - 1], int)
      return self._params[param - 1]

  def write_to(self, param: int, val: int):
    """Write a value to a location specified by a parameter."""
    assert isinstance(val, int)
    addr = self._params[param - 1]
    self.memory[addr] = val

  @property
  def len(self):
    return self._LEN

  def read(self, addr: int) -> int:
    """Read one value from mem[addr]."""
    assert isinstance(self.memory[addr], int)
    return self.memory[addr]

  def read_n(self, addr: int, count: int) -> List[int]:
    """Read N values from mem[addr]."""
    return self.memory[addr:addr + count]

  async def pop_input(self) -> int:
    """Pop an input, reading the next input value."""
    return await self.comp._in.get()

  async def push_output(self, val: int):
    """Push an output for future reading."""
    return await self.comp._out.put(val)

  def __str__(self):
    return '<OP[%02d] %-6s: %s>' % (
      self.ptr,
      type(self).__name__,
      ', '.join(f'{self.param_mode(i).name}!{i}' for i in self._params)
    )

  async def run(self):
    """Run an Instruction, executing it and updating the pointer."""
    await self.execute()
    self.comp.ptr += self.len


class Calculate(Operation):
  """Calculate operation.

  Length: 4.
  Execute: write_to(3, calculate(read_from(1), read_from(2)).
  Parameterized: calculate(a: int, b: int) -> int
  """

  _PARAMETER = 'calculate'

  def calculate(self, a: int, b: int) -> int:
    return NotImplementedError

  async def execute(self):
    val = self.calculate(self.read_from(1), self.read_from(2))
    assert isinstance(val, int), self
    self.write_to(3, val)


def make_op(name: str, opcode: int, length: int, base: type = Operation):
  """Register an Operation.

  Use Python magic to dynamically create a class.
  This class will be an Operation with a given name, length and execute.
  """
  def register(func):
    OPS[opcode] = type(name, (base, ), {base._PARAMETER: func, '_LEN': length})
  return register


@make_op('Add', opcode=1, length=4, base=Calculate)
def _operation_add(self, a: int, b: int) -> int:
  return a + b


@make_op('Mult', opcode=2, length=4, base=Calculate)
def _operation_mult(self, a: int, b: int) -> int:
  return a * b


@make_op('Input', opcode=3, length=2)
async def _operation_input(self):
  self.write_to(1, await self.pop_input())


@make_op('Output', opcode=4, length=2)
async def _operation_output(self):
  assert isinstance(self.read_from(1), int)
  await self.push_output(self.read_from(1))


@make_op('JumpIfTrue', opcode=5, length=3)
async def _operation_jump_true(self):
  if self.read_from(1):
    self.comp.ptr = self.read_from(2) - self.len


@make_op('JumpIfFalse', opcode=6, length=3)
async def _operation_jump_false(self):
  if not self.read_from(1):
    self.comp.ptr = self.read_from(2) - self.len


@make_op('LessThan', opcode=7, length=4, base=Calculate)
def _operation_less_than(self, a: int, b: int) -> int:
  return 1 if self.read_from(1) < self.read_from(2) else 0


@make_op('Equals', opcode=8, length=4, base=Calculate)
def _operation_equals(self, a: int, b: int) -> int:
  return 1 if self.read_from(1) == self.read_from(2) else 0


@make_op('Halt', opcode=99, length=1)
async def _operation_halt(self):
  self.comp.running = False


class Computer:
  """Intcode computer."""

  def __init__(self, memory: List[int]):
    """Initialize computer 'hardware'."""
    self.memory = list(memory)
    self.ptr = 0

  def copy(self):
    """Return a copy of a Computer."""
    return type(self)(self.memory)

  async def run(self, inputs: Iterable[int] = tuple(), io: Tuple[Optional[asyncio.Queue], Optional[asyncio.Queue]] = (None, None)):
    """Run the program until Halted and return mem[0]."""
    i, o = io
    self._in = i if i else asyncio.Queue()
    self._out = o if o else asyncio.Queue()
    assert isinstance(self._in, asyncio.Queue)
    assert isinstance(self._out, asyncio.Queue)

    for i in inputs:
      self._in.put_nowait(i)
    self.running = True
    while self.running:
      op_type = self.memory[self.ptr] % 100
      op = OPS[op_type](self)
      await op.run()

  def output(self):
    out = []
    while not self._out.empty():
      out.append(self._out.get_nowait())
    return out

  def pretty_mem(self):
    """Pretty print the memory."""
    for chunk in more_itertools.ichunked(enumerate(self.memory), 16):
      chunk = list(chunk)
      print('Addr:', '  '.join(f'{c[0]:02d}' for c in chunk))
      print('Vals:', '  '.join(f'{c[1]:02d}' for c in chunk))


class Challenge(aoc.Challenge):
  """AOC Intcode Computer Challenge."""

  def preparse_input(self, x: List[str]) -> Computer:
    """Return a Computer using the first line of input as the program."""
    memory = [int(num) for num in x[0].split(',')]
    return Computer(memory)
