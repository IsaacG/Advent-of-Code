"""Intcode computer."""

import collections
from typing import List


_OPS = {}


def register_op(code: int, length: int):
  """Register an Operation."""
  def register(klass):
    _OPS[code] = klass
    klass._LEN = length
    return klass
  return register


class Operation:
  """Base Operation class."""

  def __init__(self, comp: 'Intcode'):
    self.comp = comp
    self.ptr = comp.ptr

    param_count = self.len - 1
    instruction = self.comp.read_n(comp.ptr, param_count + 1)
    self.op = instruction[0]
    params = instruction[1:]
    self._params = params

  def read_from(self, param: int) -> int:
    mask = 10 ** (param + 1)
    param_mode = (self.op // mask) % 10
    if param_mode == 0:  # position mode
      return self.comp.read(self._params[param - 1])
    else:  # 1 == immediate mode
      return self._params[param - 1]

  def write_to(self, param: int, val: int):
    self.comp.write(self._params[param - 1], val)

  @property
  def len(self):
    return self._LEN

  def write(self, *args, **kwargs):
    return self.comp.write(*args, **kwargs)

  def read(self, *args, **kwargs):
    return self.comp.read(*args, **kwargs)

  def read_n(self, *args, **kwargs):
    return self.comp.read_n(*args, **kwargs)

  def pop_input(self) -> int:
    return self.comp.inputs.popleft()

  def push_output(self, val: int):
    return self.comp.outputs.append(val)

  def __str__(self):
    return '<OP[%s] %s: %s>' % (
      self.ptr,
      type(self).__name__,
      ', '.join(str(i) for i in self._params)
    )


@register_op(1, 4)
class Add(Operation):
  """Add operation."""

  def run(self):
    val = self.read_from(1) + self.read_from(2)
    self.write_to(3, val)


@register_op(2, 4)
class Mult(Operation):
  """Mult operation."""

  def run(self):
    val = self.read_from(1) * self.read_from(2)
    self.write_to(3, val)


@register_op(3, 2)
class Input(Operation):
  """Input operation."""

  def run(self):
    self.write_to(1, self.pop_input())


@register_op(4, 2)
class Output(Operation):
  """Input operation."""

  def run(self):
    self.push_output(self.read_from(1))


@register_op(99, 1)
class Halt(Operation):
  """Halt operation."""


class Intcode:
  """Intcode computer."""

  def __init__(self, memory: List[int], debug: bool = False):
    self.memory = list(memory)
    self.ptr = 0
    self.inputs = collections.deque()
    self.outputs = collections.deque()
    self.debug = debug

  def run(self):
    """Run the program until Half and return mem[0]."""
    op = self.next_op()
    while not isinstance(op, Halt):
      if self.debug:
        print(op)
        print(self.memory)
      op.run()
      op = self.next_op()
    return self.read(0)

  def next_op(self) -> Operation:
    """Return the next Operation."""
    instruction = self.memory[self.ptr] % 100
    op = _OPS[instruction](self)
    self.ptr += op.len
    return op

  def write(self, addr: int, val: int):
    """Write one value to mem[addr]."""
    self.memory[addr] = val

  def read(self, addr: int) -> int:
    """Read one value from mem[addr]."""
    return self.read_n(addr, 1)[0]

  def read_n(self, addr: int, count: int) -> List[int]:
    """Read N values from mem[addr]."""
    return self.memory[addr:addr + count]
