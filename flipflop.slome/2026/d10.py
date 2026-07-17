"""FlipFlop Codes: N."""

from lib import helpers, parsers


class Computer:
    def __init__(self, data: list[str]):
        instructions = []
        label = {}
        for idx, line in enumerate(data):
            if line.startswith("be"):
                label[len(line.removeprefix("be")) // 2] = idx + 1
                instructions.append((-1, []))
            elif line.startswith("ba"):
                line = line.removeprefix("ba")
                instr, *args = [len(part) // 2 for part in  line.split("ne")]
                instructions.append((instr, *args))
        self.instructions = instructions
        self.label = label
        self.data = data

    def run(self, reg: list[int]) -> tuple[list[int], bool]:
        ptr = 0
        instructions = self.instructions
        label = self.label
        counter = 0
        while ptr >= 0 and ptr < len(instructions) and counter < 5000000:
            instr, *args = instructions[ptr]
            ptr += 1

            if instr != -1:
                counter += 1

            if instr == -1:
                pass
            elif instr == 0:
                reg[args[1]] = args[0]
            elif instr == 1:
                reg[args[1]] = reg[args[0]]
            elif instr == 2:
                reg[args[2]] = (reg[args[0]] + reg[args[1]]) % 65536
            elif instr == 3:
                reg[args[2]] = (reg[args[0]] - reg[args[1]]) % 65536
            elif instr == 4:
                reg[args[2]] = (reg[args[0]] * reg[args[1]]) % 65536
            elif instr == 5:
                reg[args[2]] = 0 if reg[args[1]] == 0 else reg[args[0]] % reg[args[1]]
            elif instr == 6:
                reg[args[0]] = (reg[args[0]] + 1) % 65536
            elif instr == 7:
                reg[args[0]] = (reg[args[0]] - 1) % 65536
            elif instr == 8:
                ptr = label[args[0]]
            elif instr == 9:
                if reg[args[0]] == 0:
                    ptr = label[args[1]]
            elif instr == 10:
                if reg[args[0]] != 0:
                    ptr = label[args[1]]
        return reg, counter <= 5000000

    def as_go_code(self):
        """Print out the Banenalang code translated to Go."""
        count_check = "\tif count > 5000000 { return false }"
        out = []
        for idx, line in enumerate(self.data):
            if line.startswith("be"):
                label = len(line.removeprefix("be")) // 2
                out.append(f"LABEL_{label}:")
                out.append(count_check)
            elif line.startswith("ba"):
                line = line.removeprefix("ba")
                instr, *args = [len(part) // 2 for part in  line.split("ne")]
                if instr == 0:
                    out.append(f"\treg[{args[1]}] = {args[0]}")
                elif instr == 1:
                    out.append(f"\treg[{args[1]}] = reg[{args[0]}]")
                elif instr == 2:
                    out.append(f"\treg[{args[2]}] = mod(reg[{args[0]}] + reg[{args[1]}])")
                elif instr == 3:
                    out.append(f"\treg[{args[2]}] = mod(reg[{args[0]}] - reg[{args[1]}])")
                elif instr == 4:
                    out.append(f"\treg[{args[2]}] = mod(reg[{args[0]}] * reg[{args[1]}])")
                elif instr == 5:
                    out.append(f"\tif reg[{args[1]}] == 0 {{ reg[{args[2]}] = 0 }} else {{ reg[{args[2]}] = reg[{args[0]}] % reg[{args[1]}] }}")
                elif instr == 6:
                    out.append(f"\treg[{args[0]}] = mod(reg[{args[0]}] + 1)")
                elif instr == 7:
                    out.append(f"\treg[{args[0]}] = mod(reg[{args[0]}] - 1)")
                elif instr == 8:
                    out.append(f"\tgoto LABEL_{args[0]}")
                elif instr == 9:
                    out.append(f"\tif reg[{args[0]}] == 0 {{ goto LABEL_{args[1]} }}")
                elif instr == 10:
                    out.append(f"\tif reg[{args[0]}] != 0 {{ goto LABEL_{args[1]} }}")
                out.append("\tcount++")
        pre = """\
package main

import (
	"fmt"
	"sync"
	"time"
)

func mod(i int) int {
	for i < 0 {
		i += 65536
	}
	return i % 65536
}

func check(reg []int) bool {
	var count int"""

	post = """\
	if count > 5000000 { return false }
	return true
}

func main() {
	start := time.Now()
	mem := make([]int, 16)
	check(mem)
	fmt.Printf("Part 1 (%s): %d\n", time.Since(start), mem[0])

	start = time.Now()
	p2Count := 0
	for i := range 100 {
		mem := make([]int, 16)
		mem[0] = i
		if !check(mem) {
			p2Count++
		}
	}
	fmt.Printf("Part 2 (%s): %d\n", time.Since(start), p2Count)

	var wg sync.WaitGroup
	p3Counts := make([]int, 16)
	for j := range 16 {
		k := j
		wg.Go(func() {
			count := 0
			for i := range 65536 {
				mem := make([]int, 16)
				mem[0] = i
				mem[1] = k
				if !check(mem) {
					count++
				}
			}
			p3Counts[k] = count
		})
	}
	wg.Wait()
	p3Count := 0
	for _, c := range p3Counts {
		p3Count += c
	}
	fmt.Printf("Part 3 (%s): %d\n", time.Since(start), p3Count)
}"""
        print(pre + "\n" + "\n".join(out) + "\n" + post)


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    if part == 1:
        reg = [0] * 16
        reg, _ = Computer(data).run(reg)
        return str(reg)

    if part == 2:
        count = 0
        for start in range(100):
            reg = [start] + [0] * 15
            _, finished = Computer(data).run(reg)
            if not finished:
                count += 1
        return count

    if part == 3:
        count = 0
        for a in range(65536):
            for b in range(16):
                reg = [a, b] + [0] * 14
                _, finished = Computer(data).run(reg)
                if not finished:
                    count += 1
            if a % 10 == 0:
                print(a, count)
        return count



WANT = []
# PARSER = parsers.parse_one_str
TEST_DATA = [
    """\
banenanena
banenananenana
banenanananenanana
banananenanenananenananana
banananenananananenanananenanananana
bananenananananane""",
    """\
banenane
banenananananananananananena
banenanananananananananananananananananananananananananananananananananenana
banenanananananananananananananenanana
banenananananananananananananananananananananananananananananananananananananananenananana
banananenenananane
bananananenenanane
banananananenenanananane
bananananananenenane
banananananananane
banananananananane
bananananananane
banananananananena
banananananananenana
banananananananenanana
banananananananenananana""",
    """\
banenanane
banananananenenena
banananananenanenanenana
banananananenananenananenanana
banananenanananenanananenananana
banananenananananenananananenanananana
banananenanananananenanananananenananananana
banananenananananananenananananananenanananananana
banananenanananananananenanananananananenananananananana
banananenananananananananenananananananananenanananananananana
banananenanananananananananenanananananananananenananananananananana""",
    """\
banenane
banananananananananenananananananana
banenanena
be
banenanenana
banananananananananenanana
benana
banenanenanana
banananananananananena
benanana
banenanenananana
banananananananananenana
benananananananananana
banenanenanananana
bananananananananane
benananananananananananana
banenanenananananana
benanananananananana
banenanenanananananana
benananananananana
banenanenananananananana
banananananananananenananananananananana
bena
banenanenanananananananana""",
    """\
banenananenana
banenananananananananananenanananananananananananananana
be
banananenanenananena
banananananananenanana
bananananananananenananana
bananananananananenanananananananananananananana
banananananananananananenananananananananananananananane""",
    """\
banenananananananananananananananananananananena
benanana
bananananananananena
banenananananananananananananananenana
benananana
bananananananananenana
banenananananananananananenanana
bena
bananananananananenanana
banananenenane
banananenananene
banananananananananananenanananena
banananananananananananenananenananana
banananananananananananenanenanana
banenanena
bananananananananane
banene
be
bananananananananena
bananananananane
bananananananananananenane""",
    """\
banenanena
banenanananananananananananananananenanana
be
banananenenanenana
bananenane
bananenananena
bananananananananenanana
banananananananananananenananane
banenena
banenenana"""]
TESTS = [
    (1, TEST_DATA[0], "[6, 1, 2, 3, 3, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]"),
    (1, TEST_DATA[1], "[3, 11, 34, 14, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]"),
    (1, TEST_DATA[2], "[2, 4, 16, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 0, 0, 0, 0, 0]"),
    (1, TEST_DATA[3], "[1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]"),
    (1, TEST_DATA[4], "[0, 20, 2, 10, 65526, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]"),
    (1, TEST_DATA[5], "[44802, 65535, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]"),
    (1, TEST_DATA[6], "[610, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]"),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
