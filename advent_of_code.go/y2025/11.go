package y2025

import (
	// "slices"
	"strconv"
	"strings"

	// sets "github.com/deckarep/golang-set/v2"
	"isaacgood.com/aoc/helpers"
)

type dpArgs struct {
	node string
	seen int
}

// Day11 solves 2025/11.
type Day11 struct {
	dp    map[dpArgs]uint64
	graph map[string][]string
}

func (q *Day11) paths(args dpArgs) uint64 {
	if out, ok := q.dp[args]; ok {
		return out
	}
	node := args.node
	seen := args.seen
	if node == "out" {
		if seen == 2 {
			return 1
		}
		return 0
	}
	if node == "dac" || node == "fft" {
		seen++
	}

	var out uint64
	for _, nextNode := range q.graph[node] {
		out += q.paths(dpArgs{nextNode, seen})
	}

	q.dp[args] = out
	return out
}

// Solve returns the solution for one part.
func (q *Day11) Solve(data string, part int) string {
	graph := make(map[string][]string)
	for _, line := range strings.Split(data, "\n") {
		nodes := strings.Fields(strings.Replace(line, ":", "", 1))
		graph[nodes[0]] = nodes[1:]
	}
	q.graph = graph
	q.dp = make(map[dpArgs]uint64)

	var out uint64
	if part == 1 {
		out = q.paths(dpArgs{"you", 2})
	} else {
		out = q.paths(dpArgs{"svr", 0})
	}
	return strconv.FormatUint(out, 10)
}

func init() {
	helpers.AocRegister(2025, 11, &Day11{})
}
