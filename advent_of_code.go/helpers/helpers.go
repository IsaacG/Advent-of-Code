package helpers

import (
	"strconv"
)

const (
	PartOne = 0
	PartTwo = 1
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
	Dx, Dy int
}

var (
	FourDirections = []Direction{{0, 1}, {0, -1}, {1, 0}, {-1, 0}}
	EightDirections = []Direction{{0, 1}, {0, -1}, {1, 0}, {-1, 0}, {1, 1}, {-1, -1}, {1, -1}, {-1, 1}}
)

// Rotate the direction by n * 90 degrees.
func (d *Direction) Rotate(rotation Rotation) {
	switch rotation {
	case RotateRight:
		d.Dx, d.Dy = +1*d.Dy, -1*d.Dx
	case RotateLeft:
		d.Dx, d.Dy = -1*d.Dy, +1*d.Dx
	case RotateReverse:
		d.Dx, d.Dy = -1*d.Dx, -1*d.Dy
	case RotateStraight:
	}
}

// Rotated returns a new Direction with a rotation applied.
func (d *Direction) Rotated(rotation Rotation) Direction{
	n := &Direction{d.Dx, d.Dy}
	n.Rotate(rotation)
	return *n
}

// Location tracks a 2D Cartesian coordinate.
type Location struct {
	X, Y int
}

func (l Location) ManhattanDistance() int {
	return Abs(l.X) + Abs(l.Y)
}

// Robot is an object with a Cartesian location and direction. It can advance and rotate.
type Robot struct {
	Location
	Direction
}

// Advance the robot by the Direction.
func (r *Robot) Advance() {
	r.X += r.Dx
	r.Y += r.Dy
}

// Return the Location if we were to move in a given Direction.
func (r *Robot) Peak(direction Direction) Location {
	return Location{r.X + direction.Dx, r.Y + direction.Dy}
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

// Sign returns the sign of an int value.
func Sign(i int) int {
	if i > 0 {
		return 1
	}
	if i < 0 {
		return -1
	}
	return 0
}

// Abs returns the absolute int value.
func Abs(i int) int {
	if i >= 0 {
		return i
	}
	return -i
}

// Transpose a rectangular 2D list.
func Transpose[T any](data [][]T) [][]T {
	transposed := make([][]T, len(data[0]))
	columns := len(data)
	for row := range data[0] {
		transposed[row] = make([]T, columns)
	}
	for row, vals := range data {
		for col, val := range vals {
			transposed[col][row] = val
		}
	}
	return transposed
}
