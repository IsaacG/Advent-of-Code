#!/bin/pypy3
"""Train tickets."""

import typer
import aoc
import collections
import functools
import math
import re
from typing import Any, Callable, Dict, List

# Fudge the second sample to include departure rows
# so it would be valid input to part2.
SAMPLE = ["""\
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
""","""
departure class: 0-1 or 4-19
departure row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
"""]


class Day16(aoc.Challenge):
  """Day 16. Train tickets."""

  TRANSFORM = str
  SEP = '\n\n'
  TIMER_ITERATIONS = (1000, 1000)

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=71),
    aoc.TestCase(inputs=SAMPLE[1], part=2, want=132),
  )

  def preparse_input(self, chunks: List[str]):
    """Parse the input."""
    rules, your_ticket, nearby_tickets = chunks

    rule_by_name = {}
    for line in rules.split('\n'):
       name, l = line.split(': ')
       rule_by_name[name] = tuple(tuple(int(p) for p in o.split('-')) for o in l.split(' or '))
    # CSV data, one row (after the header).
    your_ticket = [int(i) for i in your_ticket.split('\n')[1].split(',')]
    # CSV data. Split in "\n" for a record, split record on "," for values.
    nearby_tickets = [[int(i) for i in line.split(',')] for line in nearby_tickets.split('\n')[1:]]

    return rule_by_name, your_ticket, nearby_tickets

  def part1(self, data) -> int:
    """Find bad fields."""
    rule_by_name, your_ticket, nearby_tickets = data
    # Bad fields are values that do not meet any rule.
    bad_values = [
      # Find all numbers on all tickets
      number for ticket in nearby_tickets for number in ticket
      if not any(
        # Where number does not satify any part of any rule.
        rule_part[0] <= number <= rule_part[1] for rule in rule_by_name.values() for rule_part in rule
      )
    ]
    return sum(bad_values)


  def part2(self, data) -> int:
    rule_by_name, your_ticket, nearby_tickets = data
    # Find good tickets.
    # Good tickets mean all values pass any part of any rules.
    nearby_tickets = [
      ticket
      for ticket in nearby_tickets
      if all(  # All numbers on the ticket
        any(   # pass any of the rules
          any( # by matching any part of the rule
            rule_part[0] <= number <= rule_part[1] for rule_part in rule
          )
          for rule in rule_by_name.values()
        )
        for number in ticket
      )
    ]
    # Construct a list of values in each column/field. Transpose the ticket info.
    col_values = [{ticket[n] for ticket in nearby_tickets} for n in range(len(nearby_tickets[0]))]

    # Fill out your ticket, mapping field name to value.
    completed_ticket = {}

    # Map each rule name to the columns that satisfy that rule.
    candidate_cols_for_rule = {
      rule_name: {
        c for c in range(len(rule_by_name))
        if all(  # All the column values pass
          any(   # any of the parts of the rule.
            rule_part[0] <= number <= rule_part[1] for rule_part in rule
          )
          for number in col_values[c]
        )
      }
      for rule_name, rule in rule_by_name.items()
    }

    # Match all rules to a column count until all rules are used up.
    while candidate_cols_for_rule:
      # Get the rule that can only be satisfied by one column.
      rule_with_one_candidate = [
        rule_name
        for rule_name, candidates in candidate_cols_for_rule.items()
        if len(candidates) == 1
      ]
      # It had better exist!
      assert len(rule_with_one_candidate) == 1
      rule_name = rule_with_one_candidate[0]

      # Get the column ID and drop the rule.
      column = candidate_cols_for_rule[rule_name].pop()
      del candidate_cols_for_rule[rule_name]

      # Update our ticket with the rule name and value.
      completed_ticket[rule_name] = your_ticket[column]

      # Drop the column we just used from the candidates. It's no longer available.
      for candidates in candidate_cols_for_rule.values():
        candidates.remove(column)

    # Multiply all the fields that start with "departure".
    return aoc.mult(v for k, v in completed_ticket.items() if k.startswith('departure'))


if __name__ == '__main__':
  typer.run(Day16().run)

# vim:ts=2:sw=2:expandtab
