package y2019

import (
	"isaacgood.com/aoc/helpers"
	"time"
)

// Day005solves 2019/05.
type Day05 struct {
}

// Solve returns the solution for one part.
func (q *Day05) Solve(data string, part int) string {
	input, output := make(chan int, 1), make(chan int, 1)
	ic := NewIntCode(data, false, input, output)
	go ic.run()
	if part == 1 {
		input <- 1
	} else {
		input <- 5
	}
	var i int
	for {
		select {
		case v := <-output:
			i = v
		case <-time.After(100 * time.Millisecond):
			if ic.state == StateHalt {
				return helpers.Itoa(i)
			}
		}
	}
	return helpers.Itoa(i)
}

func init() {
	helpers.AocRegister(2019, 5, &Day05{})
}
