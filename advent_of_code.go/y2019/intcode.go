package y2019

import (
	"isaacgood.com/aoc/helpers"
	"strings"
)

const (
	OpAdd  = 1
	OpMult = 2
	OpHalt = 99
)

type IntCode struct {
	memory map[int]int
	pc     int
}

func (ic *IntCode) nextPc() int {
	v := ic.memory[ic.pc]
	ic.pc++
	return v
}

func (ic *IntCode) memVal() int {
	return ic.memory[ic.nextPc()]
}

func (ic *IntCode) run() {
	for {
		op := ic.memory[ic.pc]
		ic.pc++
		switch op {
		case OpAdd:
			r := ic.memVal() + ic.memVal()
			ic.memory[ic.nextPc()] = r
		case OpMult:
			r := ic.memVal() * ic.memVal()
			ic.memory[ic.nextPc()] = r
		case OpHalt:
			return
		}
	}
}

func NewIntCode(input string) *IntCode {
	memory := make(map[int]int)
	for i, v := range strings.Split(input, ",") {
		memory[i] = helpers.Atoi(v)
	}
	return &IntCode{memory: memory}
}
