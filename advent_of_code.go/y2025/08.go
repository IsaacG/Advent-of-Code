package y2025

import (
	"slices"
	"strings"

	sets "github.com/deckarep/golang-set/v2"
	"isaacgood.com/aoc/helpers"
)

// Day08 solves 2025/08.
type Day08 struct {
	circuits sets.Set[sets.Set[[3]int]]
}

// Connection holds two junction boxes with their distance.
type Connection struct {
	a, b     [3]int
	distance int
}

// distance returns the straight distance between two 3D points.
func (q *Day08) distance(a, b [3]int) int {
	var total int
	for i := range 3 {
		j := a[i] - b[i]
		total += j * j
	}
	return total
}

// circuitWith returns the circuit containing a box, creating a new circuit if none is found.
func (q *Day08) circuitWith(a [3]int) (sets.Set[[3]int], bool) {
	var result sets.Set[[3]int]
	found := false
	for circuit := range q.circuits.Iter() {
		if circuit.Contains(a) {
			found = true
			result = circuit
		}
	}
	if found {
		return result, found
	}
	circuit := sets.NewThreadUnsafeSet[[3]int]()
	circuit.Add(a)
	return circuit, false
}

// Solve returns the solution for one part.
func (q *Day08) Solve(data string, part int) string {
	lines := helpers.ParseMultiNumbersPerLine(strings.ReplaceAll(data, ",", " "))
	boxes := make([][3]int, len(lines))
	numBoxes := len(boxes)
	for i, line := range lines {
		boxes[i] = [3]int{line[0], line[1], line[2]}
	}
	connections := make([]Connection, 0, len(boxes)*len(boxes))
	for idxA, a := range boxes {
		for _, b := range boxes[idxA+1:] {
			connections = append(connections, Connection{a, b, q.distance(a, b)})
		}
	}
	slices.SortFunc(connections, func(a, b Connection) int { return helpers.Cmp(a.distance, b.distance) })

	q.circuits = sets.NewThreadUnsafeSet[sets.Set[[3]int]]()
	for idx, connection := range connections {
		if part == 1 && idx == 1000 {
			sizes := make([]int, 0, q.circuits.Cardinality())
			for circuit := range q.circuits.Iter() {
				sizes = append(sizes, -circuit.Cardinality())
			}
			slices.Sort(sizes)
			prod := 1
			for i := range 3 {
				prod *= sizes[i]
			}
			return helpers.Itoa(-prod)
		}
		circuitA, okA := q.circuitWith(connection.a)
		circuitB, okB := q.circuitWith(connection.b)
		if circuitA == circuitB {
			continue
		}
		if okA {
			q.circuits.Remove(circuitA)
		}
		if okB {
			q.circuits.Remove(circuitB)
		}
		combined := circuitB.Union(circuitA)
		q.circuits.Add(combined)
		if combined.Cardinality() == numBoxes {
			return helpers.Itoa(connection.a[0] * connection.b[0])
		}
	}

	return ""
}

func init() {
	helpers.AocRegister(2025, 8, &Day08{})
}
