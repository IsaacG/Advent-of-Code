package main

// P201717 solves 2017/17.
type P201717 struct {
	steps int
}

type node struct {
	val  int
	next *node
}

func partOne(step int) int {
	list := &node{0, nil}
	list.next = list

	for size := 1; size <= 2017; size++ {
		stepsNeeded := step % size
		for i := 0; i < stepsNeeded; i++ {
			list = list.next
		}
		newNode := &node{size, list.next}
		list.next = newNode
		list = list.next
	}

	return list.next.val
}

func partTwo(step int) int {
	lastVal := 0
	pos := 0

	for size := 1; size <= 50000000; size++ {
		pos = ((pos + step) % size) + 1
		if pos == 1 {
			lastVal = size
		}
	}

	return lastVal
}

// New201717 returns a new solver for 2017/17.
func New201717() *P201717 {
	return &P201717{}
}

// SetInput handles input for this solver.
func (p *P201717) SetInput(data string) {
	p.steps = Atoi(data)
}

// Solve returns the solution for one part.
func (p *P201717) Solve(part int) string {
	m := []func(int) int{partOne, partTwo}[part]
	return Itoa(m(p.steps))
}
