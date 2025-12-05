package helpers

import (
	"fmt"
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
	FourDirections  = []Direction{{0, 1}, {0, -1}, {1, 0}, {-1, 0}}
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
func (d *Direction) Rotated(rotation Rotation) Direction {
	n := &Direction{d.Dx, d.Dy}
	n.Rotate(rotation)
	return *n
}

// Location tracks a 2D Cartesian coordinate.
type Location struct {
	X, Y int
}

func (l Location) AdjacentStraight() []Location {
	return []Location{
		{l.X + 1, l.Y},
		{l.X - 1, l.Y},
		{l.X, l.Y + 1},
		{l.X, l.Y - 1},
	}
}

func (l Location) AdjacentDiagonal() []Location {
	return []Location{
		{l.X + 1, l.Y + 1},
		{l.X - 1, l.Y + 1},
		{l.X + 1, l.Y - 1},
		{l.X - 1, l.Y - 1},
	}
}

func (l Location) AdjacentAll() []Location {
	return []Location{
		{l.X + 1, l.Y},
		{l.X - 1, l.Y},
		{l.X, l.Y + 1},
		{l.X, l.Y - 1},
		{l.X + 1, l.Y + 1},
		{l.X - 1, l.Y + 1},
		{l.X + 1, l.Y - 1},
		{l.X - 1, l.Y - 1},
	}
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
func Atoi(a string) int {
	i, err := strconv.Atoi(a)
	if err != nil {
		panic(fmt.Sprintf("strconv.Atoi failed to parse %s", a))
	}
	return i
}

// Itoa is a convenience wrapper around strconv.Itoa
func Itoa(i int) string {
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

type AccumulatorFunc[T any, R any] interface {
	~func(acc R, i int, s T) R
}

func Reduce[T any, R any, F AccumulatorFunc[T, R]](items []T, initialAccumulator R, f F) R {
	acc := initialAccumulator
	for i, s := range items {
		acc = f(acc, i, s)
	}
	return acc
}

func SumIf[T any](items []T, f func(item T) bool) int {
	sum := 0
	for _, item := range items {
		if f(item) {
			sum++
		}
	}
	return sum
}

func ApplyIf[T any](items []T, apply func(item T), test func(item T) bool) {
	for _, item := range items {
		if test(item) {
			apply(item)
		}
	}
}

func Cmp(a, b int) int {
	if a == b {
		return 0
	}
	if a < b {
		return -1
	}
	return 1
}

// Clamp b between and c.
func Clamp(a, b, c int) int {
	if b < a {
		return a
	}
	if b > c {
		return c
	}
	return b
}

// Sum up an int slice.
func Sum(i []int) int {
	total := 0
	for _, j := range i {
		total += j
	}
	return total
}

// Max is max.
func Max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

// Min is min.
func Min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

// Abs is abs.
func Abs(a int) int {
	if a < 0 {
		return -a
	}
	return a
}
