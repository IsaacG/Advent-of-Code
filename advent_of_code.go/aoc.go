package main

import (
	"fmt"
	"isaacgood.com/aoc/helpers"
	"isaacgood.com/aoc/y2017"
	"isaacgood.com/aoc/y2020"
	"isaacgood.com/aoc/y2024"
	"isaacgood.com/aoc/y2025"
	"os"
	"time"
)

var puzzles = map[helpers.Puzzle]helpers.Solver{
	helpers.Puzzle{2017, 1}:  y2017.New01(),
	helpers.Puzzle{2017, 2}:  y2017.New02(),
	helpers.Puzzle{2017, 3}:  y2017.New03(),
	helpers.Puzzle{2017, 4}:  y2017.New04(),
	helpers.Puzzle{2017, 5}:  y2017.New05(),
	helpers.Puzzle{2017, 15}: y2017.New15(),
	helpers.Puzzle{2017, 17}: y2017.New17(),
	helpers.Puzzle{2017, 22}: y2017.New22(),
	helpers.Puzzle{2017, 24}: y2017.New24(),
	helpers.Puzzle{2017, 25}: y2017.New25(),
	helpers.Puzzle{2020, 1}:  y2020.New01(),
	helpers.Puzzle{2024, 1}:  y2024.New01(),
	helpers.Puzzle{2024, 2}:  y2024.New02(),
	helpers.Puzzle{2024, 3}:  y2024.New03(),
	helpers.Puzzle{2024, 17}:  y2024.New17(),
	helpers.Puzzle{2025, 2}:  y2025.New02(),
}

func main() {
	fmt.Println(time.Now())
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
}
