package e2025

import (
	// "math"
	"strings"

	"isaacgood.com/everybodycodes/helpers"
	//sets "github.com/deckarep/golang-set/v2"
)

const toLower = 'a' - 'A'

// Quest06 for Event 2025.
type Quest06 struct{}

// p12 solves parts 1 and 2.
func (q Quest06) p12(data string, part int) int {
	count := make(map[rune]int)
	total := 0
	for _, char := range data {
		if char < 'a' {
			count[char+toLower]++
		} else if char == 'a' || part == 2 {
			total += count[char]
		}
	}
	return total
}

// Solve Quest 6.
func (q Quest06) Solve(data string, part int) string {
	total := 0
	if part != 3 {
		return helpers.Itoa(q.p12(data, part))
	}

	// Middle blocks.
	triple := data + data + data
	for idx := len(data); idx < 2*len(data); idx++ {
		if triple[idx] >= 'a' {
			total += strings.Count(triple[idx-1000:idx+1000+1], strings.ToUpper(triple[idx:idx+1]))
		}
	}
	total *= 1000 - 2

	// Sides.
	double := data + data
	for idx := 0; idx < 2*len(data); idx++ {
		if double[idx] >= 'a' {
			total += strings.Count(double[Max(0, idx-1000):Min(idx+1000+1, len(double))], strings.ToUpper(double[idx:idx+1]))
		}
	}

	return helpers.Itoa(total)
}

func init() {
	Puzzles[6] = Quest06{}
}
