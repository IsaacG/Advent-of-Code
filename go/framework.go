package main

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
	year, day int
}

// ReadData returns the puzzle input data.
func (p Puzzle) ReadData() string {
	filename := fmt.Sprintf("../inputs/%d.%02d.txt", p.year, p.day)
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
	for i := 0; i < 2; i++ {
		start := time.Now()
		got := solver.Solve(i)
		elapsed := time.Since(start)
		if got == solutions[i] {
			fmt.Printf("%d/%02d.%d PASSED!  %15s\n", p.year, p.day, i+1, elapsed)
		} else {
			fmt.Printf("%d/%02d.%d FAILED!\n", p.year, p.day, i+1)
			fmt.Printf("want %s but got %s\n", solutions[i], got)
		}
	}
}

// Solutions returns the solutions from the solution file.
func (p Puzzle) Solutions() ([]string, error) {
	filename := fmt.Sprintf("../solutions/%d.txt", p.year)
	day := fmt.Sprintf("%02d", p.day)
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
