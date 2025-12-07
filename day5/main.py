import functools
import io
import itertools
import more_itertools
import os
import re
import sys

def part1(filename):
	print("Part 1: {}".format((lambda fresh_ranges_str, ingredients_str: len(list(filter(lambda ingredient: any(ingredient in fresh_range for fresh_range in [range(int(lower), int(upper) + 1) for lower, upper in re.findall(r"(\d+)-(\d+)", fresh_ranges_str)]), map(int, re.findall(r"(\d+)", ingredients_str))))))(*io.open(filename, mode = 'r').read().strip().split("\n\n"))))

def part2(filename):
	print("Part 2: {}".format(sum(map(len, itertools.accumulate(list(sorted((range(int(lower), int(upper) + 1) for lower, upper in re.findall(r"(\d+)-(\d+)", io.open(filename, mode = 'r').read())), key=lambda fresh_range: fresh_range.start)), lambda prev_range, curr_range: range(max(curr_range.start, prev_range.stop), max(curr_range.stop, prev_range.stop)))))))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
