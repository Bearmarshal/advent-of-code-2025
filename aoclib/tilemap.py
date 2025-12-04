import collections
from dataclasses import dataclass, field
import queue
from typing import Any, Self
from collections.abc import Callable, Sequence

from .posdir import *

@dataclass(order=True)
class AStarItem:
	cost_heuristic: int
	heuristic: int
	item: Any=field(compare=False)

class TileMap[T]:
	def __init__(self, map_items: Sequence[Sequence[T]]):
		self.map = map_items
		self.y_dim = range(len(self.map))
		self.x_dim = range(len(self.map[0]))

	def __getitem__(self, position: Position):
		if position.y not in self.y_dim or position.x not in self.x_dim:
			raise IndexError
		return self.map[position.y][position.x]

	def __setitem__(self, position: Position, value: T):
		if position.y not in self.y_dim or position.x not in self.x_dim:
			raise IndexError
		self.map[position.y][position.x] = value
	
	def __contains__(self, position: Position):
		return position.y in self.y_dim and position.x in self.x_dim
	
	def bfs[A](self,
			start: Position,
			end: Position,
			neighbours: Callable[[Self, Position], Sequence[Position]] = lambda self, position: [neighbour for direction in CardinalDirection if (neighbour := position + direction) in self],
			accumulator: Callable[[Self, Position, A], A] = lambda self, position, accumulated: accumulated + [position],
			initial_acc: Callable[[Self, Position], A] = lambda self, start: [start]) -> A | None:
		open_set = collections.deque([(start, initial_acc(self, start))])
		closed_set = {}
		while open_set:
			position, accumulated = open_set.popleft()
			if position == end:
				return accumulated
			if position in closed_set:
				continue
			closed_set[position] = accumulated
			for neighbour in neighbours(self, position):
				if neighbour not in closed_set:
					open_set.append((neighbour, accumulator(self, neighbour, accumulated)))
		return None
	
	def a_star[A](self,
			start: Position,
			end: Position,
			neighbours: Callable[[Self, Position], Sequence[Position]] = lambda self, position: [neighbour for direction in CardinalDirection if (neighbour := position + direction) in self],
			heuristic: Callable[[Self, Position, Position], int] = lambda self, position, end: position.get_manhattan_distance(end),
			cost: Callable[[Self, Position, Position], int] = lambda self, position, neighbour: 1,
			accumulator: Callable[[Self, Position, A], A] = lambda self, position, accumulated: accumulated + [position],
			initial_acc: Callable[[Self, Position], A] = lambda self, start: [start]) -> A | None:
		open_set = queue.PriorityQueue()
		cost_heuristic = heuristic(self, start, end)
		open_set.put(AStarItem(cost_heuristic, cost_heuristic, (start, 0, initial_acc(self, start))))
		closed_set = {}
		while open_set.qsize():
			prioritised_item = open_set.get()
			position, distance, accumulated = prioritised_item.item
			if position == end:
				return accumulated
			if position in closed_set:
				continue
			closed_set[position] = accumulated
			for neighbour in neighbours(self, position):
				if neighbour not in closed_set:
					new_distance = distance + cost(self, position, neighbour)
					remaining_heuristic = heuristic(self, neighbour, end)
					open_set.put(AStarItem(new_distance + remaining_heuristic, remaining_heuristic, (neighbour, new_distance, accumulator(self, neighbour, accumulated))))
		return None
	
	def find_all_shortest_paths(self,
			start: Position,
			end: Position,
			neighbours: Callable[[Self, Position], Sequence[Position]] = lambda self, position: [neighbour for direction in CardinalDirection if (neighbour := position + direction) in self]) -> list[list[Position]]:
		open_set = collections.deque([(start, [start])])
		path_length = None
		paths = []
		while open_set:
			position, accumulated = open_set.popleft()
			if path_length is not None and len(accumulated) > path_length:
				continue
			if position == end:
				path_length = len(accumulated)
				paths.append(accumulated)
				continue
			for neighbour in neighbours(self, position):
				if neighbour not in accumulated:
					open_set.append((neighbour, accumulated + [neighbour]))
		return paths
