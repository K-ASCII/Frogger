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

class Log(GameObject):
	def __init__(self, pos: Vector2, direction: int):
		super().__init__(pos, "====", Colour(125,100,30))
		self.direction = direction

	def tick(self):
		self.pos.x += self.direction
		if not self.bounds.intersects(screen.bounds):
			del self

# spawning the cars and vans
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
			if randint(0, 5) < 3:
				x = -4 if spawn_location[1] > 0 else WIDTH
				vehicles.append(Car(Vector2(x, spawn_location[0]), spawn_location[1]))

	# Move existing cars
	if frame % 3 == 0:
		i = -1
		while i + 1 < len(vehicles):
			i += 1
			print(i)
			if vehicles[i].tick():
				vehicles.pop(i)
				i -= 1


#spawn frog
player = GameObject(Vector2(20, 19), "X", Colour(0, 255, 0))
bushes = GameObject(Vector2(0,0), BACKGROUND, Colour(50, 200, 50))
vehicles = []
lives = 5

for i in range(WIDTH * 3):
	process_cars(i)

t = 0
alive = True
while alive:
	t += 1
	input = get_key_press() # Returns the pressed key as a single lowercase character

	process_cars(t)

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

	screen.clear()

	screen.draw(bushes)

	screen.draw(player)
	for car in vehicles:
		screen.draw(car, error_outside_bounds=False)

	screen.draw(GameObject(Vector2(0,0), f"Lives: {lives}"))

	screen.display()
	print(len(vehicles))

	sleep_at_fps(20)
	# sleep(1/30) # Ru?n at 30 FPS

print("GAME OVER")