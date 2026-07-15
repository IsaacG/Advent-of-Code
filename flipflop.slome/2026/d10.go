package main

import (
	"fmt"
	"os"
	"strings"
	"sync"
	"time"
)

type Program struct {
	instructions [][]int
	labels map[int]int
}

func parse(data string) Program {
	lines := strings.Split(string(data), "\n")
	var instructions [][]int
	labels := map[int]int{}

	for _, line := range lines {
		if strings.HasPrefix(line, "be") {
			labels[len(strings.TrimPrefix(line, "be")) / 2] = len(instructions)
		} else if strings.HasPrefix(line, "ba") {
			line = strings.TrimPrefix(line, "ba")
			parts := strings.Split(strings.TrimPrefix(line, "ba"), "ne")
			counts := make([]int, len(parts))
			for i, part := range parts {
				counts[i] = len(part) / 2
			}
			instructions = append(instructions, counts)
		} else {
			panic("invalid line")
		}
	}
	return Program{instructions: instructions, labels: labels}
}

func mod(i int) int {
	for i < 0 {
		i += 65536
	}
	return i % 65536
}

func (p Program) run(mem []int) bool {
	ptr := 0
	counter := 0
	maxPtr := len(p.instructions)

	for ptr >= 0 && ptr < maxPtr && counter <= 5000000 {
		instruction := p.instructions[ptr]
		ptr++
		counter++
		switch instruction[0] {
		case 0:
			mem[instruction[2]] = instruction[1]
		case 1:
			mem[instruction[2]] = mem[instruction[1]]
		case 2:
			mem[instruction[3]] = mod(mem[instruction[1]] + mem[instruction[2]])
		case 3:
			mem[instruction[3]] = mod(mem[instruction[1]] - mem[instruction[2]])
		case 4:
			mem[instruction[3]] = mod(mem[instruction[1]] * mem[instruction[2]])
		case 5:
			if mem[instruction[2]] == 0 {
				mem[instruction[3]] = 0
			} else {
				mem[instruction[3]] = mem[instruction[1]] % mem[instruction[2]]
			}
		case 6:
			mem[instruction[1]] = mod(mem[instruction[1]] + 1)
		case 7:
			mem[instruction[1]] = mod(mem[instruction[1]] - 1)
		case 8:
			ptr = p.labels[instruction[1]]
		case 9:
			if mem[instruction[1]] == 0 {
				ptr = p.labels[instruction[2]]
			}
		case 10:
			if mem[instruction[1]] != 0 {
				ptr = p.labels[instruction[2]]
			}
		}
	}
	return counter <= 5000000
}

func main () {
	fmt.Println("Hello")
	start := time.Now()
	raw, err := os.ReadFile("inputs/10.txt")
	if err != nil {
		fmt.Printf("reading file: %w", err)
		return
	}
	program := parse(string(raw))
	fmt.Printf("Read and parse: %s\n", time.Since(start))

	start = time.Now()
	mem := make([]int, 16)
	program.run(mem)
	fmt.Printf("Part 1 (%s): %d\n", time.Since(start), mem[0])

	start = time.Now()
	p2Count := 0
	for i := range 100 {
		mem := make([]int, 16)
		mem[0] = i
		if !program.run(mem) {
			p2Count++
		}
	}
	fmt.Printf("Part 2 (%s): %d\n", time.Since(start), p2Count)

	start = time.Now()
	var wg sync.WaitGroup
	p3Counts := make([]int, 16)
	for j := range 16 {
		k := j
		wg.Go(func() {
			count := 0
			for i := range 65536 {
				mem := make([]int, 16)
				mem[0] = i
				mem[1] = k
				if !program.run(mem) {
					count++
				}
			}
			p3Counts[k] = count
		})
	}
	wg.Wait()
	p3Count := 0
	for _, c := range p3Counts {
		p3Count += c
	}
	fmt.Printf("Part 3 (%s): %d\n", time.Since(start), p3Count)
}
