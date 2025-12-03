package y2025

import (
	"strings"

	"isaacgood.com/aoc/helpers"
)

// Day03 solves 2025/03.
type Day03 struct {
	data string
}

// New03 returns a new solver for 2025/03.
func New03() *Day03 {
	return &Day03{}
}

// SetInput handles input for this solver.
func (p *Day03) SetInput(data string) {
	p.data = data
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
func (p *Day03) Solve(part int) string {
	total := 0
	size := []int{2, 12}[part]
	for line := range strings.SplitSeq(p.data, "\n") {
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
