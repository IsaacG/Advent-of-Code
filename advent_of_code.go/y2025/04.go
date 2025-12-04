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
	papers := sets.NewSet[[2]int]()
	for y, line := range strings.Split(data, "\n") {
		for x, char := range line {
			if char == '@' {
				papers.Add([2]int{x, y})
			}
		}
	}

	canMove := func() sets.Set[[2]int] {
		canDo := sets.NewSet[[2]int]()
		for pos := range papers.Iter() {
			neighborCount := 0
			for dx := -1; dx <= 1; dx++ {
				for dy := -1; dy <= 1; dy++ {
					if dx == 0 && dy == 0 {
						continue
					}
					if papers.Contains([2]int{pos[0] + dx, pos[1] + dy}) {
						neighborCount++
					}
				}
			}
			if neighborCount < 4 {
				canDo.Add(pos)
			}
		}
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
