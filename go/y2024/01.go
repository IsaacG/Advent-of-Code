package y2024

import (
	"isaacgood.com/aoc/helpers"
	"slices"
)

// Day01 solves 2024/01.
type Day01 struct {
	lists [][]int
}

// New01 returns a new solver for 2024/01.
func New01() *Day01 {
	return &Day01{}
}

// SetInput handles input for this solver.
func (p *Day01) SetInput(data string) {
	p.lists = helpers.Transpose(helpers.ParseMultiNumbersPerLine(data))
}

// Function partOne computes the abs diff of the sorted elements.
func (p *Day01) partOne() int {
	slices.Sort(p.lists[0])
	slices.Sort(p.lists[1])
	total := 0
	for idx := range p.lists[0] {
		total += abs(p.lists[0][idx] - p.lists[1][idx])
	}
	return total
}

// Function partTwo returns the sum of the product of elements in the first list and the count in the second list.
func (p *Day01) partTwo() int {
	counter := make(map[int]int)
	for _, num := range p.lists[1] {
		counter[num]++
	}
	total := 0
	for _, num := range p.lists[0] {
		total += num * counter[num]
	}
	return total
}

// Solve returns the solution for one part.
func (p *Day01) Solve(part int) string {
	m := []func() int{p.partOne, p.partTwo}[part]
	return itoa(m())
}
