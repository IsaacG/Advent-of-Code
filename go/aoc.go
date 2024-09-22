package main

import "os"

var puzzles = map[Puzzle]Solver{
	Puzzle{2017, 17}: New201717(),
	Puzzle{2017, 22}: New201722(),
	Puzzle{2020, 1}:  New202001(),
}

func main() {
	if len(os.Args) == 3 {
		p := Puzzle{Atoi(os.Args[1]), Atoi(os.Args[2])}
		p.Check(puzzles[p])
	} else {
		for puzzle, solver := range puzzles {
			puzzle.Check(solver)
		}
	}
}
