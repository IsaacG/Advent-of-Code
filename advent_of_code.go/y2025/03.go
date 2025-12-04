package y2025

import (
	"strings"

	"isaacgood.com/aoc/helpers"
)

// Day03 solves 2025/03.
type Day03 struct {
	data string
}

func (p *Day03) max(line string) (rune, int) {
	max := '0'
	maxIdx := 0
	for idx, char := range line {
		if char > max {
			max = char
			maxIdx = idx
		}
	}
	return max, maxIdx
}

// Solve returns the solution for one part.
func (p *Day03) Solve(data string, part int) string {
	total := 0
	size := []int{2, 12}[part-1]
	for line := range strings.SplitSeq(data, "\n") {
		var digits []rune
		for i := -(size - 1); i <= 0; i++ {
			viable := line
			if i != 0 {
				viable = line[:len(line)+i]
			}
			max, idx := p.max(viable)
			digits = append(digits, max)
			line = line[idx+1:]
		}
		total += helpers.Atoi(string(digits))
	}
	return helpers.Itoa(total)
}

func init() {
	helpers.AocRegister(2025, 3, &Day03{})
}
