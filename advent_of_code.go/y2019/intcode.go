package y2019

import (
	"fmt"
	"isaacgood.com/aoc/helpers"
	"strings"
	"time"
)

const (
	StateReady = iota
	StateRun
	StateIOBlock
	StateHalt

	ParamModePosition  = 0
	ParamModeImmediate = 1
	ParamModeRelative  = 2

	OpAdd     = 1
	OpMult    = 2
	OpInput   = 3
	OpOutput  = 4
	OpJumpT   = 5
	OpJumpF   = 6
	OpLT      = 7
	OpEQ      = 8
	OpRelBase = 9
	OpHalt    = 99
)

var OpName = map[int]string{
	OpAdd:    "ADD",
	OpMult:   "MULT",
	OpInput:  "INPUT",
	OpOutput: "OUTPUT",
	OpJumpT:  "JUMPT",
	OpJumpF:  "JUMPF",
	OpLT:     "LT",
	OpEQ:     "EQ",
	OpRelBase: "RELATIVE_BASE",
	OpHalt:   "HALT",
}

var OperandCount = map[int][2]int{
	OpAdd:    {2, 1},
	OpMult:   {2, 1},
	OpInput:  {0, 1},
	OpOutput: {1, 0},
	OpJumpT:  {2, 0},
	OpJumpF:  {2, 0},
	OpLT:     {2, 1},
	OpEQ:     {2, 1},
	OpRelBase: {1, 0},
	OpHalt:   {0, 0},
}

type IntCode struct {
	mem          map[int]int
	pc           int
	input        <-chan int
	output       chan<- int
	debug        bool
	state        int
	relativeBase int
}

func read(c <-chan int, wait time.Duration) (int, bool) {
	select {
	case v := <- c:
		return v, true
	case <- time.After(wait):
		return 0, false
	}
}

func write(c chan<- int, val int, wait time.Duration) bool {
	select {
	case c <- val:
		return true
	case <- time.After(wait):
		return false
	}
}

func (ic *IntCode) nextPc() int {
	v := ic.mem[ic.pc]
	ic.pc++
	return v
}

func (ic *IntCode) operands(op int) []int {
	count := OperandCount[op%100]
	out := make([]int, count[0]+count[1])
	op /= 10
	for i := range count[0] {
		op /= 10
		num := ic.nextPc()
		switch op % 10 {
		case ParamModePosition:
			out[i] = ic.mem[num]
		case ParamModeImmediate:
			out[i] = num
		case ParamModeRelative:
			out[i] = ic.mem[num+ic.relativeBase]
		}
	}
	if count[1] == 1 {
		op /= 10
		num := ic.nextPc()
		switch op % 10 {
		case ParamModePosition:
			out[count[0]] = num
		case ParamModeImmediate:
			panic("")
		case ParamModeRelative:
			out[count[0]] = num+ic.relativeBase
		}
	}
	return out
}

func (ic *IntCode) run() {
	ic.state = StateRun
	for {
		op := ic.nextPc()
		instruction := op % 100
		var bareParams []int
		if ic.debug {
			count := OperandCount[instruction]
			for i := range count[0] + count[1] {
				bareParams = append(bareParams, ic.mem[ic.pc+i])
			}
		}
		params := ic.operands(op)
		if ic.debug {
			fmt.Printf("%5d %-6s %18s=%28s\n", op, OpName[instruction], fmt.Sprintf("%4v", bareParams), fmt.Sprintf("%8v", params))
		}
		switch instruction {
		case OpAdd:
			ic.mem[params[2]] = params[0] + params[1]
		case OpMult:
			ic.mem[params[2]] = params[0] * params[1]
		case OpInput:
			v := <-ic.input
			ic.mem[params[0]] = v
		case OpOutput:
			ic.output <- params[0]
		case OpJumpT:
			if params[0] != 0 {
				ic.pc = params[1]
			}
		case OpJumpF:
			if params[0] == 0 {
				ic.pc = params[1]
			}
		case OpLT:
			if params[0] < params[1] {
				ic.mem[params[2]] = 1
			} else {
				ic.mem[params[2]] = 0
			}
		case OpEQ:
			if params[0] == params[1] {
				ic.mem[params[2]] = 1
			} else {
				ic.mem[params[2]] = 0
			}
		case OpRelBase:
			ic.relativeBase += params[0]
		case OpHalt:
			ic.state = StateHalt
			return
		default:
			panic(fmt.Sprintf("Unhandled op %d", op))
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
