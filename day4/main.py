import functools
import io
import itertools
import more_itertools
import os
import re
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoclib.posdir import Position, Direction
from aoclib.tilemap import TileMap

def part1(filename):
	with io.open(filename, mode = 'r') as file:
		storage_area = TileMap([line.strip() for line in file.readlines() if line])
	num_accessible = 0
	for y in storage_area.y_dim:
		for x in storage_area.x_dim:
			if storage_area.map[y][x] == "@":
				position = Position(y, x)
				num_occupied = 0
				for dy in (-1, 0, 1):
					for dx in (-1, 0, 1):
						adjacent = position + Direction(dy, dx)
						if adjacent != position and adjacent in storage_area and storage_area[adjacent] == "@":
							num_occupied += 1
				if num_occupied < 4:
					num_accessible += 1
	print("Part 1: {}".format(num_accessible))

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		storage_area = TileMap([line.strip() for line in file.readlines() if line])
	directions = [Direction(dy, dx) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dy != 0 or dx != 0]
	open_set = {position for y in storage_area.y_dim for x in storage_area.x_dim if storage_area[position := Position(y, x)] == "@"}
	removed_rolls = set()
	while open_set:
		position = open_set.pop()
		adjacent_rolls = []
		for direction in directions:
			adjacent = position + direction
			if adjacent in storage_area and storage_area[adjacent] == "@" and adjacent not in removed_rolls:
				adjacent_rolls.append(adjacent)
		if len(adjacent_rolls) < 4:
			removed_rolls.add(position)
			open_set.update(adjacent_rolls)
	print("Part 2: {}".format(len(removed_rolls)))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
