package main

import (
	"slices"
	"strings"
)

// P201702 solves 2017/02.
type P201702 struct {
	data [][]int
}

// New201702 returns a new solver for 2017/02.
func New201702() *P201702 {
	return &P201702{}
}

// SetInput handles input for this solver.
func (p *P201702) SetInput(data string) {
	lines := strings.Split(data, "\n")
	p.data = make([][]int, len(lines))
	for l, line := range lines {
		words := strings.Fields(line)
		nums := make([]int, len(words))
		for i, word := range words {
			nums[i] = Atoi(word)
		}
		p.data[l] = nums
	}
}

func (p *P201702) one() int {
	total := 0
	for _, line := range p.data {
		total += slices.Max(line) - slices.Min(line)
	}
	return total
}

func (p *P201702) two() int {
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
func (p *P201702) Solve(part int) string {
	return Itoa([]func() int{p.one, p.two}[part]())
}
