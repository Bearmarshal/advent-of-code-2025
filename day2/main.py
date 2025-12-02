import functools
import io
import itertools
import os
import re
import sys

def part1(filename):
	print("Part 1: {}".format(sum(filter(lambda product_id: re.fullmatch(r"(\d+)\1", str(product_id)) != None, itertools.chain(*(range(int(first), int(last) + 1) for first, last in re.findall(r"(\d+)-(\d+)", io.open(filename, mode = 'r').read())))))))

def part2(filename):
	print("Part 2: {}".format(sum(filter(lambda product_id: re.fullmatch(r"(\d+)\1+", str(product_id)) != None, itertools.chain(*(range(int(first), int(last) + 1) for first, last in re.findall(r"(\d+)-(\d+)", io.open(filename, mode = 'r').read())))))))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
