// Escape the Maze
//
// You are trapped in a maze represented by a grid of tiles.
// Some tiles are walls (1) and some are open (0).
// You can move up, down, left, or right.
// Find the minimum number of steps to go from the starting tile to the exit.
// If it's impossible, return -1.
//
// The grid is given as a flat array in row-major order.
// The width of the grid is provided as a separate argument.
package main

type element struct {
	steps int
	pos   [2]int
}

var directions = [][2]int{{0, 1}, {0, -1}, {1, 0}, {-1, 0}}

func escapeMaze(grid []int, width int, startR int, startC int, endR int, endC int) int {
	seen := map[[2]int]bool{
		[2]int{startR, startC}: true,
	}
	todo := []element{{0, [2]int{startR, startC}}}
	for len(todo) != 0 {
		cur := todo[0]
		todo = todo[1:]

		pos := cur.pos
		if pos[0] == endR && pos[1] == endC {
			return cur.steps
		}

		steps := cur.steps + 1
		for _, direction := range directions {
			next := [2]int{pos[0] + direction[0], pos[1] + direction[1]}
			idx := next[0]*width + next[1]
			if idx >= 0 && idx < len(grid) && grid[next[0]*width+next[1]] == 0 && !seen[next] {
				seen[next] = true
				todo = append(todo, element{steps, next})
			}
		}
	}
	return -1
}

var cases = []struct {
	grid   []int
	width  int
	startR int
	startC int
	endR   int
	endC   int
	want   int
}{
	{[]int{0, 0, 0, 0, 0, 1, 0, 0, 0, 0}, 5, 0, 0, 0, 4, 4},
	{[]int{0, 1, 0, 0, 0, 1, 0, 0, 0, 0}, 5, 0, 0, 0, 4, -1},
	{[]int{0, 1, 0, 0}, 2, 0, 0, 1, 0, 1},
}

func main() {
	for i, tc := range cases {
		if got := escapeMaze(tc.grid, tc.width, tc.startR, tc.startC, tc.endR, tc.endC); got != tc.want {
			println(i, "FAIL", got, tc.want)
		} else {
			println(i, "PASS")
		}
	}
}
