package y2024

import (
	"isaacgood.com/aoc/helpers"
)

// Day02 solves 2024/02.
type Day02 struct {
	reports [][]int
}

// New02 returns a new solver for 2024/02.
func New02() *Day02 {
	return &Day02{}
}

// SetInput handles input for this solver.
func (p *Day02) SetInput(data string) {
	p.reports = helpers.ParseMultiNumbersPerLine(data)
}

func (p *Day02) safe(data []int) bool {
	direction := sign(data[1] - data[0])
	end := len(data) - 1
	for idx := 0; idx < end; idx++ {
		diff := data[idx+1] - data[idx]
		if sign(diff) != direction || abs(diff) < 1 || abs(diff) > 3 {
			return false
		}
	}
	return true
}

// Function partOne computes the abs diff of the sorted elements.
func (p *Day02) partOne() int {
	total := 0
	for _, report := range p.reports {
		if p.safe(report) {
			total++
		}
	}
	return total
}

// Function partTwo returns the sum of the product of elements in the first list and the count in the second list.
func (p *Day02) partTwo() int {
	total := 0
	for _, report := range p.reports {
		for idx := 0; idx < len(report); idx++ {
			partial := []int{}
			partial = append(partial, report[:idx]...)
			partial = append(partial, report[idx+1:]...)
			if p.safe(partial) {
				total++
				break
			}
		}
	}
	return total
}

// Solve returns the solution for one part.
func (p *Day02) Solve(part int) string {
	m := []func() int{p.partOne, p.partTwo}[part]
	return itoa(m())
}
