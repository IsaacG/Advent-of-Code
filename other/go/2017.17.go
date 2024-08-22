package main

import (
	"fmt"
)

type Node struct {
	val  int
	next *Node
}

func partOne(step int) int {
	list := &Node{0, nil}
	list.next = list

	for size := 1; size <= 2017; size++ {
		stepsNeeded := step % size
		for i := 0; i < stepsNeeded; i++ {
			list = list.next
		}
		newNode := &Node{size, list.next}
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

func main() {
	testStep := 3
	realStep := 348
	fmt.Printf("partOne(%d) = %d\n", testStep, partOne(testStep))
	fmt.Printf("partOne(%d) = %d\n", realStep, partOne(realStep))
	fmt.Printf("partTwo(%d) = %d\n", realStep, partTwo(realStep))
}
