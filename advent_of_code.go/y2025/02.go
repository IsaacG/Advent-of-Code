package y2025

import (
	"strings"

	"github.com/dlclark/regexp2"
	"isaacgood.com/aoc/helpers"
)

// Day02 solves 2025/02.
type Day02 struct {
	pairs [][2]int
}

// New02 returns a new solver for 2025/02.
func New02() *Day02 {
	return &Day02{}
}

// SetInput handles input for this solver.
func (p *Day02) SetInput(data string) {
	for pair := range strings.SplitSeq(data, ",") {
		nums := strings.Split(pair, "-")
		p.pairs = append(p.pairs, [2]int{helpers.Atoi(nums[0]), helpers.Atoi(nums[1])})
	}
}

// Solve returns the solution for one part.
func (p *Day02) Solve(part int) string {
	total := 0
	pattern := `^(\d+)\1$`
	if part == 1 {
		pattern = `^(\d+)\1+$`
	}
	re := regexp2.MustCompile(pattern, 0)
	for _, pair := range p.pairs {
		for i := pair[0]; i <= pair[1]; i++ {
			if match, err := re.MatchString(helpers.Itoa(i)); err == nil && match {
				total += i
			}
		}
	}
	return helpers.Itoa(total)
}
