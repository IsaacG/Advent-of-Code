package e2025

import (
	"strconv"
	"strings"
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
	parts := strings.Split(input, ",")
	var nums [2]int
	for i, p := range parts {
		n, err := strconv.Atoi(p)
		if err != nil {
			return ""
		}
		nums[i] = n
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
