package y2024

import "regexp"
import "isaacgood.com/aoc/helpers"

// Day03 solves 2024/03.
type Day03 struct{ data string }

// Solve returns the solution for one part.
func (p *Day03) Solve(data string, part int) string {
	p.data = data
	pattern := regexp.MustCompile(`don't\(\)|do\(\)|mul\((\d{1,3}),(\d{1,3})\)`)
	enabled := true
	total := 0
	for _, match := range pattern.FindAllStringSubmatch(p.data, -1) {
		if match[0] == "don't()" {
			enabled = false
		} else if match[0] == "do()" {
			enabled = true
		} else if enabled || part == 0 {
			total += atoi(match[1]) * atoi(match[2])
		}
	}
	return itoa(total)
}

func init() {
	helpers.AocRegister(2024, 3, &Day03{})
}
