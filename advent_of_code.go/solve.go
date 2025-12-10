package main

import (
	"fmt"
	"isaacgood.com/aoc/helpers"
	_ "isaacgood.com/aoc/y2017"
	_ "isaacgood.com/aoc/y2020"
	_ "isaacgood.com/aoc/y2024"
	_ "isaacgood.com/aoc/y2025"
	"os"
	"time"
)

func main() {
	fmt.Println(time.Now())
	helpers.CheckAocPuzzles(os.Args)
}
