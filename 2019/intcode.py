"""Intcode computer."""

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

  @property
  def len(self):
    return self._LEN

  def params(self):
    return self.readN(self.ptr, self.len)[1:]

  def write(self, *args, **kwargs):
    return self.comp.write(*args, **kwargs)

  def read1(self, *args, **kwargs):
    return self.comp.read1(*args, **kwargs)

  def readN(self, *args, **kwargs):
    return self.comp.readN(*args, **kwargs)


@register_op(1, 4)
class Add(Operation):
  """Add operation."""

  def run(self):
    addrs = self.params()
    self.write(addrs[2], self.read1(addrs[0]) + self.read1(addrs[1]))


@register_op(2, 4)
class Mult(Operation):
  """Mult operation."""

  def run(self):
    addrs = self.params()
    self.write(addrs[2], self.read1(addrs[0]) * self.read1(addrs[1]))


@register_op(99, 1)
class Halt(Operation):
  """Halt operation."""


class Intcode:
  """Intcode computer."""

  def __init__(self, memory: List[int]):
    self.memory = list(memory)
    self.ptr = 0

  def run(self):
    """Run the program until Half and return mem[0]."""
    op = self.next_op()
    while not isinstance(op, Halt):
      op.run()
      op = self.next_op()
    return self.read1(0)

  def next_op(self) -> Operation:
    """Return the next Operation."""
    instruction = self.memory[self.ptr]
    op = _OPS[instruction](self)
    self.ptr += op.len
    return op

  def write(self, addr: int, val: int):
    """Write one value to mem[addr]."""
    self.memory[addr] = val

  def read1(self, addr: int) -> int:
    """Read one value from mem[addr]."""
    return self.readN(addr, 1)[0]

  def readN(self, addr: int, count: int) -> List[int]:
    """Read N values from mem[addr]."""
    return self.memory[addr:addr + count]
