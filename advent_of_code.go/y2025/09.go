package y2025

import (
	// "slices"
	"strings"

	// sets "github.com/deckarep/golang-set/v2"
	"isaacgood.com/aoc/helpers"
)

// Day09 solves 2025/09.
type day09Wall struct {
	left, right, top, bottom int
}

type Day09 struct {
	walls []day09Wall
}

func (q *Day09) valid(a, b []int) bool {
	left := helpers.Min(a[0], b[0])
	right := helpers.Max(a[0], b[0])
	top := helpers.Min(a[1], b[1])
	bottom := helpers.Max(a[1], b[1])
	for _, wall := range q.walls {
		if wall.top < bottom && wall.bottom > top && wall.left < right && wall.right > left {
			return false
		}
	}
	return true
}

// Solve returns the solution for one part.
func (q *Day09) Solve(data string, part int) string {
	points := helpers.ParseMultiNumbersPerLine(strings.ReplaceAll(data, ",", " "))
	// Close the circuit, leaving the first segment as a horizontal line.
	if points[0][0] == points[1][0] {
		points = append(points[len(points)-1:], points...)
	} else {
		points = append(points, points[0])
	}

	for i := 0; i < len(points) - 1; i++ {
		wall := day09Wall{
			helpers.Min(points[i][0], points[i+1][0]),  // smaller x
			helpers.Max(points[i][0], points[i+1][0]),  // bigger x
			helpers.Min(points[i][1], points[i+1][1]),  // smaller y
			helpers.Max(points[i][1], points[i+1][1]),  // bigger y
		}
		q.walls = append(q.walls, wall)
	}

	var biggest int
	for idxA, pointA := range points {
		for idxB, pointB := range points {
			if idxA <= idxB {
				continue
			}
			width := helpers.Abs(pointA[0] - pointB[0]) + 1
			height := helpers.Abs(pointA[1] - pointB[1]) + 1
			size := width * height
			if size <= biggest {
				continue
			}
			if part == 1 || q.valid(pointA, pointB) {
				biggest = size
			}
		}
	}
	return helpers.Itoa(biggest)
}

func init() {
	helpers.AocRegister(2025, 9, &Day09{})
}
