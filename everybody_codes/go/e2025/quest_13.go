package e2025

import (
	// "fmt"
	"slices"
	"strings"

	// sets "github.com/deckarep/golang-set/v2"
	"isaacgood.com/everybodycodes/helpers"
)

// Quest13 for Event 2025.
type Quest13 struct{}

// Solve Quest 13.
func (q Quest13) Solve(data string, part int) string {
	var ranges [2][][2]int

	size := 1
	ranges[0] = append(ranges[0], [2]int{1, 1})

	for idx, line := range strings.Split(data, "\n") {
		var pair [2]int
		if part == 1 {
			num := helpers.Atoi(line)
			pair = [2]int{num, num}
		} else {
			nums := strings.Split(line, "-")
			if idx%2 == 0 {
				pair = [2]int{helpers.Atoi(nums[0]), helpers.Atoi(nums[1])}
			} else {
				pair = [2]int{helpers.Atoi(nums[1]), helpers.Atoi(nums[0])}
			}
		}
		ranges[idx%2] = append(ranges[idx%2], pair)
		size += Abs(pair[1]-pair[0]) + 1
	}

	offset := []int{2025, 20252025, 202520252025}[part-1] % size
	slices.Reverse(ranges[1])
	dial := slices.Concat(ranges[0], ranges[1])
	for _, pair := range dial {
		size = Abs(pair[1]-pair[0]) + 1
		if offset < size {
			direction := 1
			if pair[0] > pair[1] {
				direction = -1
			}
			return helpers.Itoa(pair[0] + direction*offset)
		}
		offset -= size
	}

	return ""
}

func init() {
	Puzzles[13] = Quest13{}
}
