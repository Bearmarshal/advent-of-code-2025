import functools
import io
import itertools
import more_itertools
import operator
import os
import re
import sys

def part1(filename):
	with io.open(filename, mode = 'r') as file:
		junction_boxes = [tuple(map(int, (re.findall(r"\d+", line)))) for line in file]
	distances = {((b[0] - a[0])**2 + (b[1] - a[1])**2 + (b[2] - a[2])**2)**0.5: (a, b) for (a, b) in itertools.combinations(junction_boxes, 2)}
	circuits: dict[int, set[tuple[int, int, int]]] = {i: {junction_box} for i, junction_box in enumerate(junction_boxes)}
	for short_distance in more_itertools.take(1000, sorted(distances)):
		a, b = distances[short_distance]
		circuit_a = 0
		circuit_b = 0
		for circuit, circuit_junction_boxes in circuits.items():
			if a in circuit_junction_boxes:
				circuit_a = circuit
			if b in circuit_junction_boxes:
				circuit_b = circuit
			if circuit_a and circuit_b:
				break
		if circuit_a != circuit_b:
			circuits[circuit_a].update(circuits[circuit_b])
			del circuits[circuit_b]
	result = functools.reduce(operator.mul, more_itertools.take(3, sorted(map(len, circuits.values()), reverse=True)))
	print("Part 1: {}".format(result))

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		junction_boxes = [tuple(map(int, (re.findall(r"\d+", line)))) for line in file]
	distances = {((b[0] - a[0])**2 + (b[1] - a[1])**2 + (b[2] - a[2])**2)**0.5: (a, b) for (a, b) in itertools.combinations(junction_boxes, 2)}
	circuits: dict[int, set[tuple[int, int, int]]] = {i: {junction_box} for i, junction_box in enumerate(junction_boxes)}
	for short_distance in sorted(distances):
		a, b = distances[short_distance]
		circuit_a = 0
		circuit_b = 0
		for circuit, circuit_junction_boxes in circuits.items():
			if a in circuit_junction_boxes:
				circuit_a = circuit
			if b in circuit_junction_boxes:
				circuit_b = circuit
			if circuit_a and circuit_b:
				break
		if circuit_a != circuit_b:
			circuits[circuit_a].update(circuits[circuit_b])
			del circuits[circuit_b]
			if len(circuits) == 1:
				break
	print("Part 2: {}".format(a[0] * b[0]))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
