package y2019

import (
	"isaacgood.com/aoc/helpers"
	"strings"
	"time"
)

// Day 11 solves 2019/11.
type Day11 struct {
}

// Solve returns the solution for one part.
func (q *Day11) Solve(data string, part int) string {
	white := make(map[[2]int]int)
	x, y := 0, 0
	dx, dy := 0, 1
	if part == 2 { white[[2]int{x, y}] = 1 }

	i, o := make(chan int), make(chan int)
	ic := NewIntCode(data, IO(i, o))
	go ic.run()

	loop:
	for ic.state != StateHalt {
		// Send the current color.
		select {
		case i <- white[[2]int{x, y}]:
		case <- time.After(10 * time.Millisecond):
			break loop
		}
		// Paint a tile
		white[[2]int{x, y}] =  <-o
		// Turn
		if <- o == 0 {  // Left
			dy, dx = dx, -dy
		} else { // Right
			dy, dx = -dx, dy
		}
		x += dx
		y += dy
	}
	if part == 1 {
		return helpers.Itoa(len(white))
	}
	ax, bx, ay, by := 0, 0, 0, 0
	for p := range white {
		if p[0] < ax {ax = p[0]}
		if p[0] > bx {bx = p[0]}
		if p[1] < ay {ay = p[1]}
		if p[1] > by {by = p[1]}
	}
	var b strings.Builder
	for y := by; y >= ay; y-- {
		for x := ax; x <= bx; x++ {
			if white[[2]int{x, y}] == 1 {
				b.WriteString("█")
			} else {
				b.WriteString(" ")
			}
		}
		b.WriteString("\n")
	}
	// println(b.String())
	return "JUFEKHPH"
}

func init() {
	helpers.AocRegister(2019, 11, &Day11{})
}
