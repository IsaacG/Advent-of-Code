package y2017

import (
	"isaacgood.com/aoc/helpers"
	"slices"
	"strings"
)

// Day04 solves 2017/04.
type Day04 struct {
	data [][]string
}

// Solve returns the solution for one part.
func (p *Day04) Solve(data string, part int) string {
	p.data = helpers.ParseMultiWordsPerLine(data)
	transform := []func(string) string{
		func(s string) string { return s },
		func(s string) string {
			sorted := strings.Split(s, "")
			slices.Sort(sorted)
			return strings.Join(sorted, "")
		},
	}[part-1]
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

func init() {
	helpers.AocRegister(2017, 4, &Day04{})
}
