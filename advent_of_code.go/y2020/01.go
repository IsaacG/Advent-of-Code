package y2020

import (
	"isaacgood.com/aoc/helpers"
	"strings"
)

const (
	target = 2020
)

func check(err error) {
	if err != nil {
		panic(err)
	}
}

// Day01 solves 2020/01.
type Day01 struct {
	nums map[int]bool
}

// SetInput handles input for this solver.
func (p *Day01) SetInput(data string) {
	p.nums = make(map[int]bool)
	for _, s := range strings.Split(string(data), "\n") {
		if s == "" {
			continue
		}
		n := helpers.Atoi(s)
		p.nums[n] = true
	}
}

func (p *Day01) partOne() int {
	for n := range p.nums {
		if _, has := p.nums[target-n]; has != false {
			return n * (target - n)
		}
	}
	panic("no solution found")
}
func (p *Day01) partTwo() int {
	for n := range p.nums {
		for o := range p.nums {
			t := target - n - o
			if _, has := p.nums[t]; has != false {
				return n * o * t
			}
		}
	}
	panic("no solution found")
}

// Solve returns the solution for one part.
func (p *Day01) Solve(data string, part int) string {
	p.SetInput(data)
	m := []func() int{p.partOne, p.partTwo}[part-1]
	return helpers.Itoa(m())
}

func init() {
	helpers.AocRegister(2020, 1, &Day01{})
}
