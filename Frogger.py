from gemini import *
from input import get_key_press
from time import sleep
from random import randint, choice

WIDTH = 41
HEIGHT = 20
screen = Screen(Vector2(WIDTH, HEIGHT), " ")

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

#spawn frog
player = GameObject(Vector2(20, 19), "X", Colour(0, 255, 0))
bushes = GameObject(Vector2(0,0), BACKGROUND, Colour(50, 200, 50))
vehicles = []
logs = []
lives = 5

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

	screen.display()

	sleep_at_fps(20)

print("\rGAME OVER")