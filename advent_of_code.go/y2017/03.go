package y2017

import "isaacgood.com/aoc/helpers"

// Day03 solves 2017/03.
type Day03 struct {
	steps int
}

// New03 returns a new solver for 2017/03.
func New03() *Day03 {
	return &Day03{}
}

// SetInput handles input for this solver.
func (p *Day03) SetInput(data string) {
	p.steps = helpers.ParseOneNumber(data)
}

// Solve returns the solution for one part.
func (p *Day03) Solve(part int) string {
	board := make(map[helpers.Location]int)
	robot := helpers.Robot{helpers.Location{0, 0}, helpers.Direction{0, -1}}
	number := 1

	// Compute the value for one cell of the grid.
	val := []func() int{
		func() int { return number },
		func() int {
			total := 0
			for _, d := range helpers.EightDirections {
				total += board[robot.Peak(d)]
			}
			return total
		},
	}[part]

	board[robot.Location] = number
	for i := 2; i <= p.steps; i++ {
		peak := robot.Peak(robot.Direction.Rotated(helpers.RotateLeft))
		if _, ok := board[peak]; !ok {
			robot.Rotate(helpers.RotateLeft)
		}
		robot.Advance()
		value := val()
		board[robot.Location] = value
		if part == 1 && value > p.steps {
			return helpers.Itoa(value)
		}
	}
	return helpers.Itoa(robot.ManhattanDistance())
}
