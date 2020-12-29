"""Intcode computer."""

import collections
from typing import Callable, List


OPS = {}


class Operation:
  """Base Operation class."""

  def __init__(self, comp: 'Computer'):
    self.comp = comp
    self.ptr = comp.ptr
    self.memory = comp.memory

    param_count = self.len - 1
    instruction = self.read_n(comp.ptr, param_count + 1)
    self.op = instruction[0]
    self._params = instruction[1:]

  def read_from(self, param: int) -> int:
    """Read a value specified by a given parameter.

    Based on the op mask, the value might be read in position mode or immediate mode.
    """
    mask = 10 ** (param + 1)
    param_mode = (self.op // mask) % 10
    if param_mode == 0:  # position mode
      return self.read(self._params[param - 1])
    else:  # 1 == immediate mode
      return self._params[param - 1]

  def write_to(self, param: int, val: int):
    """Write a value to a location specified by a parameter."""
    addr = self._params[param - 1]
    self.memory[addr] = val

  @property
  def len(self):
    return self._LEN

  def read(self, addr: int) -> int:
    """Read one value from mem[addr]."""
    return self.memory[addr]

  def read_n(self, addr: int, count: int) -> List[int]:
    """Read N values from mem[addr]."""
    return self.memory[addr:addr + count]

  def pop_input(self) -> int:
    """Pop an input, reading the next input value."""
    return self.comp.inputs.popleft()

  def push_output(self, val: int):
    """Push an output for future reading."""
    return self.comp.outputs.append(val)

  def __str__(self):
    return '<OP[%s] %s: %s>' % (
      self.ptr,
      type(self).__name__,
      ', '.join(str(i) for i in self._params)
    )

  def run(self):
    """Run an Instruction, executing it and updating the pointer."""
    self.execute()
    self.comp.ptr += self.len


def make_op(name: str, code: int, length: int, base: type = Operation):
  """Register an Operation.

  Use Python magic to dynamically create a class.
  This class will be an Operation with a given name, length and execute.
  """
  def register(func):
    OPS[code] = type(name, (base, ), {'execute': func, '_LEN': length})
  return register


@make_op('Add', 1, 4)
def _operation_add(self):
  val = self.read_from(1) + self.read_from(2)
  self.write_to(3, val)


@make_op('Mult', 2, 4)
def _operation_mult(self):
  val = self.read_from(1) * self.read_from(2)
  self.write_to(3, val)


@make_op('Input', 3, 2)
def _operation_input(self):
  self.write_to(1, self.pop_input())


@make_op('Output', 4, 2)
def _operation_output(self):
  self.push_output(self.read_from(1))


@make_op('Halt', 99, 1)
def _operation_halt(self):
  self.comp.running = False


class Computer:
  """Intcode computer."""

  def __init__(self, memory: List[int], debug: int = 0):
    """Initialize computer 'hardware'."""
    self.memory = list(memory)
    self.ptr = 0
    self.inputs = collections.deque()
    self.outputs = collections.deque()
    self.debug = debug

  def run(self):
    """Run the program until Halted and return mem[0]."""
    self.running = True
    while self.running:
      op_type = self.memory[self.ptr] % 100
      op = OPS[op_type](self)
      if self.debug:
        self.debug -= 1
        print(op)
        print(self.memory)
      op.run()
    return self.memory[0]
