package e2025

import (
	// "fmt"
	// "slices"
	"strings"

	// sets "github.com/deckarep/golang-set/v2"
	"isaacgood.com/everybodycodes/helpers"
)

// Quest08 for Event 2025.
type Quest08 struct {}

// Solve Quest 8.
func (q Quest08) Solve(data string, part int) string {
	var numbers []int
	chords := make(map[[2]int]int)
	for i := range strings.SplitSeq(data, ",") {
		numbers = append(numbers, helpers.Atoi(i))
	}
	var lines [][2]int
	for idx := range len(numbers) - 1 {
		a, b := numbers[idx], numbers[idx+1]
		if a > b {
			a, b = b, a
		}
		// Ignore lines between adjacent nails; they play no role.
		if b - a != 1 {
			lines = append(lines, [2]int{a, b})
		}
		chords[[2]int{a, b}]++
	}

	nails := 32
	if part > 1 {
		nails = 256
	}

	total := 0
	for idx, line := range lines {
		a, b := line[0], line[1]
		if part == 1 {
			// Lines pass through the center if the start and end are opposite each other.
			if 2 * (b - a) == nails {
				total++
			}
		}
		if part == 2 {
			// For every line, check prior lines for a crossing.
			for otherIdx := range idx {
				c, d := lines[otherIdx][0], lines[otherIdx][1]
				// Find pairs of lines where they cross,
				// i.e. `a` is on one side of `c-d` and `b` is on the other side.
				if a != c && b != d && (c < a && a < d) != (c < b && b < d) {
					total++
				}
			}
		}
	}
	if part == 3 {
		for a := 1; a < nails; a++ {
			for b := a + 1; b <= nails; b++ {
				count := 0
				for line, times := range chords {
					c, d := line[0], line[1]
					if (a == c && b == d) || (a != c && b != d && (c < a && a < d) != (c < b && b < d)) {
						count += times
					}
				}
				if count > total {
					total = count
				}
			}
		}
	}
	return helpers.Itoa(total)
}
