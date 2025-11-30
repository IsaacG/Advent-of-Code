package e2025

import (
	"fmt"
	"strconv"
	"strings"

	"isaacgood.com/everybodycodes/helpers"
)

type Quest02 struct{}

func engrave(x, y int) bool {
	nx, ny := 0, 0
	for i := 0; i < 100; i++ {
		nx, ny = nx*nx-ny*ny, nx*ny*2
		nx, ny = (nx / 100000), (ny / 100000)
		nx, ny = nx+x, ny+y
		if nx < -1000000 || nx > 1000000 || ny < -1000000 || ny > 1000000 {
			return false
		}
	}
	return true
}

func (q Quest02) Solve(data string, part int) string {
	input := strings.TrimRight(data[3:], "]")
	var nums []int
	for p := range strings.SplitSeq(input, ",") {
		nums = append(nums, helpers.Atoi(p))
	}
	if part == 1 {
		x, y := nums[0], nums[1]
		nx, ny := 0, 0
		for i := 0; i < 3; i++ {
			nx, ny = nx*nx-ny*ny, nx*ny*2
			nx, ny = nx/10, ny/10
			nx, ny = nx+x, ny+y
		}
		return fmt.Sprintf("[%d,%d]", nx, ny)
	}

	step := 1
	if part == 2 {
		step = 10
	}

	total := 0
	for y := nums[1]; y < nums[1]+1001; y += step {
		for x := nums[0]; x < nums[0]+1001; x += step {
			if engrave(x, y) {
				total++
			}
		}
	}
	return strconv.Itoa(total)
}

func init() {
	Puzzles[2] = Quest02{}
}
