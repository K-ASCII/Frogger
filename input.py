import os

def string_key(c: str | None) -> str:
	if os.name == "nt":
		c = repr(c)[2:-1].lower()
		if c == "\\x03":
			raise KeyboardInterrupt
	else:
		return c.lower() if c else None

def get_key_press(is_wait = False) -> str:
	if os.name == "nt":
		from msvcrt import getch
		if is_wait:
			while True:
				if c := getch():
					return string_key(c)
		else:
			c = getch()
			return string_key(c)
	else:
		import termios, fcntl, contextlib, sys
		fd = sys.stdin.fileno()

		oldterm = termios.tcgetattr(fd)
		newattr = termios.tcgetattr(fd)
		newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
		termios.tcsetattr(fd, termios.TCSANOW, newattr)

		oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

		try:
			if is_wait:
				while True:
					with contextlib.suppress(IOError):
						if c := sys.stdin.read(1):
							return string_key(c)
			else:
				with contextlib.suppress(IOError):
					c = sys.stdin.read(1)
					return string_key(c)
		finally:
			termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
			fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
