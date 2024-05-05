#!/bin/python
"""Day 14: Space Stoichiometry.

Handle chemical reactions, converting ORE to FUEL.
"""

import collections
import math
from typing import Dict, List, Set, Tuple

import data
from lib import aoc

SAMPLE = data.D14
TRILLION = int(1e12)


class Reaction:
  """Wrapper around a single reaction."""

  def __init__(self, product: Tuple[int, str], reactants: List[Tuple[int, str]]):
    self._reactants = reactants
    self.product_amt, self.product = product
    self.reactants = {r[1] for r in self._reactants}

  def needed(self, count: int) -> Tuple[List[Tuple[int, str]], int]:
    """Calculate much of of each reactant is needed to make `count` product.

    Returns the reactants needed and the amount of product produced.
    """
    factor = math.ceil(count / self.product_amt)
    return [(factor * c, e) for c, e in self._reactants], factor * self.product_amt


class Day14(aoc.Challenge):

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=165),
    aoc.TestCase(inputs=SAMPLE[1], part=1, want=13312),
    aoc.TestCase(inputs=SAMPLE[2], part=1, want=180697),
    aoc.TestCase(inputs=SAMPLE[3], part=1, want=2210736),
    aoc.TestCase(inputs=SAMPLE[1], part=2, want=82892753),
    aoc.TestCase(inputs=SAMPLE[2], part=2, want=5586022),
    aoc.TestCase(inputs=SAMPLE[3], part=2, want=460664),
  )

  def part1(self, reactions: Dict[str, Reaction]) -> int:
    """Calculate how much ore is needed for 1 unit of fuel."""
    return self.ore_per_fuel(reactions, 1)

  def part2(self, reactions: Dict[str, Reaction]) -> int:
    """Determine how much fuel can be made with 1e12 ore.

    Use the `ore_per_fuel()` function to binary search from 0 to 2e12 / ore_per_fuel(1).
    """
    low, high = 1, 2 * TRILLION // self.ore_per_fuel(reactions, 1)
    while (high - low) > 1:
      mid = (low + high) // 2
      ore = self.ore_per_fuel(reactions, mid)
      if ore == TRILLION:
        # Unlikely to occur but it doesn't hurt to be safe.
        return mid
      elif ore > TRILLION:
        high = mid
      else:
        low = mid
    return low

  def part2_via_reactions(self, reactions: Dict[str, Reaction]) -> int:
    """Solve part2 by actually running reactions until we run out of ore."""
    # Track inventory of products as we run reactions and have leftovers.
    inventory = {product: 0 for product in reactions}
    inventory['ORE'] = TRILLION

    def react(product: str, amount: int, inv: Dict[str, int]) -> bool:
      """Run a reaction to produce `amount` of `product` using mutatable inventory `inv`.

      Returns a bool indicating if we can actually pull off the reaction. On False, `inv`
      is a bit trashed.
      """

      def _react(product, amount):
        """Closure on `inv` to avoid passing it around."""
        # If we do not have enough ore and are trying to produce some, this reaction fails.
        if product == 'ORE':
          return False

        needs, gets = reactions[product].needed(amount)

        # Produce all the needed reactants to run the reaction.
        # Some reactants might use up others to be formed, hence the loop.
        while any(inv[reactant] < uses for uses, reactant in needs):
          for uses, reactant in needs:
            if inv[reactant] >= uses:
              continue
            # We need more of this reactant. Try to produce it. Mutates `inv`.
            short = uses - inv[reactant]
            if not _react(reactant, short):
              return False

        # Mutate `inv` and run the reaction. Use up reactants, produce product.
        for uses, reactant in needs:
          inv[reactant] -= uses
        inv[product] += gets

        return True

      return _react(product, amount)

    # Try to produce fuel in large quantities at first.
    # Reduce reaction size as they fail.
    volume = TRILLION // self.part1(reactions)
    while True:
      # Since failed reactions mutate the inventory, first see if they will work
      # on a copy. Then actually update the inventory.
      if react('FUEL', volume, inventory.copy()):
        react('FUEL', volume, inventory)
      else:
        # Failed to produce 1 fuel. We are at the end.
        if volume == 1:
          return inventory['FUEL']
        volume = volume // 2 or 1

  def ore_per_fuel(self, reactions: Dict[str, Reaction], fuel: int) -> int:
    """Calculate how much ore is required to produce `fuel` units of fuel."""
    _dependencies = {'ORE': set()}  # type: Dict[str, Set[str]]

    def dependencies(product: str) -> Set[str]:
      """Compute *all* reactants (recursively) involved in producing `product`."""
      # Cache results for dynamic programming.
      if product not in _dependencies:
        # Collect all reactants ... recursively.
        deps = set(reactions[product].reactants)
        for reactant in list(deps):
          deps.update(dependencies(reactant))
        _dependencies[product] = deps
      return _dependencies[product]

    # Iteratively resolve all products to the reactants needed to produce them.
    # Stop when we get down to just ore.
    want = collections.defaultdict(int)
    want['FUEL'] = fuel
    while list(want.keys()) != ['ORE']:
      # Find all products which are not also reactants of other products.
      # If a product is also a reactant, we may need more of it so it cannot yet be solved.
      products = {r for r in want.keys() if not any(r in dependencies(other) for other in want)}
      for product in products:
        # Add all the required reactants to the want list and remove the product.
        for amount, reactant in reactions[product].needed(want[product])[0]:
          want[reactant] += amount
        del want[product]

    return want['ORE']

  def input_parser(self, puzzle_input: str) -> Dict[str, Reaction]:
    """Build a dictionary of material produced to Reaction."""
    reactions = {}  # type: Dict[str, Reaction]

    def to_tuple(pair: str) -> Tuple[int, str]:
      a, b = pair.split()
      return (int(a), b)

    for line in puzzle_input.splitlines():
      reactants, product = line.split('=>')
      reaction = Reaction(
        to_tuple(product),
        [to_tuple(p) for p in reactants.split(', ')],
      )
      reactions[reaction.product] = reaction
    return reactions
