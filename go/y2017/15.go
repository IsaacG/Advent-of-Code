package y2017

import "strings"
import "isaacgood.com/aoc/helpers"

// Day15 solves 2017/15.
type Day15 struct {
	start      []int
	factors    []int
	steps      []int
	checkMasks []int
}

const (
	mod     = 2147483647
	bitMask = (1 << 16) - 1
)

// New15 returns a new solver for 2017/15.
func New15() *Day15 {
	return &Day15{
		start:      make([]int, 2),
		factors:    []int{16807, 48271},
		steps:      []int{40000000, 5000000},
		checkMasks: []int{4 - 1, 8 - 1},
	}
}

// SetInput handles input for this solver.
func (p *Day15) SetInput(data string) {
	for l, line := range strings.Split(data, "\n") {
		words := strings.Fields(line)
		p.start[l] = helpers.Atoi(words[len(words)-1])
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
func (p *Day15) Solve(part int) string {
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
	return helpers.Itoa(total)
}
