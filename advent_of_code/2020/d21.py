#!/usr/bin/env python
"""AoC Day 21: Allergen Assessment."""


def allergen_to_food(data: list[tuple[list[str], list[str]]]) -> dict[str, str]:
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
                candidates[allergen] = set(ingredients)    # Copy the set.
            else:
                candidates[allergen] &= set(ingredients)

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


def solve(data: list[tuple[list[str], list[str]]], part: int) -> int | str:
    """Determine food allergens."""
    solved = allergen_to_food(data)
    if part == 1:
        # Count the ingredients (including repeats) of food without allergens.
        all_ingredients = [b for line in data for b in line[0]]
        bad_ingredients = solved.values()
        return sum(True for i in all_ingredients if i not in bad_ingredients)
    # Return the foods containing allergens, sorted by allergen.
    return ",".join(solved[i] for i in sorted(solved.keys()))


def input_parser(puzzle_input: str):
    """Parse input lines into tuple(list[ingredients], list[allergens])."""
    out = []
    for line in puzzle_input.splitlines():
        ingredients_raw, allergens_raw = line.split(' (contains ')
        ingredients = ingredients_raw.split(' ')
        allergens = allergens_raw[:-1].split(', ')
        out.append((set(ingredients), set(allergens)))
    return out


SAMPLE = """\
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""
TESTS = [(1, SAMPLE, 5), (2, SAMPLE, 'mxmxvkd,sqjhc,fvjkl')]
