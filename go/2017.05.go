package main

import "slices"

// P201705 solves 2017/05.
type P201705 struct {
	data []int
	size int
}

// New201705 returns a new solver for 2017/05.
func New201705() *P201705 {
	return &P201705{}
}

// SetInput handles input for this solver.
func (p *P201705) SetInput(data string) {
	p.data = ParseOneNumberPerLine(data)
	p.size = len(p.data)
}

// Solve returns the solution for one part.
func (p *P201705) Solve(part int) string {
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
	return Itoa(step)
}
