package e2025

// Clamp b between and c.
func Clamp(a, b, c int) int {
	if b < a {
		return a
	}
	if b > c {
		return c
	}
	return b
}

// Sum up an int slice.
func Sum(i []int) int {
	total := 0
	for _, j := range i {
		total += j
	}
	return total
}
