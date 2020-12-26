#!/usr/bin/env pypy

import typer
from typing import Dict, List, Tuple
from lib import aoc

SAMPLE = ["""\
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
"""]


class Day21(aoc.Challenge):

  TIMER_ITERATIONS = (20000, 200000)

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=5),
    aoc.TestCase(inputs=SAMPLE[0], part=2, want='mxmxvkd,sqjhc,fvjkl'),
  )

  def allergen_to_food(self, data: List[Tuple[List[str], List[str]]]) -> Dict[str, str]:
    """Map allergens to the ingredient that contains it.

    Map an allergen to a list of potential ingredients and pair down that list until
    it contains exactly one ingredient.
    """
    solved = {}

    # Map allergens to the intersections of candidates.
    candidates = {}
    for pair in data:
      ingredients, allergens = pair
      for allergen in allergens:
        if allergen not in candidates:
          candidates[allergen] = set(ingredients)  # Copy the set.
        else:
          candidates[allergen] &= ingredients

    # Pair up allergens to ingredients and remove candidates.
    while candidates:
      # Find an allergen with only one candidate.
      allergen, foods = [(i, j) for i, j in candidates.items() if len(j) == 1][0]
      food = foods.pop()
      solved[allergen] = food
      # Drop the candidate and remove the ingredient from all other candidate lists.
      del candidates[allergen]
      for i in candidates.values():
        if food in i:
          i.remove(food)
    return solved

  def part1(self, data: List[Tuple[List[str], List[str]]]) -> int:
    """Count the ingredients (including repeats) of food without allergens."""
    solved = self.allergen_to_food(data)
    all_ingredients = [b for line in data for b in line[0]]
    bad_ingredients = solved.values()
    return sum(True for i in all_ingredients if i not in bad_ingredients)

  def part2(self, data: List[Tuple[List[str], List[str]]]) -> str:
    """Return the foods containing allergens, sorted by allergen."""
    solved = self.allergen_to_food(data)
    return ",".join(solved[i] for i in sorted(solved.keys()))

  def preparse_input(self, lines):
    """Parse input lines into tuple(list[ingredients], list[allergens])."""
    out = []
    for line in lines:
      ingredients, allergens = line.split(' (contains ')
      ingredients = ingredients.split(' ')
      allergens = allergens[:-1].split(', ')
      out.append((set(ingredients), set(allergens)))
    return out


if __name__ == '__main__':
  typer.run(Day21().run)

# vim:ts=2:sw=2:expandtab
