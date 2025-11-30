package e2025

import (
	"math"
	"strings"

	"isaacgood.com/everybodycodes/helpers"
	//sets "github.com/deckarep/golang-set/v2"
)

// Quest04 for Event 2025.
type Quest04 struct{}

// Solve Quest 4.
func (q Quest04) Solve(data string, part int) string {
	if part != 3 {
		var numbers []int
		for i := range strings.Lines(data) {
			numbers = append(numbers, helpers.Atoi(strings.TrimRight(i, "\n")))
		}
		if part == 1 {
			return helpers.Itoa(2025 * numbers[0] / numbers[len(numbers)-1])
		} else {
			return helpers.Itoa(int(math.Ceil(10000000000000. / (float64(numbers[0]) / float64(numbers[len(numbers)-1])))))
		}
	}
	var numbers [][2]float64
	for i := range strings.SplitSeq(data, "\n") {
		parts := strings.Split(i, "|")
		if len(parts) == 1 {
			parts = []string{parts[0], parts[0]}
		}
		numbers = append(numbers, [2]float64{float64(helpers.Atoi(parts[0])), float64(helpers.Atoi(parts[1]))})
	}
	ratio := 1.0
	for idx := range len(numbers) - 1 {
		ratio *= numbers[idx][1] / numbers[idx+1][0]
	}
	return helpers.Itoa(int(ratio * 100))
}

func init() {
	Puzzles[4] = Quest04{}
}
