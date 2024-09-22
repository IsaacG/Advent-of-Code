package main

import (
	"slices"
	"strings"
)

// P201704 solves 2017/04.
type P201704 struct {
	data [][]string
}

// New201704 returns a new solver for 2017/04.
func New201704() *P201704 {
	return &P201704{}
}

// SetInput handles input for this solver.
func (p *P201704) SetInput(data string) {
	p.data = ParseMultiWordsPerLine(data)
}

// Solve returns the solution for one part.
func (p *P201704) Solve(part int) string {
	transform := []func(string) string{
		func(s string) string { return s },
		func(s string) string {
			sorted := strings.Split(s, "")
			slices.Sort(sorted)
			return strings.Join(sorted, "")
		},
	}[part]
	total := 0
outer:
	for _, words := range p.data {
		uniq := make(map[string]struct{}, len(words))
		for _, word := range words {
			word = transform(word)
			if _, ok := uniq[word]; ok {
				continue outer
			}
			uniq[word] = struct{}{}
		}
		total++
	}
	return Itoa(total)
}
