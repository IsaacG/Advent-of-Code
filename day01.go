package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

func check(err error) {
	if err != nil {
		panic(err)
	}
}

func main() {
	nums := make(map[int]bool)
	target := 2020

	data, err := ioutil.ReadFile(os.Args[1])
	check(err)

	for _, s := range strings.Split(string(data), "\n") {
		if s == "" {
			continue
		}
		n, err := strconv.Atoi(s)
		check(err)

		nums[n] = true
	}

	for n, _ := range nums {
		if _, has := nums[target-n]; has != false {
			fmt.Printf("Part one: %d\n", n*(target-n))
			break
		}
	}

	found := false
	for n, _ := range nums {
		for o, _ := range nums {
			p := target - n - o
			if _, has := nums[p]; has != false {
				fmt.Printf("Part two: %d\n", n*o*p)
				found = true
				break
			}
		}
		if found {
			break
		}
	}
}
