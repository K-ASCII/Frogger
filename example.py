# Example project made with gemini-py v2 (i'm really proud of this actually)

from Frogger.gemini import *
from Frogger.input import get_key_press
from time import sleep

WIDTH = 40
HEIGHT = 20
screen = Screen(Vector2(WIDTH, HEIGHT), " ")

class Bouncer(GameObject):
	def __init__(self, pos: Vector2, colour: Colour = None):
		super().__init__(pos, "█", colour)
		self.direction = 1

	def tick(self, other_object: GameObject):
		self.pos.y += self.direction

		if self.pos.y < 0 or self.pos.y >= HEIGHT or self.bounds.intersects(other_object.bounds):
			self.direction = -self.direction
			self.pos.y += self.direction

bouncers = []
for x in range(WIDTH):
	bouncers.append(Bouncer(Vector2(x, 0), Colour(x / WIDTH * 255, 0, 0)))

player = GameObject(Vector2(10, 8), "-===-", Colour(0, 255, 0))

while True:
	input = get_key_press() # Returns the pressed key as a single lowercase character

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
	# if not player.bounds.is_inside(screen.bounds):
	# 	player.pos = old_pos

	# Move all the bouncers. You can handle obstacles in a similar way
	for bouncer in bouncers:
		bouncer.tick(player) # Player is passed because they might collide

	screen.clear()

	# Draw all the objects
	for bouncer in bouncers:
		screen.draw(bouncer) # We can pass a bouncer here because it inherits from `GameObject`
	screen.draw(player, error_outside_bounds=False)

	screen.display()

	sleep_at_fps(30) # Run at 30 FPS
