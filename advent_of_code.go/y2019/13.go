package y2019

import (
	"isaacgood.com/aoc/helpers"
)

// Day 13 solves 2019/13.
type Day13 struct {}

func (q *Day13) read(ic *IntCode, o <-chan int) int {
	v := <- o
	ic.run()
	return v
}

// Solve returns the solution for one part.
func (q *Day13) Solve(data string, part int) string {

	i, o := make(chan int, 1), make(chan int, 1)
	ic := NewIntCode(data, IO(i, o), Synchronous())
	if part == 2 {
		ic.mem[0] = 2
	}

	var ball, paddle, score = 0, 0, 0
	blocks := make(map[[2]int]int)
	for ic.state != StateHalt {
		ic.run()
		for ic.state != StateBlockInput && ic.state != StateHalt {
			x := q.read(ic, o)
			y := q.read(ic, o)
			tileType := q.read(ic, o)
			if tileType == 2 {
				blocks[[2]int{x, y}] = 1
			} else if x == -1 && y == 0 {
				score = tileType
			} else {
				if tileType == 3 {
					paddle = x
				} else if tileType == 4 {
					ball = x
				}
				delete(blocks, [2]int{x, y})
			}
		}
		if part == 1 {
			return helpers.Itoa(len(blocks))
		}
		if len(blocks) == 0 {
			return helpers.Itoa(score)
		}
		if paddle == ball {
			i <- 0
		} else if paddle > ball {
			i <- -1
		} else {
			i <- 1
		}
	}
	return ""
}

func init() {
	helpers.AocRegister(2019, 13, &Day13{})
}
