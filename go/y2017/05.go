package y2017

import "slices"
import "isaacgood.com/aoc/helpers"

// Day05 solves 2017/05.
type Day05 struct {
	data []int
	size int
}

// New05 returns a new solver for 2017/05.
func New05() *Day05 {
	return &Day05{}
}

// SetInput handles input for this solver.
func (p *Day05) SetInput(data string) {
	p.data = helpers.ParseOneNumberPerLine(data)
	p.size = len(p.data)
}

// Solve returns the solution for one part.
func (p *Day05) Solve(part int) string {
	mem := slices.Clone(p.data)
	step := 0
	for ptr := 0; 0 <= ptr && ptr < p.size; step++ {
		offset := mem[ptr]
		if part == 1 && offset >= 3 {
			mem[ptr]--
		} else {
			mem[ptr]++
		}
		ptr += offset
	}
	return helpers.Itoa(step)
}
