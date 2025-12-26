package y2019

import (
	"fmt"
	"isaacgood.com/aoc/helpers"
	"strings"
)

const (
	StateReady = iota
	StateRun
	StateIOBlock
	StateHalt
)

const (
	OpAdd    = 1
	OpMult   = 2
	OpInput  = 3
	OpOutput = 4
	OpJumpT  = 5
	OpJumpF  = 6
	OpLT     = 7
	OpEQ     = 8
	OpHalt   = 99
)

type IntCode struct {
	mem    map[int]int
	pc     int
	input  <-chan int
	output chan<- int
	debug  bool
	state  int
}

func (ic *IntCode) nextPc() int {
	v := ic.mem[ic.pc]
	ic.pc++
	return v
}

func (ic *IntCode) getVal(mode int) int {
	pc := ic.nextPc()
	// Position mode 0
	if mode == 0 {
		return ic.mem[pc]
	}
	// Immediate mode 1
	if mode == 1 {
		return pc
	}
	return 0
}

func (ic *IntCode) run() {
	ic.state = StateRun
	for {
		op := ic.mem[ic.pc]
		ic.pc++
		switch op % 100 {
		case OpAdd:
			if ic.debug {
				fmt.Printf("ADD  %4d %4d -> %4d\n", ic.mem[ic.pc+0], ic.mem[ic.pc+1], ic.mem[ic.pc+2])
			}
			r := ic.getVal((op/100)%10) + ic.getVal((op/1000)%10)
			ic.mem[ic.nextPc()] = r
		case OpMult:
			if ic.debug {
				fmt.Printf("MULT %4d %4d -> %4d\n", ic.mem[ic.pc+0], ic.mem[ic.pc+1], ic.mem[ic.pc+2])
			}
			r := ic.getVal((op/100)%10) * ic.getVal((op/1000)%10)
			ic.mem[ic.nextPc()] = r
		case OpInput:
			v := <-ic.input
			if ic.debug {
				fmt.Printf("INPT %d -> %4d\n", v, ic.mem[ic.pc+0])
			}
			ic.mem[ic.nextPc()] = v
		case OpOutput:
			v := ic.getVal(op / 100 % 10)
			if ic.debug {
				fmt.Printf("OUTP %d\n", v)
			}
			ic.output <- v
		case OpJumpT:
			cmp, dst := ic.getVal(op/100%10), ic.getVal(op/1000%10)
			if ic.debug {
				fmt.Printf("JMPT %d %d\n", cmp, dst)
			}
			if cmp != 0 {
				ic.pc = dst
			}
		case OpJumpF:
			cmp, dst := ic.getVal(op/100%10), ic.getVal(op/1000%10)
			if ic.debug {
				fmt.Printf("JMPF %d %d\n", cmp, dst)
			}
			if cmp == 0 {
				ic.pc = dst
			}
		case OpLT:
			a, b, dst := ic.getVal(op/100%10), ic.getVal(op/1000%10), ic.nextPc()
			if ic.debug {
				fmt.Printf("LT %d %s -> %d\n", a, b, dst)
			}
			if a < b {
				ic.mem[dst] = 1
			} else {
				ic.mem[dst] = 0
			}
		case OpEQ:
			a, b, dst := ic.getVal(op/100%10), ic.getVal(op/1000%10), ic.nextPc()
			if ic.debug {
				fmt.Printf("EQ %d %s -> %d\n", a, b, dst)
			}
			if a == b {
				ic.mem[dst] = 1
			} else {
				ic.mem[dst] = 0
			}
		case OpHalt:
			if ic.debug {
				fmt.Println("HALT")
			}
			ic.state = StateHalt
			return
		}
	}
}

func NewIntCode(program string, debug bool, input <-chan int, output chan<- int) *IntCode {
	mem := make(map[int]int)
	for i, v := range strings.Split(program, ",") {
		mem[i] = helpers.Atoi(v)
	}
	return &IntCode{mem: mem, input: input, output: output, debug: debug, state: StateReady}
}
