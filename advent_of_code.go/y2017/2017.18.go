package y2017

import (
	"isaacgood.com/aoc/helpers"
	"strconv"
	"strings"
	"sync"
)

// Day18 solves 2017/18.
type Day18 struct {
	instructions [][]string
}
type semaphore struct {
	Count int
	Mu    sync.Mutex
}

type program struct {
	ID           int
	Snd          chan<- int
	Rcv          <-chan int
	SendCount    int
	Registers    map[string]int
	Instructions [][]string
	Ptr          int
	Wg           *sync.WaitGroup
	sem          *semaphore
}

func newProgram(id int, snd, rcv chan int, instructions [][]string, wg *sync.WaitGroup, sem *semaphore) *program {
	wg.Add(1)
	return &program{
		ID:           id,
		Snd:          snd,
		Rcv:          rcv,
		Registers:    map[string]int{"p": id},
		Instructions: instructions,
		Wg:           wg,
		sem:          sem,

		SendCount: 0,
	}
}

func (p *program) getValue(val string) int {
	num, err := strconv.Atoi(val)
	if err == nil {
		return num
	}
	return p.Registers[val]
}

func (p *program) Run() {
	var instruction []string
	for true {
		instruction = p.Instructions[p.Ptr]
		task := instruction[0]
		X := instruction[1]
		var Y string
		if len(instruction) > 2 {
			Y = instruction[2]
		}
		switch task {
		case "set":
			p.Registers[X] = p.getValue(Y)
		case "add":
			p.Registers[X] += p.getValue(Y)
		case "mul":
			p.Registers[X] *= p.getValue(Y)
		case "mod":
			p.Registers[X] %= p.getValue(Y)
		case "jgz":
			if p.getValue(X) > 0 {
				p.Ptr += p.getValue(Y) - 1
			}
		case "snd":
			p.SendCount++
			p.Snd <- p.getValue(X)
		case "rcv":
			func() {
				p.sem.Mu.Lock()
				defer p.sem.Mu.Unlock()
				p.sem.Count--
				if p.sem.Count == 0 {
					p.Wg.Done()
					return
				}
				p.Registers[X] = <-p.Rcv
				p.sem.Count++
			}()
		}
		p.Ptr++
	}
}

// New18 returns a new solver for 2017/18.
func New18() *Day18 {
	return &Day18{}
}

// SetInput handles input for this solver.
func (p *Day18) SetInput(data string) {
	for _, line := range strings.Split(string(data), "\n") {
		if line == "" {
			continue
		}
		words := strings.Split(line, " ")
		p.instructions = append(p.instructions, words)
	}
}

// Solve returns the solution for one part.
func (p *Day18) Solve(part int) string {
	if part == 1 {
		return ""
	}

	chanOne := make(chan int, 100)
	chanTwo := make(chan int, 100)
	var wg sync.WaitGroup
	sem := &semaphore{Count: 2}

	p0 := newProgram(0, chanOne, chanTwo, p.instructions, &wg, sem)
	p1 := newProgram(1, chanTwo, chanOne, p.instructions, &wg, sem)
	go p0.Run()
	go p1.Run()

	wg.Wait()
	return helpers.Itoa(p1.SendCount)
}
