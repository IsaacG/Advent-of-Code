package y2017

import (
	"slices"
	"strings"
	"isaacgood.com/aoc/helpers"
)

// Day04 solves 2017/04.
type Day04 struct {
	data [][]string
}

// New04 returns a new solver for 2017/04.
func New04() *Day04 {
	return &Day04{}
}

// SetInput handles input for this solver.
func (p *Day04) SetInput(data string) {
	p.data = helpers.ParseMultiWordsPerLine(data)
}

// Solve returns the solution for one part.
func (p *Day04) Solve(part int) string {
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
	return helpers.Itoa(total)
}
