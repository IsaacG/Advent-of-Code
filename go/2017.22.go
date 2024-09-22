package main

import (
	"maps"
	"slices"
	"strings"
)

type virusState int

// P201722 solves 2017/22.
type P201722 struct {
	nodes     map[Location]virusState
	center    int
	steps     []int
	nextState []map[virusState]virusState
}

const (
	clean    virusState = iota
	weakened virusState = iota
	infected virusState = iota
	flagged  virusState = iota
)

type simulation struct {
	*Robot
	nodes     map[Location]virusState
	infected  int
	nextState map[virusState]virusState
}

func (s *simulation) run(steps int, states map[virusState]virusState) {
	rotations := map[virusState]Rotation{clean: RotateLeft, weakened: RotateStraight, infected: RotateRight, flagged: RotateReverse}
	for range steps {
		state, ok := s.nodes[s.Location]
		if !ok {
			state = clean
		}
		s.Direction.Rotate(rotations[state])
		s.nodes[s.Location] = states[state]
		if s.nodes[s.Location] == infected {
			s.infected++
		}
		s.Robot.Advance()
	}
}

// New201722 returns a new solver for 2017/22.
func New201722() *P201722 {
	return &P201722{
		steps: []int{10000, 10000000},
		nextState: []map[virusState]virusState{
			{clean: infected, infected: clean},
			{clean: weakened, weakened: infected, infected: flagged, flagged: clean},
		},
	}
}

// SetInput handles input for this solver.
func (p *P201722) SetInput(data string) {
	lines := strings.Split(data, "\n")
	slices.Reverse(lines)
	p.nodes = make(map[Location]virusState)
	for y, line := range lines {
		for x, char := range line {
			if char == '#' {
				p.nodes[Location{x, y}] = infected
			}
		}
	}
	p.center = (len(lines) - 1) / 2
}

// Solve returns the solution for one part.
func (p *P201722) Solve(part int) string {
	s := simulation{
		Robot:    &Robot{Location{p.center, p.center}, Direction{0, 1}},
		nodes:    maps.Clone(p.nodes),
		infected: 0,
	}
	s.run(p.steps[part], p.nextState[part])
	return Itoa(s.infected)
}
