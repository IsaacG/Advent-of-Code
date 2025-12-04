package y2017

import "slices"
import "isaacgood.com/aoc/helpers"

// Day05 solves 2017/05.
type Day05 struct {
	data []int
	size int
}

// Solve returns the solution for one part.
func (p *Day05) Solve(data string, part int) string {
	p.data = helpers.ParseOneNumberPerLine(data)
	p.size = len(p.data)
	mem := slices.Clone(p.data)
	step := 0
	for ptr := 0; 0 <= ptr && ptr < p.size; step++ {
		offset := mem[ptr]
		if part == 2 && offset >= 3 {
			mem[ptr]--
		} else {
			mem[ptr]++
		}
		ptr += offset
	}
	return helpers.Itoa(step)
}

func init() {
	helpers.AocRegister(2017, 5, &Day05{})
}
