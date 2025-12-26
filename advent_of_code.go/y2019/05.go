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
	i, o:= make(chan int, 1), make(chan int, 1)
	ic := NewIntCode(data, IO(i, o))
	go ic.run()
	if part == 1 {
		i <- 1
	} else {
		i <- 5
	}
	var output int
	for {
		select {
		case v := <-o:
			output = v
		case <-time.After(100 * time.Millisecond):
			if ic.state == StateHalt {
				return helpers.Itoa(output)
			}
		}
	}
	return helpers.Itoa(output)
}

func init() {
	helpers.AocRegister(2019, 5, &Day05{})
}
