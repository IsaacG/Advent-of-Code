package y2024

import (
	"isaacgood.com/aoc/helpers"
)

const (
	target = 2024
)

func check(err error) {
	if err != nil {
		panic(err)
	}
}

func abs(n int) int     { return helpers.Abs(n) }
func sign(n int) int    { return helpers.Sign(n) }
func itoa(n int) string { return helpers.Itoa(n) }
func atoi(n string) int { return helpers.Atoi(n) }
