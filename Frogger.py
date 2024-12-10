from gemini import *
from input import get_key_press
from time import sleep
from random import randint, choice

WIDTH = 41
HEIGHT = 20
screen = Screen(Vector2(WIDTH, HEIGHT), " ")

class Car(GameObject):
	def __init__(self, pos: Vector2, direction: int):
		r = randint(0,255)
		g = randint(0,255)
		b = randint(0,255)
		texture = choice([":=:", ":==:"])

		super().__init__(pos, texture, Colour(r,g,b))
		self.direction = direction

	# Return true if the car has left the screen
	def tick(self) -> bool:
		self.pos.x += self.direction
		if not self.bounds.intersects(screen.bounds):
			return True

# Log inherits from car, meaning that we don't need to write the `tick()` method
class Log(Car):
	def __init__(self, pos: Vector2, direction: int):
		super().__init__(pos, direction)
		self.texture = "===="
		# Set the colour to a variant of brown
		self.colour = Colour(60, 40, 20)
		self.colour.r += randint(-20, 20)
		self.colour.g += randint(-20, 20)
		self.colour.b += randint(-20, 20)

"""
Start screen
"""

START_BACKGROUND = """
╔═══════════════════════════════════════╗
╝                                       ╚

╗                                       ╔
║                                       ║
║                                       ║
║                                       ║
║                                       ║
║                                       ║
║                                       ║
║                                       ║
║                                       ║
║                                       ║
╝                                       ╚

╗                                       ╔
╚═══════════════════════════════════════╝
"""

start_screen = GameObject(Vector2(0,0), START_BACKGROUND, Colour(50, 200, 50))
start_cars = []

def process_start_cars(frame: int):
	if frame % 10 == 0:
		start_cars.append(Car(Vector2(-3, 3), 1))
		start_cars[-1].texture = ":=:"
		start_cars.append(Car(Vector2(WIDTH, 15), -1))
		start_cars[-1].texture = ":=:"
	if frame % 2 == 0:
		i = -1
		while i + 1 < len(start_cars):
			i += 1
			if start_cars[i].tick():
				start_cars.pop(i)
				i -= 1

for i in range(WIDTH * 2):
	process_start_cars(i)

t = 0
while get_key_press() != 'e':
	t += 1

	process_start_cars(t)

	screen.clear()

	screen.draw(start_screen)
	screen.draw(GameObject(Vector2(16,8),"FROGGER", Colour(0,225,0)))
	screen.draw(GameObject(Vector2(19,9),"X", Colour(0,225,0)))
	screen.draw(GameObject(Vector2(12,10),"PRESS E TO START"))
	for car in start_cars:
		screen.draw(car, error_outside_bounds=False)

	screen.display()

	sleep_at_fps(20)

"""
Main Game
"""

BACKGROUND = """
     ╔═╗    ╔═╗    ╔═╗    ╔═╗    ╔═╗
═════╝ ╚════╝ ╚════╝ ╚════╝ ╚════╝ ╚═════



══════════╗      ╔═════╗      ╔══════════
══════════╝      ╚═════╝      ╚══════════




╗      ╔═════════════════════════╗      ╔
╝      ╚═════════════════════════╝      ╚


╗                                       ╔
║                                       ║
╚═════════════════╗   ╔═════════════════╝
                  ║   ║
"""

#spawn frog
player = GameObject(Vector2(20, 19), "X", Colour(0, 255, 0))
bushes = GameObject(Vector2(0,0), BACKGROUND, Colour(50, 200, 50))
vehicles = []
logs = []
winPos = []
lives = 5

# processing of cars/vans
def process_cars(frame: int):
	spawn_locations = [
		( 8, -2),
		( 9,  2),
		(10, -1),
		(11,  1),
		(14,  1),
		(15, -1),
	]

	for spawn_location in spawn_locations:
		if frame % (25 / abs(spawn_location[1])) == 0:
			if randint(0, 10) < 9:
				x = -3 if spawn_location[1] > 0 else WIDTH
				vehicles.append(Car(Vector2(x, spawn_location[0]), spawn_location[1]))

	# Move existing cars
	if frame % 3 == 0:
		i = -1
		while i + 1 < len(vehicles):
			i += 1
			if vehicles[i].tick():
				vehicles.pop(i)
				i -= 1

# processing of logs
def process_logs(frame: int):
	spawn_locations = [
		( 3, 1),
		( 4, -1),
		( 5, 1),
	]

	for spawn_location in spawn_locations:
		if frame % (25 / abs(spawn_location[1])) == 0:
			if randint(0, 10) < 6:
				x = -4 if spawn_location[1] > 0 else WIDTH
				logs.append(Log(Vector2(x, spawn_location[0]), spawn_location[1]))

	# Move existing logs
	if frame % 4 == 0:
		i = -1
		while i + 1 < len(logs):
			i += 1
			if logs[i].tick():
				logs.pop(i)
				i -= 1

for i in range(WIDTH * 3):
	process_cars(i)
	process_logs(i)

t = 0
alive = True
while alive:
	t += 1

	process_cars(t)
	process_logs(t)

	while input := get_key_press():
		old_pos = player.pos.copy()
		match input: # Player movement
			case 'w':
				player.pos.y -= 1
			case 'a':
				player.pos.x -= 1
			case 's':
				player.pos.y += 1
			case 'd':
				player.pos.x += 1
		if not player.bounds.is_inside(screen.bounds) or bushes.draws_on_pos(player.pos):
			player.pos = old_pos

	# win conditions
	if player.pos.y == 2:
		if player.pos not in winPos:
			winPos.append (player.pos.copy())
			if len(winPos) == 5:
				alive = False
			else:
				player.pos = Vector2(20,19)
		else:
			player.pos.y += 1

	# DEATH TO THE FROG
	for vehicle in vehicles:
		if player.bounds.intersects(vehicle.bounds):
			player.pos = Vector2(20,19)
			lives -= 1
			if lives <= 0:
				alive = False
	if player.pos.y in [3, 4, 5]:
		on_log = False
		for log in logs:
			if player.bounds.intersects(log.bounds):
				on_log = True
				break

		if not on_log:
			player.pos = Vector2(20,19)
			lives -= 1
			if lives <= 0:
				alive = False

	screen.clear()

	screen.draw(bushes)

	for log in logs:
		screen.draw(log, error_outside_bounds=False)
	screen.draw(player)
	for car in vehicles:
		screen.draw(car, error_outside_bounds=False)

	screen.draw(GameObject(Vector2(0,0), f"Lives: {lives}"))

	for pos in winPos:
		screen.draw(GameObject(pos, "X", Colour(0,200,0)))

	screen.display()

	sleep_at_fps(20)


if lives > 0:
	print("\rYOU WIN")
else:
	print("\rGAME OVER")
