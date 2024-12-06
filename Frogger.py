from gemini import *
from input import get_key_press
from time import sleep
from random import randint, choice

WIDTH = 40
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

	def tick(self):
		self.pos.x += self.direction
		if not self.bounds.intersects(screen.bounds):
			del self

class Log(GameObject):
	def __init__(self, pos: Vector2, direction: int):
		super().__init__(pos, "====", Colour(125,100,30))
		self.direction = direction

	def tick(self):
		self.pos.x += self.direction
		if not self.bounds.intersects(screen.bounds):
			del self


#spawn frog
player = GameObject(Vector2(20, 19), "X", Colour(0, 255, 0))
vehicles = []


t = 0

while True:
	t += 1
	input = get_key_press() # Returns the pressed key as a single lowercase character

	#spawning the cars and vans
	if t % 25 == 0:
		vehicles.append(Car(Vector2(0,10), 1))
		vehicles.append(Car(Vector2(40,15), -1))
	# " "
	if t % 30 == 0:
		if randint(0, 2) == 0:
			vehicles.append(Car(Vector2(40,8), -1))

		if randint(0, 2) == 0:
			vehicles.append(Car(Vector2(0,11), 1))
		
	

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
	if not player.bounds.is_inside(screen.bounds):
		player.pos = old_pos

	if t % 3 == 0:
		for car in vehicles:
			car.tick()
			 # Player is passed because they might collide


	# DEATH TO THE FROG
	for vehicle in vehicles:
		if player.bounds.intersects(vehicle.bounds):
			player.pos = Vector2(20,19)

	screen.clear()

	screen.draw(player)
	for car in vehicles:
		screen.draw(car, error_outside_bounds=False)

	screen.display()

	sleep_at_fps(20)
	# sleep(1/30) # Ru?n at 30 FPS
