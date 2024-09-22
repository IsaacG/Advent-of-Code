package main

import (
	"strconv"
)

// Rotation encodes a rotation of n * 90 degrees.
type Rotation int

// Rotations in four directions.
const (
	RotateRight    Rotation = iota
	RotateLeft     Rotation = iota
	RotateReverse  Rotation = iota
	RotateStraight Rotation = iota
)

// Direction tracks a 2D vector.
type Direction struct {
	dx, dy int
}

var (
	FourDirections = []Direction{{0, 1}, {0, -1}, {1, 0}, {-1, 0}}
	EightDirections = []Direction{{0, 1}, {0, -1}, {1, 0}, {-1, 0}, {1, 1}, {-1, -1}, {1, -1}, {-1, 1}}
)

// Rotate the direction by n * 90 degrees.
func (d *Direction) Rotate(rotation Rotation) {
	switch rotation {
	case RotateRight:
		d.dx, d.dy = +1*d.dy, -1*d.dx
	case RotateLeft:
		d.dx, d.dy = -1*d.dy, +1*d.dx
	case RotateReverse:
		d.dx, d.dy = -1*d.dx, -1*d.dy
	case RotateStraight:
	}
}

// Rotated returns a new Direction with a rotation applied.
func (d *Direction) Rotated(rotation Rotation) Direction{
	n := &Direction{d.dx, d.dy}
	n.Rotate(rotation)
	return *n
}

// Location tracks a 2D Cartesian coordinate.
type Location struct {
	x, y int
}

func (l Location) ManhattanDistance() int {
	return Abs(l.x) + Abs(l.y)
}

// Robot is an object with a Cartesian location and direction. It can advance and rotate.
type Robot struct {
	Location
	Direction
}

// Advance the robot by the Direction.
func (r *Robot) Advance() {
	r.x += r.dx
	r.y += r.dy
}

// Return the Location if we were to move in a given Direction.
func (r *Robot) Peak(direction Direction) Location {
	return Location{r.x + direction.dx, r.y + direction.dy}
}

// Atoi is a convenience wrapper around strconv.Atoi
func Atoi(a string) int{
	i, err := strconv.Atoi(a)
	if err != nil {
		panic("strconv.Atoi failed")
	}
	return i
}

// Itoa is a convenience wrapper around strconv.Itoa
func Itoa(i int) string{
	return strconv.Itoa(i)
}

func Abs(i int) int {
	if i >= 0 {
		return i
	}
	return -i
}
