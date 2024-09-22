package main

// P201701 solves 2017/01.
type P201701 struct {
	data string
}

// New201701 returns a new solver for 2017/01.
func New201701() *P201701 {
	return &P201701{}
}

// SetInput handles input for this solver.
func (p *P201701) SetInput(data string) {
	p.data = data
}

// Solve returns the solution for one part.
func (p *P201701) Solve(part int) string {
	total := 0
	length := len(p.data)
	offset := []int{1, length / 2}[part]
	for i := range length {
		if p.data[i] == p.data[(i + offset) % length] {
			total += Atoi(string(p.data[i]))
		}
	}
	return Itoa(total)
}
