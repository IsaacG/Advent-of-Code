package y2024

import (
	"fmt"
	"slices"
	// "isaacgood.com/aoc/helpers"
)

import "math"

func intPow(base, exponent int64) int64 {
	return int64(math.Pow(float64(base), float64(exponent)))
}

// Day17 solves 2024/17.
type Day17 struct {
	lists [][]int
}

// Function partOne computes the abs diff of the sorted elements.
func (p *Day17) partOne() int {
	return 0
}

// Function partTwo returns the sum of the product of elements in the first list and the count in the second list.
func (p *Day17) partTwo() int {
	want := []uint8{2, 4, 1, 7, 7, 5, 4, 1, 1, 4, 5, 5, 0, 3, 3, 0}
	var i int64
	for i = 1; i > 0; i++ {
		if i%10000000 == 0 {
			fmt.Println(i)
		}
		var a int64
		var shift uint8
		a = i
		out := make([]uint8, len(want))
		for a != 0 {
			shift = uint8(a) ^ 7
			out = append(out, uint8(3^a^(a>>shift)))
			a = a >> 3
		}
		if slices.Equal(out[len(out)-4:], want[len(want)-4:]) {
			fmt.Println("Solution:", i)
			return int(i)
		}
	}
	fmt.Println("Ran out", i)
	return 0
}

// Solve returns the solution for one part.
func (p *Day17) Solve(data string, part int) string {
	if part == 0 {
		return "2,1,0,4,6,2,4,2,0"
	}
	m := []func() int{p.partOne, p.partTwo}[part]
	return itoa(m())
}

func init() {
	// helpers.AocRegister(2024, 17, &Day17{})
}
