package e2025

import (
	// "fmt"
	// "slices"
	"strings"

	sets "github.com/deckarep/golang-set/v2"
	"isaacgood.com/everybodycodes/helpers"
)

// Quest09 for Event 2025.
type Quest09 struct{
	dnas map[int]string
}

func (q Quest09) findParents() [][3]int {
	dnas := q.dnas

	bucketed := make(map[byte][]int)
	for scale, dna := range dnas {
		bucketed[dna[4]] = append(bucketed[dna[4]], scale)
	}

	var parents [][3]int
	for childScale, childDNA := range dnas {
		matched := false
		for p1Scale, p1DNA := range dnas {
			if childScale == p1Scale {
				continue
			}
			for _, p2Scale := range bucketed[childDNA[4]] {
				if childScale == p2Scale || p1Scale == p2Scale {
					continue
				}
				p2DNA := dnas[p2Scale]
				isMatch := true
				for i := range(len(childDNA)) {
					if childDNA[i] != p1DNA[i] && childDNA[i] != p2DNA[i] {
						isMatch = false
						break
					}
				}
				if isMatch {
					matched = true
					parents = append(parents, [3]int{childScale, p1Scale, p2Scale})
					break
				}
			}
			if matched {
				break
			}
		}
	}
	return parents
}

func (q Quest09) matches(i, j int) int {
	a, b := q.dnas[i], q.dnas[j]
	count := 0
	for i := range(len(a)) {
		if a[i] == b[i] {
			count++
		}
	}
	return count
}

// Solve Quest 9.
func (q Quest09) Solve(data string, part int) string {
	dnas := make(map[int]string)
	for _, line := range strings.Split(data, "\n") {
		parts := strings.Split(line, ":")
		dnas[helpers.Atoi(parts[0])] = parts[1]
	}
	q.dnas = dnas
	parents := q.findParents()

	if part != 3 {
		total := 0
		for _, family := range parents {
			total += q.matches(family[0], family[1]) * q.matches(family[0], family[2])
		}
		return helpers.Itoa(total)
	}

	// Convert to a set.
	groups := sets.NewSet[sets.Set[int]]()
	for _, family := range parents {
		groups.Add(sets.NewSet(family[0], family[1], family[2]))
	}
	// Combine groups.
	priorSize := 0
	for priorSize != groups.Cardinality() {
		priorSize = groups.Cardinality()
		newGroups := sets.NewSet[sets.Set[int]]()
		for !groups.IsEmpty() {
			one, _ := groups.Pop()
			for _, other := range groups.ToSlice() {
				if one.ContainsAnyElement(other) {
					one = one.Union(other)
					groups.Remove(other)
				}
			}
			newGroups.Add(one)
		}
		groups = newGroups
	}

	total, size := 0, 0
	for group := range groups.Iter() {
		if group.Cardinality() > size {
			size = group.Cardinality()
			total = 0
			for scale := range group.Iter() {
				total += scale
			}
		}
	}
	return helpers.Itoa(total)
}
