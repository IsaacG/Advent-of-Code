package y2025

import (
	"isaacgood.com/aoc/helpers"
	"slices"
	"strings"
)

// Day05 solves 2025/05.
type Day05 struct{}

// Solve returns the solution for one part.
func (p *Day05) Solve(data string, part int) string {
	blocks := strings.Split(data, "\n\n")
	fresh := helpers.ParseMultiNumbersPerLine(strings.ReplaceAll(blocks[0], "-", " "))
	available := helpers.ParseOneNumberPerLine(blocks[1])

	var total int
	if part == 1 {
		total = helpers.SumIf(available, func(i int) bool {
			for _, f := range fresh {
				if f[0] <= i && i <= f[1] {
					return true
				}
			}
			return false
		})
		return helpers.Itoa(total)
	}

	slices.SortFunc(fresh, func(a, b []int) int {
		if a[0] != b[0] {
			return helpers.Cmp(a[0], b[0])
		}
		return helpers.Cmp(a[1], b[1])
	})

	open, closed := fresh[0][0], fresh[0][1]
	for _, pair := range fresh[1:] {
		if closed < pair[0] {
			total += 1 + closed - open
			open, closed = pair[0], pair[1]
		} else {
			closed = helpers.Max(closed, pair[1])
		}
	}
	total += 1 + closed - open

	return helpers.Itoa(total)
}

func init() {
	helpers.AocRegister(2025, 5, &Day05{})
}
