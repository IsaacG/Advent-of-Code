package y2017

import (
	"regexp"
	"strings"
	"isaacgood.com/aoc/helpers"
)

var preambleRe = regexp.MustCompile(`Begin in state (.)\.\nPerform a diagnostic checksum after ([0-9]+) steps.`)
var ruleRe = regexp.MustCompile(`In state (.):
  If the current value is 0:
    - Write the value ([01])\.
    - Move one slot to the (left|right)\.
    - Continue with state (.)\.
  If the current value is 1:
    - Write the value ([01])\.
    - Move one slot to the (left|right)\.
    - Continue with state (.)\.`)

type turingRule struct {
	write bool
	move int
	nextState string
}

func newTuringRule(parts []string) *turingRule {
	return &turingRule{
		write: parts[0] == "1",
		move: map[string]int{"left": -1, "right": 1}[parts[1]],
		nextState: parts[2],
	}
}

// Day25 solves 2017/25.
type Day25 struct {
	rules map[string][2]*turingRule
	initialState string
	steps int
}

// New25 returns a new solver for 2017/25.
func New25() *Day25 {
	return &Day25{}
}

// SetInput handles input for this solver.
func (p *Day25) SetInput(data string) {
	chunks := strings.Split(data, "\n\n")
	matches := preambleRe.FindStringSubmatch(chunks[0])
	p.initialState = matches[1]
	p.steps = helpers.Atoi(matches[2])
	p.rules = make(map[string][2]*turingRule)
	for _, chunk := range chunks[1:] {
		matches = ruleRe.FindStringSubmatch(chunk)
		p.rules[matches[1]] = [2]*turingRule{
			newTuringRule(matches[2:5]),
			newTuringRule(matches[5:8]),
		}
	}
}

// Solve returns the solution for one part.
func (p *Day25) Solve(part int) string {
	state := p.initialState
	cursor := 0
	tape := make(map[int]interface{})
	for range(p.steps) {
		var idx int
		if _, ok := tape[cursor]; ok {
			idx = 1
		} else {
			idx = 0
		}
		rule := p.rules[state][idx]
		if rule.write {
			tape[cursor] = struct{}{}
		} else {
			delete(tape, cursor)
		}
		cursor += rule.move
		state = rule.nextState
	}
        return helpers.Itoa(len(tape))
}
