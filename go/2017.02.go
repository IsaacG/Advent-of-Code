package main

import (
	"slices"
)

// Day201702 solves 2017/02.
type Day201702 struct {
	data [][]int
}

// New201702 returns a new solver for 2017/02.
func New201702() *Day201702 {
	return &Day201702{}
}

// SetInput handles input for this solver.
func (p *Day201702) SetInput(data string) {
	p.data = ParseMultiNumbersPerLine(data)
}

func (p *Day201702) one() int {
	total := 0
	for _, line := range p.data {
		total += slices.Max(line) - slices.Min(line)
	}
	return total
}

func (p *Day201702) two() int {
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
func (p *Day201702) Solve(part int) string {
	return Itoa([]func() int{p.one, p.two}[part]())
}
