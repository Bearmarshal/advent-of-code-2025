import functools
import io
import itertools
import more_itertools
import os
import re
import sys

def part1(filename):
	print("Part 1: {}".format(sum(jolts for (jolts, _) in (functools.reduce(lambda curr_max, digit: (max(curr_max[0], 10 * curr_max[1] + digit), max(curr_max[1], digit)), (int(digit) for digit in re.findall(r"(\d)", line)), (0, 0)) for line in io.open(filename, mode = 'r')))))

def part2(filename):
	print("Part 2: {}".format(sum(jolts for (jolts, _) in (functools.reduce(lambda curr_max, digit: (max(curr_max[0], int(curr_max[1] + digit)), "".join(old_curr[index] for index, old_curr_iter in enumerate(more_itertools.before_and_after(lambda old_curr: old_curr[0] >= old_curr[1], zip(curr_max[1], curr_max[1][1:] + digit))) for old_curr in old_curr_iter)), (digit for digit in re.findall(r"(\d)", line)), (0, "00000000000")) for line in io.open(filename, mode = 'r')))))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
