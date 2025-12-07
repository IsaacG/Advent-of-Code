package y2025

import (
	sets "github.com/deckarep/golang-set/v2"
	"isaacgood.com/aoc/helpers"
	"strconv"
	"strings"
)

// Day07 solves 2025/07.
type Day07 struct {
	dpCache       map[[2]int]uint64
	splittersUsed sets.Set[[2]int]
	splitters     sets.Set[[2]int]
	height        int
}

func (p *Day07) timelines(pos [2]int) uint64 {
	if t, ok := p.dpCache[pos]; ok {
		return t
	}
	if pos[1] == p.height {
		return 1
	}
	var t uint64
	pos[1]++
	if p.splitters.Contains(pos) {
		t = p.timelines([2]int{pos[0] - 1, pos[1]}) + p.timelines([2]int{pos[0] + 1, pos[1]})
		p.splittersUsed.Add(pos)
	} else {
		t = p.timelines(pos)
	}

	p.dpCache[pos] = t
	return t
}

// Solve returns the solution for one part.
func (p *Day07) Solve(data string, part int) string {
	coords := helpers.ParseCharCoords(data)
	start, _ := coords['S'].Pop()

	p.dpCache = make(map[[2]int]uint64)
	p.splitters = coords['^']
	p.splittersUsed = sets.NewSet[[2]int]()
	p.height = len(strings.Split(data, "\n"))

	p2 := strconv.FormatUint(p.timelines(start), 10)
	return []string{
		helpers.Itoa(p.splittersUsed.Cardinality()),
		p2,
	}[part-1]
}

func init() {
	helpers.AocRegister(2025, 7, &Day07{})
}
