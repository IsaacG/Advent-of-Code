package helpers

import (
	"fmt"
	"io/ioutil"
	"strings"
	"time"
)

// Solver is able to solve the puzzle for a day.
type Solver interface {
	Solve(int) string
	SetInput(string)
}

// Puzzle is the challenge for a day.
type Puzzle struct {
	Year, Day int
}

// ReadData returns the puzzle input data.
func (p Puzzle) ReadData() string {
	filename := fmt.Sprintf("../inputs/%d.%02d.txt", p.Year, p.Day)
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		panic("Failed to read file")
	}
	return strings.TrimRight(string(data), "\n")
}

// Check checks if a Solver can solve a puzzle.
func (p Puzzle) Check(solver Solver) {
	solutions, err := p.Solutions()
	if err != nil {
		fmt.Println("failed to load solutions: %v", err)
	}
	solver.SetInput(p.ReadData())
	for i, solution := range(solutions) {
		start := time.Now()
		got := solver.Solve(i)
		elapsed := time.Since(start)
		if got == solution {
			fmt.Printf("%d/%02d.%d PASSED!  %15s\n", p.Year, p.Day, i+1, elapsed)
		} else {
			fmt.Printf("%d/%02d.%d FAILED!\n", p.Year, p.Day, i+1)
			fmt.Printf("want %s but got %s\n", solutions[i], got)
		}
	}
}

// Solutions returns the solutions from the solution file.
func (p Puzzle) Solutions() ([]string, error) {
	filename := fmt.Sprintf("../solutions/%d.txt", p.Year)
	day := fmt.Sprintf("%02d", p.Day)
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		panic("Failed to read file")
	}
	for _, line := range strings.Split(strings.TrimRight(string(data), "\n"), "\n") {
		if line == "" {
			continue
		}
		words := strings.Split(line, " ")
		if words[0] == day {
			return words[1:], nil
		}
	}
	return nil, fmt.Errorf("Failed to load solutions")
}
