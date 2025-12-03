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

// New01 returns a new solver for 2025/01.
func New01() *Day01 {
	return &Day01{}
}

// SetInput handles input for this solver.
func (p *Day01) SetInput(data string) {
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
func (p *Day01) Solve(part int) string {
	var clicks uint64
	position := 50
	for _, turn := range p.turns {
		step := turn[1]
		for i := 0; i < turn[0]; i++ {
			position += step
			if position%100 == 0 && part == 1 {
				clicks++
			}
		}
		if position%100 == 0 && part == 0 {
			clicks++
		}
	}
	return strconv.FormatUint(clicks, 10)
}
