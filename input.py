import os

if os.name == "nt":
	_ARROW_KEYS = {
		"h": "up",
		"p": "down",
		"m": "right",
		"k": "left",
	}
else:
	_ARROW_KEYS = {
		"a": "up",
		"b": "down",
		"c": "right",
		"d": "left",
	}

def string_key(c: str | None) -> str | None:
	if c is None:
		return None
	if os.name == "nt":
		c = repr(c)[2:-1].lower()
		if c == "\\x03":
			raise KeyboardInterrupt
		if c == "\\xe0":
			return f"{_ARROW_KEYS[get_key_press()]}_arrow"
		return c
	else:
		if c == "\x1b":
			get_key_press() # skip [
			return f"{_ARROW_KEYS[get_key_press()]}_arrow"
		return c.lower()

def get_key_press(wait = False) -> str | None:
	if os.name == "nt":
		from msvcrt import getch, kbhit
		if wait or kbhit():
			return string_key(getch())
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
			if wait:
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
