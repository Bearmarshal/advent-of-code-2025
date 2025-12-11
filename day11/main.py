import collections
import functools
import io
import itertools
import more_itertools
import operator
import os
import re
import sys

def count_paths(device, devices, known):
	if device in known:
		return known[device]
	count = sum(count_paths(output, devices, known) for output in devices.get(device, []))
	known[device] = count
	return count

def part1(filename):
	with io.open(filename, mode = 'r') as file:
		devices = {device.strip(): re.findall(r"(\w+)", outputs) for device, outputs in (line.split(":") for line in file if line)}
	known = {"out": 1}
	print("Part 1: {}".format(count_paths("you", devices, known)))

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		devices = {device.strip(): re.findall(r"(\w+)", outputs) for device, outputs in (line.split(":") for line in file if line)}
	svr_dac = count_paths("svr", devices, {"dac": 1})
	svr_fft = count_paths("svr", devices, {"fft": 1})
	dac_fft = count_paths("dac", devices, {"fft": 1})
	fft_dac = count_paths("fft", devices, {"dac": 1})
	fft_out = count_paths("fft", devices, {"out": 1})
	dac_out = count_paths("dac", devices, {"out": 1})
	print("Part 2: {}".format(svr_dac * dac_fft * fft_out + svr_fft * fft_dac * dac_out))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
