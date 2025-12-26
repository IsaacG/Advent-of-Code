package y2019

import (
	"isaacgood.com/aoc/helpers"
	"time"
)

// Day 13 solves 2019/13.
type Day13 struct {
}

// Solve returns the solution for one part.
func (q *Day13) Solve(data string, part int) string {
	blocks := make(map[[2]int]int)

	i, o := make(chan int), make(chan int)
	ic := NewIntCode(data, false, i, o)
	if part == 2 {
		ic.mem[0] = 2
	}
	go ic.run()

	var ball, paddle, score = 0, 0, 0
	for ic.state != StateHalt {
		for ic.state != StateHalt {
			x, ok := read(o, 2*time.Millisecond)
			if !ok {
				break
			}
			y, tileType := <-o, <-o
			if part == 1 && tileType == 2 {  // block
				blocks[[2]int{x, y}] = 1
			} else if tileType == 3 {
				paddle = x
			} else if tileType == 4 {
				ball = x
			} else if x == -1 && y == 0 {
				score = tileType
			}

		}
		if part == 1 {
			return helpers.Itoa(len(blocks))
		}
		if paddle == ball {
			if ok := write(i, 0, 10*time.Millisecond); !ok {
				break
			}
		} else if paddle > ball {
			if ok := write(i, -1, 10*time.Millisecond); !ok {
				break
			}
		} else {
			if ok := write(i, 1, 10*time.Millisecond); !ok {
				break
			}
		}
	}
	return helpers.Itoa(score)
}

func init() {
	helpers.AocRegister(2019, 13, &Day13{})
}
