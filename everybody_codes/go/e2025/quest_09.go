package e2025

import (
	// "fmt"
	// "slices"
	"strings"

	sets "github.com/deckarep/golang-set/v2"
	"isaacgood.com/everybodycodes/helpers"
)

// Quest09 for Event 2025.
type Quest09 struct {
	dnas map[int]string
}

// BitDNA reduces runtime from ~450ms to ~350ms.
type BitDNA []int64

func (d BitDNA) matches(a, b BitDNA) bool {
	for idx := range len(d) {
		if d[idx]&(a[idx]|b[idx]) != d[idx] {
			return false
		}
	}
	return true
}

func (q Quest09) toBits(dna string) BitDNA {
	nucleotides := map[rune]int64{
		'A': 1,
		'C': 2,
		'G': 4,
		'T': 8,
	}
	var bits []int64
	var num int64
	for idx, char := range dna {
		num = (num << 4) | nucleotides[char]
		if idx%16 == 15 {
			bits = append(bits, num)
			num = 0
		}
	}
	return bits
}

func (q Quest09) findParents() [][3]int {
	dnas := make(map[int]BitDNA)
	for scale, dna := range q.dnas {
		dnas[scale] = q.toBits(dna)
	}

	// Reduces runtime from ~1.5s to ~0.5s.
	bucketed := make(map[int64][]int)
	for scale, dna := range dnas {
		bucketed[dna[0]&0xF] = append(bucketed[dna[0]&0xF], scale)
	}

	var parents [][3]int
	for childScale, childDNA := range dnas {
		matched := false
		for p1Scale, p1DNA := range dnas {
			if childScale == p1Scale {
				continue
			}
			for _, p2Scale := range bucketed[childDNA[0]&0xF] {
				if childScale == p2Scale || p1Scale == p2Scale {
					continue
				}
				p2DNA := dnas[p2Scale]
				if childDNA.matches(p1DNA, p2DNA) {
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
	for i := range len(a) {
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
