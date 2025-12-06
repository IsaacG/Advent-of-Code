package y2025

import (
	"isaacgood.com/aoc/helpers"
	"strings"
)

// Day06 solves 2025/06.
type Day06 struct {
	op      map[string]func(int, int) int
	initial map[string]int
}

// Solve returns the solution for one part.
func (p *Day06) Solve(data string, part int) string {
	p.op = map[string]func(int, int) int{
		"+": func(a, b int) int { return a + b },
		"*": func(a, b int) int { return a * b },
	}
	p.initial = map[string]int{
		"+": 0,
		"*": 1,
	}
	return []func(string) string{p.p1, p.p2}[part-1](data)
}

func (p *Day06) p1(data string) string {
	lines := helpers.ParseMultiWordsPerLine(data)
	maxLine := len(lines) - 1
	var total int
	for col := range len(lines[0]) {
		tally := p.initial[lines[maxLine][col]]
		op := p.op[lines[maxLine][col]]
		for _, line := range lines[:maxLine] {
			tally = op(tally, helpers.Atoi(line[col]))
		}
		total += tally
	}
	return helpers.Itoa(total)
}

func (p *Day06) p2(data string) string {
	lines := strings.Split(data, "\n")
	maxLine := len(lines) - 1

	var colStarts []int
	var operators []string
	for idx, char := range lines[len(lines)-1] {
		if char != ' ' {
			operators = append(operators, string(char))
			colStarts = append(colStarts, idx)
		}
	}

	var longest int
	for _, line := range lines {
		if l := len(line); l > longest {
			longest = l
		}
	}
	colEnds := colStarts[1:]
	colEnds = append(colEnds, longest+1)

	var total int
	for idx, opChar := range operators {
		tally := p.initial[opChar]
		op := p.op[opChar]

		for col := colStarts[idx]; col < colEnds[idx]-1; col++ {
			var number []byte
			for _, line := range lines[:maxLine] {
				if char := line[col]; char != ' ' {
					number = append(number, line[col])
				}
			}
			tally = op(tally, helpers.Atoi(string(number)))
		}
		total += tally
	}
	return helpers.Itoa(total)
}

func init() {
	helpers.AocRegister(2025, 6, &Day06{})
}
