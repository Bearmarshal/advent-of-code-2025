import functools
import io
import itertools
import more_itertools
import operator
import os
import re
import sys

def part1(filename):
	print("Part 1: {}".format("\n".join(itertools.accumulate(("." + line.strip() + "." for line in io.open(filename, mode = 'r') if line), lambda upper, lower: "." + "".join("|" if any(lw[i] == "^.^"[i] and uw[i] in "|S" for i in range(3)) else "x" if lw[1] == "^" and uw[1] in "|S" else lw[1] for (uw, lw) in zip(more_itertools.windowed(upper, 3), more_itertools.windowed(lower, 3))) + ".")).count("x")))

def part2(filename):
	print("Part 2: {}".format(sum(functools.reduce(lambda timeline_count, lower: [0] + list(sum(tw[i] for i in range(3) if lw[i] == "^.^"[i]) + (lw[1] == "S") for (tw, lw) in zip(more_itertools.windowed(timeline_count, 3), more_itertools.windowed(lower, 3))) + [0], ("." + line.strip() + "." for line in io.open(filename, mode = 'r') if line), itertools.repeat(0)))))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
