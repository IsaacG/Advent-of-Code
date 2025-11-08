package main

import (
	"fmt"
	"os"
	"strings"
	"time"

	"isaacgood.com/everybodycodes/e2025"
	"isaacgood.com/everybodycodes/helpers"
)

type Day struct {
	event string
	day int
}

var puzzles = map[Day]func (string, int) string {
	Day{"e2025", 2}: e2025.Quest02,
	Day{"e2025", 5}: e2025.Quest05,
}

type Puzzle struct {
	Day
	input map[int]string
	want map[int]string
	solver func (string, int) string
}

func NewPuzzle(event string, day int) *Puzzle {
	solver, ok := puzzles[Day{event, day}]
	if !ok {
		fmt.Printf("No solver configured for %s/%02d\n", event, day)
		return nil
	}

	solutions := map[int]string{}
	raw_solutions := helpers.LoadFile(fmt.Sprintf("%s/solutions.txt", event))
	for part := 1; part <= 3; part ++ {
		prefix := fmt.Sprintf("%02d.%d ", day, part)
		for line := range strings.Lines(raw_solutions) {
			if strings.HasPrefix(line, prefix) {
				solutions[part] = strings.TrimSuffix(strings.TrimPrefix(line, prefix), "\n")
			}

		}
	}
	input := map[int]string{}
	for part := 1; part <= 3; part ++ {
		input[part] = helpers.LoadFile(fmt.Sprintf("%s/inputs/%02d.%d.txt", event, day, part))
	}

	return &Puzzle{Day{event, day}, input, solutions, solver}
}

func (p *Puzzle) check() {
	for part := 1; part <= 3; part ++ {
		start := time.Now()
		data := p.input[part]
		got := p.solver(data, part)
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
	event, day := os.Args[1], helpers.Atoi(os.Args[2])
	p := NewPuzzle(event, day)
	if p != nil {
		p.check()
	}
	/*
	if len(os.Args) == 1 {
		for puzzle, solver := range puzzles {
			puzzle.Check(solver)
		}
	} else if len(os.Args) == 2 {
		year := helpers.Atoi(os.Args[1])
		for puzzle, solver := range puzzles {
			if puzzle.Year == year {
				puzzle.Check(solver)
			}
		}
	} else if len(os.Args) == 3 {
		p := helpers.Puzzle{helpers.Atoi(os.Args[1]), helpers.Atoi(os.Args[2])}
		s, ok := puzzles[p]
		if !ok {
			panic("That solver does not exist")
		}
		p.Check(s)
	}
	*/
}
