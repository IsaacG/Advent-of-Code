package e2025

import (
	"isaacgood.com/everybodycodes/helpers"
	"strings"
)

// Quest01 for Event 2025.
type Quest01 struct{}

// Solve Quest 1.
func (q Quest01) Solve(data string, part int) string {
	lines := strings.Split(strings.TrimRight(data, "\n"), "\n\n")
	names := strings.Split(lines[0], ",")
	size := len(names)
	pointer := 0
	for instruction := range strings.SplitSeq(lines[1], ",") {
		direction := instruction[0]
		distance := helpers.Atoi(instruction[1:])
		if direction == 'R' {
			pointer += distance
		} else {
			pointer -= distance
		}
		if part == 1 {
			pointer = Clamp(0, pointer, size-1)
		} else if part == 3 {
			distance = distance % size
			if direction == 'L' {
				distance = size - distance
			}
			names[0], names[distance] = names[distance], names[0]
		}
	}
	if part == 2 {
		pointer = pointer % size
	} else if part == 3 {
		pointer = 0
	}
	return names[pointer]
}
