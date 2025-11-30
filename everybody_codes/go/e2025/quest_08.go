package e2025

import (
	// "fmt"
	// "slices"
	"strings"

	// sets "github.com/deckarep/golang-set/v2"
	"isaacgood.com/everybodycodes/helpers"
)

// Quest08 for Event 2025.
type Quest08 struct{}

// Solve Quest 8.
func (q Quest08) Solve(data string, part int) string {
	nails := 32
	if part > 1 {
		nails = 256
	}

	var numbers []int
	for i := range strings.SplitSeq(data, ",") {
		numbers = append(numbers, helpers.Atoi(i)-1)
	}
	chords := make(map[int]map[int]int)
	for i := range nails {
		chords[i] = make(map[int]int)
	}
	var lines [][2]int

	for idx := range len(numbers) - 1 {
		a, b := numbers[idx], numbers[idx+1]
		if a > b {
			a, b = b, a
		}
		// Ignore lines between adjacent nails; they play no role.
		if b-a != 1 {
			lines = append(lines, [2]int{a, b})
		}
		chords[a][b]++
		chords[b][a]++
	}

	total := 0
	for idx, line := range lines {
		a, b := line[0], line[1]
		if part == 1 {
			// Lines pass through the center if the start and end are opposite each other.
			if 2*(b-a) == nails {
				total++
			}
		}
		if part == 2 {
			// For every line, check prior lines for a crossing.
			for otherIdx := range idx {
				c, d := lines[otherIdx][0], lines[otherIdx][1]
				// Find pairs of lines where they cross,
				// i.e. `a` is on one side of `c-d` and `b` is on the other side.
				if a != c && b != d && (c < a && a < d) != (c < b && b < d) {
					total++
				}
			}
		}
	}
	if part != 3 {
		return helpers.Itoa(total)
	}

	cumulative := make(map[int]map[int]int)
	for i := range nails {
		cumulative[i] = make(map[int]int)
		for j := i + 2; j < i+nails; j++ {
			cumulative[i][j%nails] = cumulative[i][(j-1)%nails] + chords[i][j%nails]
		}
	}

	most := 0
	for a := 0; a < nails-1; a++ {
		for b := a + 1; b < nails; b++ {
			count := chords[a][b]
			for i := a + 1; i < b; i++ {
				count += cumulative[i][(a-1)%nails] - cumulative[i][b]
			}
			most = Max(most, count)
		}
	}
	return helpers.Itoa(most)
}

func init() {
	Puzzles[8] = Quest08{}
}
