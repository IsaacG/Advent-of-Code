import itertools
import pathlib

def part1():
    data = pathlib.Path("inputs/01.1.txt").read_text().rstrip()
    costs = {"A": 0, "B": 1, "C": 3}
    return sum(costs[char] for char in data) 

def part2():
    actual_data = pathlib.Path("inputs/01.2.txt").read_text().rstrip()
    test_data = "AxBCDDCAxD"
    costs = {"A": 0, "B": 1, "C": 3, "D": 5, "x": 0}

    def solve(data):
        total = 0
        for a, b in zip(data[::2], data[1::2]):
            total += costs[a] + costs[b]
            if "x" not in [a, b]:
                total += 2
        return total

    assert solve(test_data) == 28, solve(test_data)
    return solve(actual_data)

def part3():
    actual_data = pathlib.Path("inputs/01.3.txt").read_text().rstrip()
    test_data = "xBxAAABCDxCC"
    costs = {"A": 0, "B": 1, "C": 3, "D": 5, "x": 0}

    def solve(data):
        total = 0
        for a, b, c in zip(data[::3], data[1::3], data[2::3]):
            group_cost = costs[a] + costs[b] + costs[c]
            group_size = sum(char != "x" for char in [a, b, c])
            if group_size == 2:
                group_cost += 2
            elif group_size == 3:
                group_cost += 6
            print(f"{a}{b}{c} = {group_cost}")
            total += group_cost
        return total

    assert solve(test_data) == 30, solve(test_data)
    return solve(actual_data)


print("Part one:", part1())
print("Part two:", part2())
print("Part three:", part3())
