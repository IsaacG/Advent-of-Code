package y2017

import (
	"maps"
	"slices"
	"strings"
	"isaacgood.com/aoc/helpers"
)

type virusState int

// Day22 solves 2017/22.
type Day22 struct {
	nodes     map[helpers.Location]virusState
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
	*helpers.Robot
	nodes     map[helpers.Location]virusState
	infected  int
	nextState map[virusState]virusState
}

func (s *simulation) run(steps int, states map[virusState]virusState) {
	rotations := map[virusState]helpers.Rotation{clean: helpers.RotateLeft, weakened: helpers.RotateStraight, infected: helpers.RotateRight, flagged: helpers.RotateReverse}
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

// New22 returns a new solver for 2017/22.
func New22() *Day22 {
	return &Day22{
		steps: []int{10000, 10000000},
		nextState: []map[virusState]virusState{
			{clean: infected, infected: clean},
			{clean: weakened, weakened: infected, infected: flagged, flagged: clean},
		},
	}
}

// SetInput handles input for this solver.
func (p *Day22) SetInput(data string) {
	lines := strings.Split(data, "\n")
	slices.Reverse(lines)
	p.nodes = make(map[helpers.Location]virusState)
	for y, line := range lines {
		for x, char := range line {
			if char == '#' {
				p.nodes[helpers.Location{x, y}] = infected
			}
		}
	}
	p.center = (len(lines) - 1) / 2
}

// Solve returns the solution for one part.
func (p *Day22) Solve(part int) string {
	nodes := make(map[helpers.Location]virusState)
	maps.Copy(nodes, p.nodes)
	s := simulation{
		Robot:    &helpers.Robot{helpers.Location{p.center, p.center}, helpers.Direction{0, 1}},
		nodes:    nodes,
		infected: 0,
	}
	s.run(p.steps[part], p.nextState[part])
	return helpers.Itoa(s.infected)
}
