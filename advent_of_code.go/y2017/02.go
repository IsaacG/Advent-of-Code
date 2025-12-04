package y2017

import (
	"isaacgood.com/aoc/helpers"
	"slices"
)

// Day02 solves 2017/02.
type Day02 struct {
	data [][]int
}

func (p *Day02) one() int {
	total := 0
	for _, line := range p.data {
		total += slices.Max(line) - slices.Min(line)
	}
	return total
}

func (p *Day02) two() int {
	total := 0
outer:
	for _, line := range p.data {
		sorted := slices.Clone(line)
		slices.Sort(sorted)
		length := len(sorted)
		for i := length - 1; i > 0; i-- {
			for j := i - 1; j >= 0; j-- {
				if sorted[i]%sorted[j] == 0 {
					total += sorted[i] / sorted[j]
					continue outer
				}
			}
		}
	}
	return total
}

// Solve returns the solution for one part.
func (p *Day02) Solve(data string, part int) string {
	p.data = helpers.ParseMultiNumbersPerLine(data)
	return helpers.Itoa([]func() int{p.one, p.two}[part-1]())
}

func init() {
	helpers.AocRegister(2017, 2, &Day02{})
}
