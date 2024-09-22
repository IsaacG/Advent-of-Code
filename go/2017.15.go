package main

import "strings"

// P201715 solves 2017/15.
type P201715 struct {
	start      []int
	factors    []int
	steps      []int
	checkMasks []int
}

const (
	mod     = 2147483647
	bitMask = (1 << 16) - 1
)

// New201715 returns a new solver for 2017/15.
func New201715() *P201715 {
	return &P201715{
		start:      make([]int, 2),
		factors:    []int{16807, 48271},
		steps:      []int{40000000, 5000000},
		checkMasks: []int{4 - 1, 8 - 1},
	}
}

// SetInput handles input for this solver.
func (p *P201715) SetInput(data string) {
	for l, line := range strings.Split(data, "\n") {
		words := strings.Fields(line)
		p.start[l] = Atoi(words[len(words)-1])
	}
}

func generator(ch chan<- int, value, factor, mask, part int) {
	for {
		value = (value * factor) % mod
		if part == 0 || value&mask == 0 {
			ch <- value & bitMask
		}
	}
}

// Solve returns the solution for one part.
func (p *P201715) Solve(part int) string {
	total := 0

	var chs []chan int
	for i := 0; i < 2; i++ {
		ch := make(chan int)
		chs = append(chs, ch)
		go generator(ch, p.start[i], p.factors[i], p.checkMasks[i], part)
	}
	for range p.steps[part] {
		if <-chs[0] == <-chs[1] {
			total++
		}
	}
	return Itoa(total)
}
