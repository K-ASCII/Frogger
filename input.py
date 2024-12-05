import os


def string_key(c: str | None) -> str:
    c = repr(c)
    if os.name == "nt":
        slice = (2,-1)
    else:
        slice = (1,-1)

    if not c:
        return None

    c = c[slice[0]:slice[1]].lower()

    if os.name == "nt" and c == "\\x03":
        raise KeyboardInterrupt

    return c

def get_key_press(is_wait = False) -> str:
    if os.name == "nt":
        from msvcrt import getch, kbhit
        if is_wait:
            while True:
                if c := getch():
                    return string_key(c)
        else:
            if kbhit():
                c = getch()
                print(c)
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
