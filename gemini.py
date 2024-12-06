import os, time

_terminal_prepared = False
def prepare_terminal():
	global _terminal_prepared
	if _terminal_prepared: return
	_terminal_prepared = True

	print('\n' * os.get_terminal_size().lines)

_last_called = time.time()
def sleep_at_fps(fps: float):
	global _last_called
	elapsed = time.time() - _last_called
	if elapsed >= 1 / fps:
		_last_called = time.time()
		return
	time.sleep(1 / fps - elapsed)
	_last_called = time.time()

class Vector2:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return f"({self.x}, {self.y})"

	def __eq__(self, value: object) -> bool:
		return self.x == value.x and self.y == value.y

	def __add__(self, value):
		return Vector2(self.x + value.x, self.y + value.y)

	def __sub__(self, value):
		return Vector2(self.x - value.x, self.y - value.y)

	def copy(self):
		return Vector2(self.x, self.y)

class Rect:
	@property
	def bottom_right(self):
		return self.top_left + self.size #- Vector2(1,1)

	def __init__(self, top_left: Vector2, size: Vector2):
		self.top_left = top_left
		self.size = size

	def intersects(self, other) -> bool:
		return not (self.top_left.x >= other.bottom_right.x or
                     other.top_left.x >= self.bottom_right.x or
                     self.top_left.y >= other.bottom_right.y or
                     other.top_left.y >= self.bottom_right.y)

	def is_inside(self, other) -> bool:
		return (self.top_left.x >= other.top_left.x
				and other.bottom_right.x >= self.bottom_right.x
				and self.top_left.y >= other.top_left.y
				and other.bottom_right.y >= self.bottom_right.y)

class Colour:
	END = '\x1b[0m'

	def __init__(self, r: int, g: int, b: int):
		self.r = r
		self.g = g
		self.b = b

	def to_str(self):
		return f'\x1b[38;2;{int(self.r)};{int(self.g)};{int(self.b)}m'

class GameObject:
	@property
	def size(self) -> Vector2:
		""" Get the size of the object, generated automatically based on the texture"""
		lines = self.texture.splitlines()
		return Vector2(max(map(lambda s: len(s), lines)), len(lines))

	@property
	def bounds(self) -> Rect:
		"""The smallest rectangle that the `GameObject` could fit in. Use for collisions!"""
		return Rect(self.pos, self.size)

	def __init__(self, pos: Vector2, texture: str, colour: Colour = None):
		self.pos = pos
		self.texture = texture
		self.colour = colour

	def draws_on_pos(self, pos: Vector2) -> bool:
		lines = self.texture.splitlines()
		if pos.y < self.pos.y or pos.y > self.pos.y + len(lines):
			return False

		line = lines[pos.y - self.pos.y]
		if pos.x < self.pos.x or pos.x > self.pos.x + len(line):
			return False

		return line[pos.x - self.pos.x] != ' '

class Screen:
	@property
	def bounds(self) -> Rect:
		return Rect(Vector2(0,0), self.size)

	def __init__(self, size: Vector2, bg_char: str, bg_colour: Colour = None):
		self.size = size
		self.bg_char = bg_char
		self.bg_colour = bg_colour
		self.clear()

	def clear(self):
		"""Clear the entire screen with the set bg char and colour"""
		if self.bg_colour is not None:
			self._pixels = [f"{self.bg_colour.to_str()}{self.bg_char}{Colour.END}" for _ in range(self.size.x * self.size.y)]
		else:
			self._pixels = [self.bg_char for _ in range(self.size.x * self.size.y)]

	def plot(self, pos: Vector2, char: str, colour: Colour = None, *, error_outside_bounds = True):
		"""Plot a single pixel to the screen at the given position"""
		if pos.x < 0 or pos.y < 0 or pos.x >= self.size.x or pos.y >= self.size.y:
			if error_outside_bounds:
				raise Exception(f"Plotted position {pos} is outside screen")
			else:
				return
		if len(char) != 1:
			raise Exception(f"Char parameter should be a single character, got string length {len(char)}")

		to_plot = char
		if colour is not None:
			to_plot = colour.to_str() + char + Colour.END

		self._pixels[pos.y * self.size.x + pos.x] = to_plot

	def draw(self, object: GameObject, *, error_outside_bounds = True):
		for offset_y, line in enumerate(object.texture.splitlines()):
			y = object.pos.y + offset_y

			for offset_x, c in enumerate(line):
				x = object.pos.x + offset_x
				self.plot(Vector2(x, y), c, object.colour, error_outside_bounds=error_outside_bounds)

	def display(self):
		prepare_terminal()
		render = ""
		render += "\x1b[H\x1b[J"
		for	y in range(self.size.y):
			begin = self.size.x * y
			end = self.size.x * (y + 1)
			render += ''.join(self._pixels[begin:end]) + '\n'

		print(render, end='')
