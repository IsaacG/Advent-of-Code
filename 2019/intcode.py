"""Intcode computer."""

import asyncio
import collections
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

    self.params = []
    for i, p in enumerate(instruction[1:]):
      mask = 10 ** (i + 2)
      param_mode = (self.op // mask) % 10
      if self._writes and i == self.len - 2:
        # If this instruction writes, the last param is a POS
        # but we are writing to it, not reading, so we do not
        # actually want to dereference it.
        assert param_mode != 1
        if param_mode == 0:
          self.params.append(p)
        elif param_mode == 2:
          self.params.append(self.comp.relative_base_offset + p)
      elif param_mode == 0:  # position mode
        self.params.append(self.read(p))
      elif param_mode == 1:  # immediate mode
        self.params.append(p)
      elif param_mode == 2:  # relative mode
        self.params.append(self.read(self.comp.relative_base_offset + p))
    assert all(isinstance(p, int) for p in self.params)

  def write_to(self, addr: int, val: int):
    """Write a value to a location specified by a parameter."""
    assert isinstance(val, int)
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
    return [self.memory[addr + n] for n in range(count)]

  async def pop_input(self) -> int:
    """Pop an input, reading the next input value."""
    return await asyncio.wait_for(self.comp._in.get(), timeout=2)

  async def push_output(self, val: int):
    """Push an output for future reading."""
    return await self.comp._out.put(val)

  def __str__(self):
    return '<OP[%02d] %-6s: %s>' % (self.ptr, type(self).__name__, ', '.join(str(i) for i in self.params))

  async def run(self):
    """Run an Instruction, executing it and updating the pointer."""
    assert all(i is not None for i in (self, self.params, self.execute))
    await self.execute(*self.params)
    self.comp.ptr += self.len


class Calculate(Operation):
  """Calculate operation.

  Length: 4.
  Execute: write_to(3, calculate(read_from(1), read_from(2)).
  Parameterized: calculate(a: int, b: int) -> int
  """

  _PARAMETER = 'calculate'

  async def calculate(self, a: int, b: int) -> int:
    return NotImplementedError

  async def execute(self, a, b, dest):
    val = await self.calculate(a, b)
    assert isinstance(val, int), self
    self.write_to(dest, val)


def make_op(name: str, opcode: int, length: int, base: type = Operation, writes: bool = False):
  """Register an Operation.

  Use Python magic to dynamically create a class.
  This class will be an Operation with a given name, length and execute.
  """
  def register(func):
    OPS[opcode] = type(name, (base, ), {base._PARAMETER: func, '_LEN': length, '_writes': writes})
  return register


@make_op('Add', opcode=1, length=4, base=Calculate, writes=True)
async def _operation_add(self, a: int, b: int) -> int:
  return a + b


@make_op('Mult', opcode=2, length=4, base=Calculate, writes=True)
async def _operation_mult(self, a: int, b: int) -> int:
  return a * b


@make_op('Input', opcode=3, length=2, writes=True)
async def _operation_input(self, addr):
  self.write_to(addr, await self.pop_input())


@make_op('Output', opcode=4, length=2)
async def _operation_output(self, val):
  assert isinstance(val, int)
  await self.push_output(val)


@make_op('JumpIfTrue', opcode=5, length=3)
async def _operation_jump_true(self, cond, addr):
  if cond:
    self.comp.ptr = addr - self.len


@make_op('JumpIfFalse', opcode=6, length=3)
async def _operation_jump_false(self, cond, addr):
  if not cond:
    self.comp.ptr = addr - self.len


@make_op('LessThan', opcode=7, length=4, base=Calculate, writes=True)
async def _operation_less_than(self, a: int, b: int) -> int:
  return 1 if a < b else 0


@make_op('Equals', opcode=8, length=4, base=Calculate, writes=True)
async def _operation_equals(self, a: int, b: int) -> int:
  return 1 if a == b else 0


@make_op('BaseOffset', opcode=9, length=2)
async def _operation_base_offset(self, val: int):
  self.comp.relative_base_offset += val


@make_op('Halt', opcode=99, length=1)
async def _operation_halt(self):
  self.comp.running = False


class Computer:
  """Intcode computer."""

  def __init__(self, memory: List[int]):
    """Initialize computer 'hardware'."""
    self.memory = collections.defaultdict(lambda: 0, enumerate(memory))
    self.ptr = 0
    self.relative_base_offset = 0

  def copy(self):
    """Return a copy of a Computer."""
    copy = type(self)([])
    copy.memory = self.memory.copy()
    return copy

  async def run(
    self,
    inputs: Iterable[int] = tuple(),
    io: Tuple[Optional[asyncio.Queue], Optional[asyncio.Queue]] = (None, None)
  ):
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
      assert op is not None
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
