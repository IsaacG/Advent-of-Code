package main

import (
	"fmt"
	"os"
	"strings"
	"time"

	"isaacgood.com/everybodycodes/e2025"
	"isaacgood.com/everybodycodes/helpers"
)

// Day represents one challenge.
type Day struct {
	event string
	day   int
}

// Puzzle has all the data for one day.
type Puzzle struct {
	Day
	input  map[int]string
	want   map[int]string
	solver e2025.Solver
}

// NewPuzzle constructs and configures a puzzle.
func NewPuzzle(event string, day int) *Puzzle {
	solver, ok := e2025.Puzzles[day]
	if !ok {
		fmt.Printf("No solver configured for %s/%02d\n", event, day)
		return nil
	}

	solutions := map[int]string{}
	rawSolutions := helpers.LoadFile(fmt.Sprintf("%s/solutions.txt", event))
	for part := 1; part <= 3; part++ {
		prefix := fmt.Sprintf("%02d.%d ", day, part)
		for line := range strings.Lines(rawSolutions) {
			if strings.HasPrefix(line, prefix) {
				solutions[part] = strings.TrimSuffix(strings.TrimPrefix(line, prefix), "\n")
			}

		}
	}
	input := map[int]string{}
	for part := 1; part <= 3; part++ {
		input[part] = strings.TrimRight(helpers.LoadFile(fmt.Sprintf("%s/inputs/%02d.%d.txt", event, day, part)), "\n")
	}

	return &Puzzle{Day{event, day}, input, solutions, solver}
}

func (p *Puzzle) check() {
	for part := 1; part <= 3; part++ {
		start := time.Now()
		data := p.input[part]
		got := p.solver.Solve(data, part)
		elapsed := time.Since(start)
		if got == p.want[part] {
			fmt.Printf("%s/%02d.%d PASSED!  %15s\n", p.event, p.day, part, elapsed)
		} else {
			fmt.Printf("%s/%02d.%d FAILED!\n", p.event, p.day, part)
			fmt.Printf("want %s but got %s\n", p.want[part], got)
		}
	}
}

func main() {
	if len(os.Args) == 3 {
		event, day := os.Args[1], helpers.Atoi(os.Args[2])
		p := NewPuzzle(event, day)
		if p != nil {
			p.check()
		}
	} else if len(os.Args) == 2 {
		for day := range 25 {
			if _, ok := e2025.Puzzles[day]; ok {
				NewPuzzle(os.Args[1], day).check()
			}
		}
	} else {
		for day := range e2025.Puzzles {
			NewPuzzle("e2025", day).check()
		}
	}
}
