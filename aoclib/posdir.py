import enum

class EnumContainsValueMeta(enum.EnumMeta):
	def __contains__(cls, value):
		return value in cls.__members__.values()

class Direction(tuple):
	def __new__(cls, dy, dx):
		self = tuple.__new__(cls, (dy, dx))
		self.dy = dy
		self.dx = dx
		return self

	def __neg__(self):
		return Direction(-self.dy, -self.dx)

	def __add__(self, other):
		return Direction(self.dy + other.dy, self.dx + other.dx)
	
	def __sub__(self, other):
		return Direction(self.dy - other.dy, self.dx - other.dx)
	
	def __mul__(self, value):
		return Direction(self.dy * value, self.dx * value)
	
	def __rmul__(self, value):
		return self.__mul__(value)
	
	def discretise(self):
		steps = []
		for _ in range(0, self.dy, dy_step := (-1 if self.dy < 0 else 1)):
			steps.append(CardinalDirection((dy_step, 0)))
		for _ in range(0, self.dx, dx_step := (-1 if self.dx < 0 else 1)):
			steps.append(CardinalDirection((0, dx_step)))
		return steps
	
class CardinalDirection(Direction, enum.Enum):
	def __new__(cls, dy, dx):
		self = Direction.__new__(cls, dy, dx)
		self._value_ = (dy, dx)
		return self

	def __neg__(self):
		return CardinalDirection((-self.dy, -self.dx))

	def opposite(self):
		return -self

	def right(self):
		return CardinalDirection((self.dx, -self.dy))

	def left(self):
		return CardinalDirection((-self.dx, self.dy))
	
	def __str__(self):
		return self.name
	
	def glyph(self):
		match self:
			case CardinalDirection.NORTH: return "^"
			case CardinalDirection.SOUTH: return "v"
			case CardinalDirection.WEST: return "<"	
			case CardinalDirection.EAST: return ">"

	@classmethod
	def from_glyph(cls, glyph):
		match glyph:
			case "^": return cls.NORTH
			case "v": return cls.SOUTH
			case "<": return cls.WEST
			case ">": return cls.EAST

	NORTH = (-1, 0)
	SOUTH = (1, 0)
	WEST = (0, -1)
	EAST = (0, 1)

NORTH = CardinalDirection.NORTH
SOUTH = CardinalDirection.SOUTH
EAST = CardinalDirection.EAST
WEST = CardinalDirection.WEST

class Position(tuple):
	def __new__(cls, y, x):
		self = tuple.__new__(cls, (y, x))
		self.y = y
		self.x = x
		return self

	def __add__(self, direction: Direction):
		return Position(self.y + direction.dy, self.x + direction.dx)
	
	def __sub__(self, other):
		if isinstance(other, Position):
			return Direction(self.y - other.y, self.x - other.x)
		elif isinstance(other, Direction):
			return self + -other
	
	def wraparound(self, y_dim, x_dim):
		if type(y_dim) is int:
			y_dim = range(y_dim)
		if type(x_dim) is int:
			x_dim = range(x_dim)
		return Position((self.y - y_dim.start) % (y_dim.stop - y_dim.start) + y_dim.start, (self.x - x_dim.start) % (x_dim.stop - x_dim.start) + x_dim.start)
	
	def __getitem__(self, map):
		return map[self.y][self.x]
	
	def __setitem__(self, map, value):
		map[self.y][self.x] = value

	def get_manhattan_distance(self, other):
		return abs(self.y - other.y) + abs(self.x - other.x)