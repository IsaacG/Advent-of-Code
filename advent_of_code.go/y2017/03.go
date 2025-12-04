package y2017

import "isaacgood.com/aoc/helpers"

// Day03 solves 2017/03.
type Day03 struct {
	steps int
}

// Solve returns the solution for one part.
func (p *Day03) Solve(data string, part int) string {
	p.steps = helpers.ParseOneNumber(data)
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
	}[part-1]

	board[robot.Location] = number
	for i := 2; i <= p.steps; i++ {
		peak := robot.Peak(robot.Direction.Rotated(helpers.RotateLeft))
		if _, ok := board[peak]; !ok {
			robot.Rotate(helpers.RotateLeft)
		}
		robot.Advance()
		value := val()
		board[robot.Location] = value
		if part == 2 && value > p.steps {
			return helpers.Itoa(value)
		}
	}
	return helpers.Itoa(robot.ManhattanDistance())
}

func init() {
	helpers.AocRegister(2017, 3, &Day03{})
}
