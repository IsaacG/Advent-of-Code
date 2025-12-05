package e2025

import "isaacgood.com/everybodycodes/helpers"

// Solver is able to solve the puzzle for a day.
type Solver interface {
	Solve(string, int) string
}

var Puzzles = map[int]Solver{}

Clamp = helpers.Clamp
Sum = helpers.Sum
Max = helpers.Max
Min = helpers.Min
Abs = helpers.Abs
