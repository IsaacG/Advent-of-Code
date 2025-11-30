package e2025

import (
	// "fmt"
	// "slices"
	"strings"

	sets "github.com/deckarep/golang-set/v2"
	"isaacgood.com/everybodycodes/helpers"
)

// Quest14 for Event 2025.
type Quest14 struct {
	boardSize int
	maxCoord  int
}

// We test diagonal adjacencies.
var adjacents = [4][2]int{{1, 1}, {1, -1}, {-1, 1}, {-1, -1}}

// neighbors returns the number of active diagonal-adjacent neighbors.
func (q Quest14) neighbors(coord [2]int, active sets.Set[[2]int]) int {
	out := 0
	for _, adjacent := range adjacents {
		new := [2]int{coord[0] + adjacent[0], coord[1] + adjacent[1]}
		if active.Contains(new) {
			out++
		}
	}
	return out
}

// Solve Quest 14.
func (q Quest14) Solve(data string, part int) string {
	// Parse the input and set up variables.
	inputSize := len(strings.Split(data, "\n"))
	boardSize := inputSize

	offset := 0
	if part == 3 {
		boardSize = 34
		offset = (boardSize - inputSize) / 2
	}
	q.boardSize = boardSize
	q.maxCoord = boardSize - 1
	inputOn := sets.NewSet[[2]int]()
	inputOff := sets.NewSet[[2]int]()

	for y, line := range strings.Split(data, "\n") {
		for x, char := range line {
			if char == '#' {
				inputOn.Add([2]int{x + offset, y + offset})
			} else {
				inputOff.Add([2]int{x + offset, y + offset})
			}
		}
	}

	// Initial state.
	active := sets.NewSet[[2]int]()
	if part != 3 {
		active = inputOn
	}
	countAt := make(map[int]int)
	seen := make(map[sets.Set[[2]int]]int)

	// Simulate the game.
	count := 0
	steps := []int{10, 2025, 1000000000}[part-1]
	for step := range steps {
		// Compute the new active set.
		new := sets.NewSet[[2]int]()
		for x := range boardSize {
			for y := range boardSize {
				coord := [2]int{x, y}
				if active.Contains(coord) == ((q.neighbors(coord, active) % 2) == 1) {
					new.Add(coord)
				}
			}
		}
		active = new

		if part != 3 {
			count += active.Cardinality()
		} else if inputOn.IsSubset(active) && inputOff.Intersect(active).IsEmpty() {
			countAt[step] = active.Cardinality()
			// Check for a cycle.
			repeats, cycleStart := false, 0
			for prior := range seen {
				if active.Equal(prior) {
					cycleStart, repeats = seen[prior]
					break
				}
			}
			// On a cycle, compute the total.
			if repeats {
				cycle := step - cycleStart
				// Collect all steps at which the pattern appears.
				allMatchingSteps := sets.NewSet[int]()
				for priorStep := range countAt {
					if priorStep >= cycleStart {
						for i := priorStep; i < steps; i += cycle {
							allMatchingSteps.Add(i)
						}
					}
				}
				// Sum up the tiles when the pattern appears.
				out := 0
				for step := range allMatchingSteps.Iter() {
					out += countAt[((step-cycleStart)%cycle)+cycleStart]
				}
				return helpers.Itoa(out)
			}
			seen[active] = step
		}
	}
	return helpers.Itoa(count)
}

func init() {
	Puzzles[14] = Quest14{}
}
