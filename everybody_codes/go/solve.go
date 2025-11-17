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

// Solver is able to solve the puzzle for a day.
type Solver interface {
	Solve(string, int) string
}

var puzzles = map[Day]Solver{
	Day{"e2025", 1}: e2025.Quest01{},
	Day{"e2025", 2}: e2025.Quest02{},
	Day{"e2025", 3}: e2025.Quest03{},
	Day{"e2025", 4}: e2025.Quest04{},
	Day{"e2025", 5}: e2025.Quest05{},
	Day{"e2025", 6}: e2025.Quest06{},
	Day{"e2025", 7}: e2025.Quest07{},
	Day{"e2025", 8}: e2025.Quest08{},
	Day{"e2025", 9}: e2025.Quest09{},
}

// Puzzle has all the data for one day.
type Puzzle struct {
	Day
	input  map[int]string
	want   map[int]string
	solver Solver
}

// NewPuzzle constructs and configures a puzzle.
func NewPuzzle(event string, day int) *Puzzle {
	solver, ok := puzzles[Day{event, day}]
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
			if _, ok := puzzles[Day{os.Args[1], day}]; ok {
				NewPuzzle(os.Args[1], day).check()
			}
		}
	} else {
		for solution, _ := range puzzles {
			NewPuzzle(solution.event, solution.day).check()
		}
	}
}
