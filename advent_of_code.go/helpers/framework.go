package helpers

import (
	"fmt"
	"io/ioutil"
	"maps"
	"slices"
	"strings"
	"time"
)

// Solver is able to solve the puzzle for a day.
type Solver interface {
	Solve(string, int) string
}

// Puzzle is the challenge for a day.
type Puzzle struct {
	Year, Day int
}

// AocID identifies a puzzle.
type AocID struct {
	year int
	day  int
}

func (id AocID) String() string {
	return fmt.Sprintf("AoC %d/%02d", id.year, id.day)
}

func CheckAocPuzzles(args []string) {
	var nums []int
	for _, arg := range args[1:] {
		nums = append(nums, Atoi(arg))
	}
	var filter func(id AocID) bool
	if len(nums) >= 2 {
		filter = func(id AocID) bool { return id.year == nums[0] && id.day == nums[1] }
	} else if len(nums) == 1 {
		filter = func(id AocID) bool { return id.year == nums[0] }
	} else {
		filter = func(id AocID) bool { return true }
	}

	for _, id := range slices.SortedFunc(
		maps.Keys(AocPuzzles),
		func(a, b AocID) int {
			if a.year == b.year {
				return Cmp(a.day, b.day)
			}
			return Cmp(a.year, b.year)
		},
	) {
		if filter(id) {
			puzzle := GetAocPuzzle(id)
			if len(nums) > 2 {
				puzzle.parts = nums[2]
			}
			puzzle.Check()
		}
	}
}

// Puzzle has all the data for one puzzle.
type AocPuzzle struct {
	AocID
	input  string
	want   []string
	parts  int
	solver Solver
}

var AocPuzzles = map[AocID]Solver{}

// GetAocPuzzle constructs and configures a puzzle.
func GetAocPuzzle(id AocID) *AocPuzzle {
	solver, ok := AocPuzzles[id]
	parts := 2
	if id.year < 2025 && id.day == 25 || id.year >= 2025 && id.day == 12 {
		parts = 1
	}
	if !ok {
		fmt.Printf("No solver configured for %s\n", id)
		return nil
	}

	solutions, err := id.loadSolutions()
	if err != nil {
		fmt.Printf("Failed to load solutions for %s\n", id)
		return nil
	}

	input := id.readData()
	return &AocPuzzle{id, input, solutions, parts, solver}
}

func AocRegister(year, day int, solver Solver) {
	AocPuzzles[AocID{year, day}] = solver
}

// LoadFile returns the contents of a file.
func LoadFile(filename string) string {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		panic("Failed to read solutions file")
	}
	return string(data)
}

// Check checks if a Solver can solve a puzzle.
func (p *AocPuzzle) Check() {
	for part := 1; part <= p.parts; part++ {
		start := time.Now()
		want := p.want[part-1]
		got := p.solver.Solve(p.input, part)
		elapsed := time.Since(start)
		if got == want {
			fmt.Printf("%d/%02d.%d PASSED!  %15s\n", p.year, p.day, part, elapsed)
		} else {
			fmt.Printf("%d/%02d.%d FAILED!  %15s\n", p.year, p.day, part, elapsed)
			fmt.Printf(" => want %s but got %s\n", want, got)
		}
	}
}

// readData returns the puzzle input data.
func (id AocID) readData() string {
	filename := fmt.Sprintf("../advent_of_code/inputs/%d.%02d.txt", id.year, id.day)
	return strings.TrimRight(LoadFile(filename), "\n")
}

// Solutions returns the solutions from the solution file.
func (id AocID) loadSolutions() ([]string, error) {
	filename := fmt.Sprintf("../advent_of_code/solutions/%d.txt", id.year)
	day := fmt.Sprintf("%02d", id.day)
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		panic("Failed to read file")
	}
	var solutions []string
	for _, line := range strings.Split(strings.TrimRight(string(data), "\n"), "\n") {
		if line == "" {
			continue
		}
		words := strings.Split(line, " ")
		if words[0] == day {
			return words[1:], nil
		} else if words[0] == day + ".1" {
			solutions = append(solutions, words[1])
		} else if words[0] == day + ".2" {
			solutions = append(solutions, words[1])
		}
	}
	if len(solutions) > 0 {
		return solutions, nil
	}
	return nil, fmt.Errorf("Failed to load solutions")
}
