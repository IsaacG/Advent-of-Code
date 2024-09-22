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

// Location tracks a 2D Cartesian coordinate.
type Location struct {
	x, y int
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
