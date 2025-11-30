package e2025

import (
	"slices"
	"strings"

	sets "github.com/deckarep/golang-set/v2"
	"isaacgood.com/everybodycodes/helpers"
)

// Quest03 for Event 2025.
type Quest03 struct{}

// Solve Quest 3.
func (q Quest03) Solve(data string, part int) string {
	var numbers []int
	for i := range strings.SplitSeq(data, ",") {
		numbers = append(numbers, helpers.Atoi(i))
	}
	if part != 3 {
		set := sets.NewSet[int](numbers...)
		numbers = set.ToSlice()
		if part == 2 {
			slices.Sort(numbers)
			numbers = numbers[:20]
		}
		return helpers.Itoa(Sum(numbers))
	}
	count := make(map[int]int)
	most := 0
	for _, i := range numbers {
		count[i]++
		if count[i] > most {
			most = count[i]
		}
	}
	return helpers.Itoa(most)
}

func init() {
	Puzzles[3] = Quest03{}
}
