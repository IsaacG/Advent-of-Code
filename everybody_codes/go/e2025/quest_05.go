package e2025

import (
	"cmp"
	"slices"
	"strconv"
	"strings"

	"isaacgood.com/everybodycodes/helpers"
)

// Quest05 for event 25.
type Quest05 struct{}

// Fishbone is a sword structure.
type Fishbone struct {
	index    int
	segments []*struct{ left, middle, right int }
	spine    int
	rows     []int
}

func (f Fishbone) getRows() []int {
	var rows []int
	for _, segment := range f.segments {
		var parts []string
		for _, n := range []int{segment.left, segment.middle, segment.right} {
			if n != 0 {
				parts = append(parts, helpers.Itoa(n))
			}
		}
		rows = append(rows, helpers.Atoi(strings.Join(parts, "")))
	}
	return rows
}

func (f Fishbone) getSpine() int {
	var parts []string
	for _, segment := range f.segments {
		parts = append(parts, helpers.Itoa(segment.middle))
	}
	return helpers.Atoi(strings.Join(parts, ""))
}

func newFishbone(line string) Fishbone {
	parts := strings.Split(strings.Trim(line, "\n"), ":")
	numbers := strings.Split(parts[1], ",")
	var segments []*struct{ left, middle, right int }
	for _, numRaw := range numbers {
		num := helpers.Atoi(numRaw)
		updated := false
		for _, segment := range segments {
			if num < segment.middle && segment.left == 0 {
				segment.left = num
				updated = true
				break
			} else if num > segment.middle && segment.right == 0 {
				segment.right = num
				updated = true
				break
			}
		}
		if !updated {
			segments = append(segments, &struct{ left, middle, right int }{middle: num})
		}
	}
	f := Fishbone{helpers.Atoi(parts[0]), segments, 0, nil}
	f.spine = f.getSpine()
	f.rows = f.getRows()
	return f
}

// Solve solves one part.
func (q Quest05) Solve(data string, part int) string {
	var swords []Fishbone
	var spines []int
	for line := range strings.Lines(data) {
		sword := newFishbone(line)
		swords = append(swords, sword)
		spines = append(spines, sword.spine)
	}
	switch part {
	case 1:
		return helpers.Itoa(swords[0].spine)
	case 2:
		return helpers.Itoa(slices.Max(spines) - slices.Min(spines))
	}
	slices.SortFunc(swords, func(a, b Fishbone) int {
		if i := cmp.Compare(a.spine, b.spine); i != 0 {
			return -i
		}
		for i := 0; i < slices.Min([]int{len(a.rows), len(b.rows)}); i++ {
			if i := cmp.Compare(a.rows[i], b.rows[i]); i != 0 {
				return -i
			}
		}
		return -cmp.Compare(a.index, b.index)
	})
	total := 0
	for idx, sword := range swords {
		total += (idx + 1) * sword.index
	}
	return strconv.Itoa(total)
}

func init() {
	Puzzles[5] = Quest05{}
}
