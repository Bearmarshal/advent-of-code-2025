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
	with io.open(filename, mode = 'r') as file:
		fresh_ranges_str, ingredients_str = file.read().strip().split("\n\n")
	fresh_ranges = list(sorted((range(int(lower), int(upper) + 1) for lower, upper in re.findall(r"(\d+)-(\d+)", fresh_ranges_str)), key=lambda fresh_range: fresh_range.start))
	merged_ranges = [fresh_ranges.pop(0)]
	for fresh_range in fresh_ranges:
		last_merged = merged_ranges[-1]
		if fresh_range.start <= last_merged.stop:
			if fresh_range.stop > last_merged.stop:
				merged_ranges[-1] = range(last_merged.start, fresh_range.stop)
		else:
			merged_ranges.append(fresh_range)
	num_fresh = sum(map(len, merged_ranges))
	print("Part 2: {}".format(num_fresh))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
