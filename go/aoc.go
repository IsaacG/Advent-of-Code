package main

import (
	"fmt"
	"os"
	"time"
)

var puzzles = map[Puzzle]Solver{
	Puzzle{2017, 1}: New201701(),
	Puzzle{2017, 2}:  New201702(),
	Puzzle{2017, 3}:  New201703(),
	Puzzle{2017, 4}:  New201704(),
	Puzzle{2017, 5}:  New201705(),
	Puzzle{2017, 15}: New201715(),
	Puzzle{2017, 17}: New201717(),
	Puzzle{2017, 22}: New201722(),
	Puzzle{2017, 24}: New201724(),
	Puzzle{2017, 25}: New201725(),
	Puzzle{2020, 1}:  New202001(),
}

func main() {
	fmt.Println(time.Now())
	if len(os.Args) == 1 {
		for puzzle, solver := range puzzles {
			puzzle.Check(solver)
		}
	} else if len(os.Args) == 2 {
		year := Atoi(os.Args[1])
		for puzzle, solver := range puzzles {
			if puzzle.year == year {
				puzzle.Check(solver)
			}
		}
	} else if len(os.Args) == 3 {
		p := Puzzle{Atoi(os.Args[1]), Atoi(os.Args[2])}
		s, ok := puzzles[p]
		if !ok {
			panic("That solver does not exist")
		}
		p.Check(s)
	}
}
