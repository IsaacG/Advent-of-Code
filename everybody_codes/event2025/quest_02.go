package q02

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

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

func main() {
	for part := 2; part < 4; part++ {
		data, err := ioutil.ReadFile(fmt.Sprintf("inputs/02.%d.txt", part))
		if err != nil {
			panic("Failed to read file")
		}
		input := strings.TrimRight(strings.TrimRight(string(data), "\n")[3:], "]")
		parts := strings.Split(input, ",")
		var nums [2]int
		for i, p := range parts {
			n, err := strconv.Atoi(p)
			if err != nil {
				return
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
		fmt.Println(part, total)
	}
}
