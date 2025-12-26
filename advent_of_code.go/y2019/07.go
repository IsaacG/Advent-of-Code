package y2019

import (
	"gonum.org/v1/gonum/stat/combin"
	"isaacgood.com/aoc/helpers"
	"sync"
)

// Day 07 solves 2019/07.
type Day07 struct {
}

// Solve returns the solution for one part.
func (q *Day07) Solve(data string, part int) string {
	best := 0
	gen := combin.NewPermutationGenerator(5, 5)
	var channels []chan int
	for i := 0; i < 5; i++ {
		channels = append(channels, make(chan int, 2))
	}
	var offset int
	if part == 2 {
		offset = 5
	}
	for gen.Next() {
		var ics []*IntCode
		var wg sync.WaitGroup
		for i := 0; i < 5; i++ {
			ics = append(ics, NewIntCode(data, IO(channels[i], channels[(i+1)%5])))
		}
		for i, v := range gen.Permutation(nil) {
			channels[i] <- v + offset
		}
		channels[0] <- 0
		for _, ic := range ics {
			wg.Go(ic.run)
		}
		wg.Wait()
		got := <-channels[0]
		if got > best {
			best = got
		}
	}
	return helpers.Itoa(best)
}

func init() {
	helpers.AocRegister(2019, 7, &Day07{})
}
