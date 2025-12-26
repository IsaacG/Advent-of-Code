package y2019

import (
	"isaacgood.com/aoc/helpers"
)

// Day 09 solves 2019/09.
type Day09 struct {
}

// Solve returns the solution for one part.
func (q *Day09) Solve(data string, part int) string {
	i, o := make(chan int, 1), make(chan int)
	i <- part
	ic := NewIntCode(data, IO(i, o))
	go ic.run()
	return helpers.Itoa(<-o)
}

func init() {
	helpers.AocRegister(2019, 9, &Day09{})
}
