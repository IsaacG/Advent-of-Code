package y2019

import (
	"isaacgood.com/aoc/helpers"
)

// Day02 solves 2019/02.
type Day02 struct {
}

func (q *Day02) run(data string, a, b int) int {
	ic := NewIntCode(data, false, nil, nil)
	ic.mem[1] = a
	ic.mem[2] = b
	ic.run()
	return ic.mem[0]
}

// Solve returns the solution for one part.
func (q *Day02) Solve(data string, part int) string {
	if part == 1 {
		return helpers.Itoa(q.run(data, 12, 2))
	}
	for a := 0; a < 100; a++ {
		for b := 0; b < 100; b++ {
			if q.run(data, a, b) == 19690720 {
				return helpers.Itoa(100*a + b)
			}
		}
	}
	return ""
}

func init() {
	helpers.AocRegister(2019, 2, &Day02{})
}
