package y2025

import (
	"strconv"
	"strings"

	"isaacgood.com/aoc/helpers"
)

// Day01 solves 2025/01.
type Day01 struct {
	turns [][2]int
}

// SetInput handles input for this solver.
func (p *Day01) SetInput(data string) {
	if p.turns != nil {
		return
	}
	for line := range strings.SplitSeq(data, "\n") {
		turn := helpers.Atoi(line[1:])
		step := 1
		if line[0] == 'L' {
			step = -1
		}
		p.turns = append(p.turns, [2]int{turn, step})
	}
}

// Solve returns the solution for one part.
func (p *Day01) Solve(data string, part int) string {
	p.SetInput(data)
	var clicks uint64
	position := 50
	for _, turn := range p.turns {
		step := turn[1]
		for i := 0; i < turn[0]; i++ {
			position += step
			if position%100 == 0 && part == 2 {
				clicks++
			}
		}
		if position%100 == 0 && part == 1 {
			clicks++
		}
	}
	return strconv.FormatUint(clicks, 10)
}

func init() {
	helpers.AocRegister(2025, 1, &Day01{})
}
