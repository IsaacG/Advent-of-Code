package main

import (
	"fmt"
	"io/ioutil"
	"maps"
	"slices"
	"strings"
)

type Rotation int
type virusState int

const (
	rotateRight    Rotation   = iota
	rotateLeft     Rotation   = iota
	rotateReverse  Rotation   = iota
	rotateStraight Rotation   = iota
	clean          virusState = iota
	weakened       virusState = iota
	infected       virusState = iota
	flagged        virusState = iota
	steps1                    = 10000
	steps2                    = 10000000
)

var (
	nextState1 = map[virusState]virusState{clean: infected, infected: clean}
	nextState2 = map[virusState]virusState{clean: weakened, weakened: infected, infected: flagged, flagged: clean}
	rotations  = map[virusState]Rotation{clean: rotateLeft, weakened: rotateStraight, infected: rotateRight, flagged: rotateReverse}
)

type Location struct {
	x, y int
}

func (l *Location) Advance(d *Direction) {
	l.x += d.dx
	l.y += d.dy
}

type Direction struct {
	dx, dy int
}

func (d *Direction) Rotate(rotation Rotation) {
	switch rotation {
	case rotateRight:
		d.dx, d.dy = +1*d.dy, -1*d.dx
	case rotateLeft:
		d.dx, d.dy = -1*d.dy, +1*d.dx
	case rotateReverse:
		d.dx, d.dy = -1*d.dx, -1*d.dy
	case rotateStraight:
	}
}

type Simulation struct {
	*Location
	*Direction
	nodes    map[Location]virusState
	infected int
}

func (s *Simulation) Run(steps int, states map[virusState]virusState) {
	for range steps {
		state, ok := s.nodes[*s.Location]
		if !ok {
			state = clean
		}
		s.Direction.Rotate(rotations[state])
		s.nodes[*s.Location] = states[state]
		if s.nodes[*s.Location] == infected {
			s.infected++
		}
		s.Advance(s.Direction)
	}
}

func main() {
	data, err := ioutil.ReadFile("2017/22.txt")
	if err != nil {
		panic("Failed to read file")
	}
	lines := strings.Split(strings.TrimRight(string(data), "\n"), "\n")
	slices.Reverse(lines)
	nodes := make(map[Location]virusState)
	for y, line := range lines {
		for x, char := range line {
			if char == '#' {
				nodes[Location{x, y}] = infected
			}
		}
	}
	center := (len(lines) - 1) / 2
	nodes2 := maps.Clone(nodes)
	s := &Simulation{&Location{center, center}, &Direction{0, 1}, nodes, 0}
	s.Run(steps1, nextState1)
	fmt.Printf("Part 1: Robot infected %d locations. Correct: %v\n", s.infected, s.infected == 5261)
	s = &Simulation{&Location{center, center}, &Direction{0, 1}, nodes2, 0}
	s.Run(steps2, nextState2)
	fmt.Printf("Part 2: Robot infected %d locations. Correct: %v\n", s.infected, s.infected == 2511927)
}
