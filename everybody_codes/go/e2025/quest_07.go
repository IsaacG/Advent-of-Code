package e2025

import (
	"slices"
	"strings"

	sets "github.com/deckarep/golang-set/v2"
	"isaacgood.com/everybodycodes/helpers"
)

// Quest07 for Event 2025.
type Quest07 struct {
	ruleAfter map[string][]string
	dpCache   map[int]map[string]int
}

// filterNames returns unique names and excludes names which have a prefix.
func (q Quest07) filterNames(names []string) []string {
	uniqueNames := sets.NewSet(names...).ToSlice()
	names = []string{}
	for idx, name := range uniqueNames {
		hasPrefix := false
		for idxOther, nameOther := range uniqueNames {
			if strings.HasPrefix(name, nameOther) && idx != idxOther {
				hasPrefix = true
				break
			}
		}
		if !hasPrefix {
			names = append(names, name)
		}
	}
	return names
}

// possibilities returns how many possible names can be formed
// given an existing size and trailing letter. Uses DP.
func (q Quest07) possibilities(size int, letter string) int {
	if size == 11 {
		return 1
	}
	if cached, ok := q.dpCache[size][letter]; ok {
		return cached
	}
	count := 0
	if size >= 7 {
		count++
	}
	for _, char := range q.ruleAfter[letter] {
		count += q.possibilities(size+1, char)
	}

	q.dpCache[size][letter] = count
	return count
}

// Solve Quest 7.
func (q Quest07) Solve(data string, part int) string {
	blocks := strings.Split(data, "\n\n")
	names := strings.Split(blocks[0], ",")

	ruleAfter := make(map[string][]string)
	for line := range strings.SplitSeq(blocks[1], "\n") {
		parts := strings.Split(line, " > ")
		ruleAfter[parts[0]] = strings.Split(parts[1], ",")
	}

	total := 0
	if part == 3 {
		names = q.filterNames(names)
		q.ruleAfter = ruleAfter
		q.dpCache = make(map[int]map[string]int)
		for i := range 12 {
			q.dpCache[i] = make(map[string]int)
		}
	}

	for idxName, name := range names {
		valid := true
		for idx := 0; idx < len(name)-1; idx++ {
			if !slices.Contains(ruleAfter[name[idx:idx+1]], name[idx+1:idx+2]) {
				valid = false
				break
			}
		}
		if valid {
			switch part {
			case 1:
				return name
			case 2:
				total += idxName + 1
			case 3:
				total += q.possibilities(len(name), name[len(name)-1:])
			}
		}
	}

	return helpers.Itoa(total)
}
