import functools
import io
import itertools
import os
import re
import sys

def part1(filename):
	print("Part 1: {}".format(len([position for position in itertools.accumulate(((-1 if direction == "L" else 1) * int(distance) for (direction, distance) in re.findall(r"([LR])(\d+)", io.open(filename, mode = 'r').read())), lambda position, rotation: (position + rotation) % 100, initial=50) if position == 0])))

def part2(filename):
	print("Part 2: {}".format(functools.reduce(lambda pos_clicks, rotation: ((pos_clicks[0] + rotation) % 100, pos_clicks[1] + (abs((pos_clicks[0] if pos_clicks[0] or rotation > 0 else 100) - 50 + rotation) + 50) // 100), ((-1 if direction == "L" else 1) * int(distance) for (direction, distance) in re.findall(r"([LR])(\d+)", io.open(filename, mode = 'r').read())), (50, 0))[1]))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
