package e2025

import (
	// "fmt"
	"slices"
	"strings"

	sets "github.com/deckarep/golang-set/v2"
	"isaacgood.com/everybodycodes/helpers"
)

var dragonOffsets = [8][2]int{
	{1, 2},
	{1, -2},
	{-1, 2},
	{-1, -2},
	{2, 1},
	{2, -1},
	{-2, 1},
	{-2, -1},
}

// Quest10 for Event 2025.
type Quest10 struct {
	board      map[rune][][2]int
	rows       int
	cols       int
	cache      map[[3]int]int
	vulnerable []int
	hideouts   sets.Set[[2]int]
}

func (q Quest10) moves(x, y int) [][2]int {
	var options [][2]int
	for _, offset := range dragonOffsets {
		nx, ny := x+offset[0], y+offset[1]
		if nx >= 0 && nx < q.cols && ny >= 0 && ny < q.rows {
			options = append(options, [2]int{nx, ny})
		}
	}
	return options

}

func (q Quest10) p12(part int) int {
	moves := 4
	if part == 2 {
		moves = 20
	}

	sheepMoves := make([][]int, moves+1)
	for step := range moves + 1 {
		if part == 1 {
			sheepMoves[step] = []int{0}
		} else {
			sheepMoves[step] = []int{step - 1, step}
		}
	}

	start := q.board['D'][0]
	queue := [][3]int{{start[0], start[1], 0}}
	seen := sets.NewSet[[3]int]()
	lambs := sets.NewSet[[2]int](q.board['S']...)

	count := 0
	for len(queue) != 0 {
		cur := queue[0]
		queue = queue[1:]
		dx, dy, steps := cur[0], cur[1], cur[2]

		if steps > 0 && !q.hideouts.Contains([2]int{dx, dy}) {
			for _, dLamb := range sheepMoves[steps] {
				lambPos := [2]int{dx, dy - dLamb}
				if lambs.Contains(lambPos) {
					count++
					lambs.Remove(lambPos)
				}
			}
		}

		if steps == moves {
			continue
		}
		steps++
		for _, move := range q.moves(dx, dy) {
			newState := [3]int{move[0], move[1], steps}
			if seen.Contains(newState) {
				continue
			}
			seen.Add(newState)
			queue = append(queue, newState)
		}
	}
	return count
}

func (q Quest10) cacheKey(dx, dy int, lambs []int) [3]int {
	lambKey := 0
	for _, lamb := range lambs {
		lambKey = lambKey*(q.rows+1) + (lamb + 1)
	}
	return [3]int{dx, dy, lambKey}
}

func (q Quest10) possibilities(dx, dy int, lambs []int) int {
	key := q.cacheKey(dx, dy, lambs)
	if got, ok := q.cache[key]; ok {
		return got
	}

	got := 0
	var lambOptions [][]int
	for idx, pos := range lambs {
		if pos == -1 || pos == q.vulnerable[idx] {
			continue
		}
		if idx != dx || pos+1 != dy || q.hideouts.Contains([2]int{idx, pos + 1}) {
			option := slices.Clone(lambs)
			option[idx]++
			lambOptions = append(lambOptions, option)
		}
	}
	if len(lambOptions) == 0 {
		for idx, pos := range lambs {
			if pos == q.vulnerable[idx] {
				// Lamb must escape; dragon does not win.
				return 0
			}
		}
		lambOptions = append(lambOptions, lambs)
	}

	for _, option := range lambOptions {
		for _, move := range q.moves(dx, dy) {
			lambs = slices.Clone(option)
			won := false
			// Dragon eats sheep
			if move[1] == lambs[move[0]] && !q.hideouts.Contains(move) {
				lambs[move[0]] = -1
				// Check if all the sheep are gone.
				won = true
				for _, pos := range lambs {
					if pos != -1 {
						won = false
						break
					}
				}
			}
			if won {
				got++
			} else {
				got += q.possibilities(move[0], move[1], lambs)
			}
		}
	}

	q.cache[key] = got
	return got
}

func (q Quest10) p3() int {
	q.vulnerable = make([]int, q.cols)
	lambs := make([]int, q.cols)
	q.cache = make(map[[3]int]int)

	hideouts := sets.NewSet[[2]int](q.board['#']...)
	for x := range q.cols {
		y := q.rows - 1
		for hideouts.Contains([2]int{x, y}) {
			y--
		}
		q.vulnerable[x] = y
		lambs[x] = -1
	}
	for _, lamb := range q.board['S'] {
		lambs[lamb[0]] = lamb[1]
	}
	return q.possibilities(q.board['D'][0][0], q.board['D'][0][1], lambs)
}

// Solve Quest 10.
func (q Quest10) Solve(data string, part int) string {
	total := 0
	board := make(map[rune][][2]int)
	for y, line := range strings.Split(data, "\n") {
		for x, char := range line {
			board[char] = append(board[char], [2]int{x, y})
		}
	}
	q.board = board
	q.rows = len(strings.Split(data, "\n"))
	q.cols = len(strings.Split(data, "\n")[0])
	q.hideouts = sets.NewSet[[2]int](board['#']...)

	if part != 3 {
		total = q.p12(part)
	} else {
		total = q.p3()
	}
	return helpers.Itoa(total)
}
