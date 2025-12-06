import functools
import io
import itertools
import more_itertools
import operator
import os
import re
import sys

def part1(filename):
	print("Part 1: {}".format(sum(functools.reduce(operator.add if op_nums_strs[-1] == "+" else operator.mul, map(int, op_nums_strs[:-1])) for op_nums_strs in list(zip(*(re.findall(r"\S+", line) for line in io.open(filename, mode = 'r') if line))))))

def part2(filename):
	print("Part 2: {}".format(sum(functools.reduce(operator.add if op_nums_strs[0][-1] == "+" else operator.mul, [int(num_str[:-1]) for num_str in op_nums_strs]) for op_nums_strs in filter(len, more_itertools.split_at(map("".join, zip(*io.open(filename, mode = 'r'))), str.isspace)))))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
