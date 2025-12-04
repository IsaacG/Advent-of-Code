package y2017

import "isaacgood.com/aoc/helpers"

// Day01 solves 2017/01.
type Day01 struct{}

// Solve returns the solution for one part.
func (p *Day01) Solve(data string, part int) string {
	total := 0
	length := len(data)
	offset := []int{1, length / 2}[part-1]
	for i := range length {
		if data[i] == data[(i+offset)%length] {
			total += helpers.Atoi(string(data[i]))
		}
	}
	return helpers.Itoa(total)
}

func init() {
	helpers.AocRegister(2017, 1, &Day01{})
}
