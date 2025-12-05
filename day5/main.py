import functools
import io
import itertools
import more_itertools
import os
import re
import sys

def part1(filename):
	with io.open(filename, mode = 'r') as file:
		fresh_ranges_str, ingredients_str = file.read().strip().split("\n\n")
	fresh_ranges = [range(int(lower), int(upper) + 1) for lower, upper in re.findall(r"(\d+)-(\d+)", fresh_ranges_str)]
	num_fresh = len(list(filter(lambda ingredient: any(ingredient in fresh_range for fresh_range in fresh_ranges), map(int, re.findall(r"(\d+)", ingredients_str)))))
	print("Part 1: {}".format(num_fresh))

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
