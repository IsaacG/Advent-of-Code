package y2025

import (
	"strings"
	"isaacgood.com/aoc/helpers"
)

// Day12 solves 2025/12.
type Day12 struct {
}

// Solve returns the solution for one part.
func (q *Day12) Solve(data string, part int) string {
	blocks := strings.Split(data, "\n\n")
	total := 0
	for _, line := range strings.Split(blocks[len(blocks)-1], "\n") {
		parts := strings.Split(line, ": ")
		areas := strings.Split(parts[0], "x")
		area := helpers.Atoi(areas[0]) * helpers.Atoi(areas[1])
		numGifts := 0
		for i := range strings.FieldsSeq(parts[1]) {
			numGifts += helpers.Atoi(i)
		}
		if area >= 9 * numGifts {
			total++
		}
	}
	return helpers.Itoa(total)
}

func init() {
	helpers.AocRegister(2025, 12, &Day12{})
}
