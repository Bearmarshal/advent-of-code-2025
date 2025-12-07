import collections
import functools
import io
import itertools
import more_itertools
import os
import re
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoclib.posdir import Position, Direction, CARDINAL_AND_DIAGONAL_DIRECTIONS
from aoclib.tilemap import TileMap

def part1(filename):
	with io.open(filename, mode = 'r') as file:
		storage_area = TileMap([line.strip() for line in file.readlines() if line])
	num_accessible = 0
	for tile in storage_area.find_tiles("@"):
		num_occupied = 0
		for adjacent in tile.neighbours(CARDINAL_AND_DIAGONAL_DIRECTIONS):
			num_occupied += "@" in adjacent
		num_accessible += num_occupied < 4
	print("Part 1: {}".format(num_accessible))

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		storage_area = TileMap([line.strip() for line in file.readlines() if line])
	open_set = collections.deque(storage_area.find_tiles("@"))
	removed_rolls = set()
	while open_set:
		tile = open_set.pop()
		if tile in removed_rolls:
			continue
		adjacent_rolls = [adjacent for adjacent in tile.neighbours(CARDINAL_AND_DIAGONAL_DIRECTIONS) if "@" in adjacent and adjacent not in removed_rolls]
		if len(adjacent_rolls) < 4:
			removed_rolls.add(tile)
			open_set.extend(adjacent_rolls)
	print("Part 2: {}".format(len(removed_rolls)))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
