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
	print("Part 1: {}".format(sum(sum("@" in adjacent for adjacent in tile.neighbours(CARDINAL_AND_DIAGONAL_DIRECTIONS)) < 4 for tile in TileMap([line.strip() for line in io.open(filename, mode = 'r').readlines() if line]).find_tiles("@"))))

def part2(filename):
	print("Part 2: {}".format(len(list(itertools.takewhile(lambda closed_open_sets: closed_open_sets[1], itertools.accumulate(itertools.count(), lambda closed_open_sets, _: functools.reduce(lambda new_closed_open_sets, tile_adjacent_rolls: (new_closed_open_sets[0] | tile_adjacent_rolls[0], new_closed_open_sets[1] | tile_adjacent_rolls[1]), filter(lambda tile_adjacent_rolls: len(tile_adjacent_rolls[1]) < 4, (({tile}, {adjacent for adjacent in tile.neighbours(CARDINAL_AND_DIAGONAL_DIRECTIONS) if "@" in adjacent and adjacent not in closed_open_sets[0]}) for tile in closed_open_sets[1] if tile not in closed_open_sets[0])), (closed_open_sets[0], set())), initial=(set(), set(TileMap([line.strip() for line in io.open(filename, mode = 'r').readlines() if line]).find_tiles("@"))))))[-1][0])))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
