package main

import (
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

// Day202001 solves 2020/01.
type Day202001 struct {
	nums map[int]bool
}

// New202001 returns a new solver for 2020/01.
func New202001() *Day202001 {
	return &Day202001{}
}

// SetInput handles input for this solver.
func (p *Day202001) SetInput(data string) {
	p.nums = make(map[int]bool)
	for _, s := range strings.Split(string(data), "\n") {
		if s == "" {
			continue
		}
		n := Atoi(s)
		p.nums[n] = true
	}
}

func (p *Day202001) partOne() int {
	for n := range p.nums {
		if _, has := p.nums[target-n]; has != false {
			return n * (target - n)
		}
	}
	panic("no solution found")
}
func (p *Day202001) partTwo() int {
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
func (p *Day202001) Solve(part int) string {
	m := []func() int{p.partOne, p.partTwo}[part]
	return Itoa(m())
}
