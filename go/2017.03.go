package main

// Day201703 solves 2017/03.
type Day201703 struct {
	steps int
}

// New201703 returns a new solver for 2017/03.
func New201703() *Day201703 {
	return &Day201703{}
}

// SetInput handles input for this solver.
func (p *Day201703) SetInput(data string) {
	p.steps = ParseOneNumber(data)
}

// Solve returns the solution for one part.
func (p *Day201703) Solve(part int) string {
	board := make(map[Location]int)
	robot := Robot{Location{0, 0}, Direction{0, -1}}
	number := 1

	// Compute the value for one cell of the grid.
	val := []func() int{
		func() int { return number },
		func() int {
			total := 0
			for _, d := range EightDirections {
				total += board[robot.Peak(d)]
			}
			return total
		},
	}[part]

	board[robot.Location] = number
	for i := 2; i <= p.steps; i++ {
		peak := robot.Peak(robot.Direction.Rotated(RotateLeft))
		if _, ok := board[peak]; !ok {
			robot.Rotate(RotateLeft)
		}
		robot.Advance()
		value := val()
		board[robot.Location] = value
		if part == 1 && value > p.steps {
			return Itoa(value)
		}
	}
	return Itoa(robot.ManhattanDistance())
}
