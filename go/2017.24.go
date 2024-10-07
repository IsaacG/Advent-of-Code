package main

import "strings"

// magneticComponent represents a magnetic component with two ports, each of which have a fixed number of pins.
type magneticComponent struct {
	one, two int
}

// Function other returns the number of pins on the other port, if this port exists.
func (mc magneticComponent) other(this int) (int, bool) {
	if this == mc.one {
		return mc.two, true
	}
	if this == mc.two {
		return mc.one, true
	}
	return 0, false
}

// Function strength returns the strength of a magnetic component.
func (mc magneticComponent) strength() int {
	return mc.one + mc.two
}

// Day201724 solves 2017/24.
type Day201724 struct {
	components []magneticComponent
}

// New201724 returns a new solver for 2017/24.
func New201724() *Day201724 {
	return &Day201724{}
}

// SetInput handles input for this solver.
func (p *Day201724) SetInput(data string) {
	lines := strings.Split(data, "\n")
	for _, line := range lines {
		ports := strings.Split(line, "/")
		p.components = append(p.components, magneticComponent{Atoi(ports[0]), Atoi(ports[1])})
	}
}

// Function build returns the max strength of a bridge which can be built with a set of components and starting with start pins.
func (p *Day201724) build(start int, components []magneticComponent) (int, int, int) {
	maxStrongest, maxLongest, maxLength := 0, 0, 0
	// lastIndex is a helper to access the last index, used to swap (removing an element from the slice).
	lastIndex := len(components) - 1
	for i, component := range components {
		// Check if this component can be used to start this (sub)bridge.
		other, ok := component.other(start)
		if !ok {
			continue
		}
		strength := component.strength()

		// Component the characteristics of a sub-bridge excluding this component.
		// Swap a component to the end of the slice then shorten the slice to "remove" the component.
		components[i], components[lastIndex] = components[lastIndex], components[i]
		strongest, longest, length := p.build(other, components[:lastIndex])
		components[i], components[lastIndex] = components[lastIndex], components[i]

		// Add this component to the bridge characteristics.
		strongest += strength
		longest += strength
		length++

		// Update max values.
		if strongest > maxStrongest {
			maxStrongest = strongest
		}
		if length > maxLength || (length == maxLength && longest > maxLongest) {
			maxLength = length
			maxLongest = longest
		}
	}
	return maxStrongest, maxLongest, maxLength
}

// Solve returns the solution for one part.
func (p *Day201724) Solve(part int) string {
	strongest, longest, _ := p.build(0, p.components)
	var result int
	if part == 0 {
		result = strongest
	} else {
		result = longest
	}
	return Itoa(result)
}
