package y2025

import (
	"strings"

	sets "github.com/deckarep/golang-set/v2"
	"isaacgood.com/aoc/helpers"
)

// Day04 solves 2025/04.
type Day04 struct{}

// Solve returns the solution for one part.
func (p *Day04) Solve(data string, part int) string {
	papers := sets.NewSet[helpers.Location]()
	for y, line := range strings.Split(data, "\n") {
		for x, char := range line {
			if char == '@' {
				papers.Add(helpers.Location{x, y})
			}
		}
	}

	// isPaper checks if a location contains paper.
	isPaper := func(neighbor helpers.Location) bool { return papers.Contains(neighbor) }
	// paperCanMove checks if paper has less than 4 neighbors and can move.
	paperCanMove := func(l helpers.Location) bool { return helpers.SumIf(l.AdjacentAll(), isPaper) < 4 }
	// canMove returns the set of papers that can be moved.
	canMove := func() sets.Set[helpers.Location] {
		canDo := sets.NewSet[helpers.Location]()
		helpers.ApplyIf(papers.ToSlice(), func(l helpers.Location) { canDo.Add(l) }, paperCanMove)
		return canDo
	}

	if part == 1 {
		return helpers.Itoa(canMove().Cardinality())
	}

	total := 0
	for {
		canDo := canMove()
		if canDo.Cardinality() == 0 {
			break
		}
		total += canDo.Cardinality()
		papers = papers.Difference(canDo)
	}
	return helpers.Itoa(total)
}

func init() {
	helpers.AocRegister(2025, 4, &Day04{})
}
