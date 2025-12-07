package helpers

import (
	"strings"
	sets "github.com/deckarep/golang-set/v2"
)

func ParseOneNumber(data string) int {
	return Atoi(data)
}

func ParseOneNumberPerLine(data string) []int {
	lines := strings.Split(data, "\n")
	numbers := make([]int, len(lines))
	for i, line := range lines {
		numbers[i] = Atoi(line)
	}
	return numbers
}

func ParseMultiNumbersPerLine(data string) [][]int {
	lines := strings.Split(data, "\n")
	numbers := make([][]int, len(lines))
	for l, line := range lines {
		words := strings.Fields(line)
		nums := make([]int, len(words))
		for i, word := range words {
			nums[i] = Atoi(word)
		}
		numbers[l] = nums
	}
	return numbers
}

func ParseOneLineMultiNumbers(data string) []int {
	words := strings.Fields(data)
	numbers := make([]int, len(words))
	for i, word := range words {
		numbers[i] = Atoi(word)
	}
	return numbers
}

func ParseMultiWordsPerLine(data string) [][]string {
	lines := strings.Split(data, "\n")
	words := make([][]string, len(lines))
	for l, line := range lines {
		words[l] = strings.Fields(line)
	}
	return words
}

func ParseCharCoords(data string) map[rune]sets.Set[[2]int] {
	c := make(map[rune]sets.Set[[2]int])
	for y, line := range strings.Split(data, "\n") {
		for x, char := range line {
			if _, ok := c[char]; !ok {
				c[char] = sets.NewSet[[2]int]()
			}
			c[char].Add([2]int{x, y})
		}
	}
	return c
}
