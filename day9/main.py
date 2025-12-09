import functools
import io
import itertools
import more_itertools
import operator
import os
import re
import sys

def part1(filename):
	print("Part 1: {}".format(max((abs(ax - bx) + 1) * (abs(ay - by) + 1) for (ax, ay), (bx, by) in itertools.combinations(((int(x), int(y)) for x, y in re.findall(r"(\d+),(\d+)", io.open(filename, mode = 'r').read())), 2))))

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		red_tiles = [(int(x), int(y)) for x, y in re.findall(r"(\d+),(\d+)", file.read())]
	x_lines = []
	y_lines = []
	prev_x, prev_y = red_tiles[-1]
	for i in range(len(red_tiles)):
		x, y = red_tiles[i]
		if x == prev_x:
			yl, yu = sorted((prev_y, y))
			y_lines.append((x, range(yl, yu + 1)))
		else:
			xl, xu = sorted((prev_x, x))
			x_lines.append((range(xl, xu + 1), y))
		prev_x = x
		prev_y = y
	x_lines.sort(key=lambda x_line: len(x_line[0]), reverse=True)
	y_lines.sort(key=lambda y_line: len(y_line[1]), reverse=True)
	rectangles = [((xu - xl + 1) * (yu - yl + 1), range(xl + 1, xu), range(yl + 1, yu)) for (xl, xu), (yl, yu) in (((min(ax, bx), max(ax, bx)), (min(ay, by), max(ay, by))) for (ax, ay), (bx, by) in itertools.combinations(red_tiles, 2))]
	result = 0
	for area, x_range, y_range in sorted(rectangles, key=lambda rectangle: rectangle[0], reverse=True):
		if any(y in y_range and (x_line.start in x_range or x_line.stop - 1 in x_range or x_range.start in x_line) for x_line, y in x_lines):
			continue
		if any(x in x_range and (y_line.start in y_range or y_line.stop - 1 in y_range or y_range.start in y_line) for x, y_line in y_lines):
			continue
		result = area
		break
	print("Part 2: {}".format(result))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
