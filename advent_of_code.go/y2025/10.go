// Solve 2025 day 10 using the bifurcate approach.
// https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/
package y2025

import (
	"fmt"
	"maps"
	"slices"
	"strings"

	"isaacgood.com/aoc/helpers"
)

const inf = 10000000

// Day10 solves 2025/10.
type Day10 struct{}

// parseLine parses a line into the target (lights for p1, joltage for p2) and the button outputs.
func (q *Day10) parseLine(line string, part int) ([]int, [][]int) {
	var jolts []int
	var buttons [][]int
	firstSpace := strings.Index(line, " ")
	lastSpace := strings.LastIndex(line, " ")

	for _, group := range strings.Fields(line[firstSpace+1 : lastSpace]) {
		buttons = append(buttons, helpers.ParseOneLineMultiNumbers(strings.ReplaceAll(group[1:len(group)-1], ",", " ")))
	}
	if part == 1 {
		vals := strings.TrimSpace(strings.ReplaceAll(strings.ReplaceAll(line[1:firstSpace-1], "#", "1 "), ".", "0 "))
		jolts = helpers.ParseOneLineMultiNumbers(vals)
	} else {
		jolts = helpers.ParseOneLineMultiNumbers(strings.ReplaceAll(line[lastSpace+2:len(line)-1], ",", " "))
	}
	return jolts, buttons
}

// d10ButtonPushes contains the result of pushing multiple buttons (each button 0 or 1 time).
type d10ButtonPushes struct {
	counts []int
	pushes int
}

// d10ButtonCombiner is used to find all combinations of (0 or 1 each) button pushes.
type d10ButtonCombiner struct {
	buttons [][]int
	outputs int
}

// _getCombos is a recursive `itertools.combinations()` type function.
// It returns the possible combinations of button pushes.
func (bc d10ButtonCombiner) _getCombos(buttons [][]int) []d10ButtonPushes {
	if len(buttons) == 0 {
		return []d10ButtonPushes{{make([]int, bc.outputs), 0}}
	}
	subCombos := bc._getCombos(buttons[1:])
	// For each sub-combination, try with and without the first button pushed.
	withPush := make([]d10ButtonPushes, len(subCombos))
	for idx, push := range subCombos {
		pushed := &withPush[idx]
		pushed.pushes = push.pushes + 1
		pushed.counts = slices.Clone(push.counts)
		for _, button := range buttons[0] {
			pushed.counts[button]++
		}
	}

	return append(subCombos, withPush...)
}

// allCombos returns all combinations of button pushes.
// When different combinations have the same outputs, take the one with fewest pushes.
func (bc d10ButtonCombiner) allCombos(part int) []d10ButtonPushes {
	min := make(map[string]d10ButtonPushes)
	combos := bc._getCombos(bc.buttons)
	for _, push := range combos {
		// In part one we only care about the right most bit,
		// ie pushing (1) twice is the same as not pushing it.
		if part == 1 {
			for idx, count := range push.counts {
				push.counts[idx] = count % 2
			}
		}
		key := fmt.Sprintf("%v", push.counts)
		if prior, ok := min[key]; !ok || prior.pushes > push.pushes {
			min[key] = push
		}
	}
	return slices.Collect(maps.Values(min))
}

// solveOne returns the solution for one line.
func (q *Day10) solveOne(jolts []int, combos []d10ButtonPushes) int {
	outputs := len(jolts)

	// Solve recursively, one bit at a time.
	var recursive func(jolts []int) int
	cache := make(map[string]int)
	recursive = func(jolts []int) int {
		// Memoize the result.
		key := fmt.Sprintf("%v", jolts)
		if got, ok := cache[key]; ok {
			return got
		}
		// Stop when all outputs are zeroed out.
		if helpers.Sum(jolts) == 0 {
			return 0
		}
		// Find the best combination.
		best := inf
		for _, combo := range combos {
			remaining := make([]int, outputs)
			valid := true
			for idx, count := range combo.counts {
				// A combination is only valid if we get a non-negative remainder which is even.
				if r := jolts[idx] - count; r >= 0 && r%2 == 0 {
					remaining[idx] = r >> 1
				} else {
					valid = false
					break
				}
			}
			if !valid {
				continue
			}
			combinedSteps := combo.pushes + 2*recursive(remaining)
			if combinedSteps < best {
				best = combinedSteps
			}
		}
		cache[key] = best
		return best
	}
	return recursive(jolts)
}

// Solve returns the solution for one part.
func (q *Day10) Solve(data string, part int) string {
	total := 0
	for _, line := range strings.Split(data, "\n") {
		jolts, buttons := q.parseLine(line, part)
		combos := d10ButtonCombiner{buttons, len(jolts)}.allCombos(part)
		total += q.solveOne(jolts, combos)
	}
	return helpers.Itoa(total)
}

func init() {
	helpers.AocRegister(2025, 10, &Day10{})
}
