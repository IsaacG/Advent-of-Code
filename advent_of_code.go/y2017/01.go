package y2017

import "isaacgood.com/aoc/helpers"

// Day01 solves 2017/01.
type Day01 struct {
	data string
}

// New01 returns a new solver for 2017/01.
func New01() *Day01 {
	return &Day01{}
}

// SetInput handles input for this solver.
func (p *Day01) SetInput(data string) {
	p.data = data
}

// Solve returns the solution for one part.
func (p *Day01) Solve(part int) string {
	total := 0
	length := len(p.data)
	offset := []int{1, length / 2}[part]
	for i := range length {
		if p.data[i] == p.data[(i + offset) % length] {
			total += helpers.Atoi(string(p.data[i]))
		}
	}
	return helpers.Itoa(total)
}
