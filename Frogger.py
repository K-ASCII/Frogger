# Example project made with gemini-py v2 (i'm really proud of this actually)


from gemini import *
from input import get_key_press
from time import sleep
from random import randint


WIDTH = 40
HEIGHT = 20
screen = Screen(Vector2(WIDTH, HEIGHT), " ")


class Car(GameObject):
	def __init__(self, pos: Vector2, direction: int):
		r = randint(0,255)
		g = randint(0,255)
		b = randint(0,255)
		super().__init__(pos, ":=:", Colour(r,g,b))
		self.direction = direction

	def tick(self):
		self.pos.x += self.direction
		if not self.bounds.intersects(screen.bounds):
			del self
	

player = GameObject(Vector2(20, 19), "X", Colour(0, 255, 0))
car = Car(Vector2(0,10), 1)


while True:
	input = get_key_press() # Returns the pressed key as a single lowercase character


	match input: # Player movement
		case 'w':
			player.pos.y -= 1
		case 'a':
			player.pos.x -= 1
		case 's':
			player.pos.y += 1
		case 'd':
			player.pos.x += 1


	car.tick() # Player is passed because they might collide


	screen.clear()

	screen.draw(player)
	screen.draw(car)


	screen.display()


	sleep(1/30) # Run at 30 FPS


