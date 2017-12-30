import os
import time

import screen
import hexgrid
import solver

newgame_p = (600, 730)
center = screen.center

def moveto(coord):
    x, y = coord
    os.system(f"xdotool mousemove {x} {y}")

def click(dur):
    os.system(f"xdotool mousedown 1")
    time.sleep(dur)
    os.system(f"xdotool mouseup 1")

def timeout(func, args=(), kwargs={}, timeout_duration=1, default=None):
    import signal

    class TimeoutError(Exception):
        pass

    def handler(signum, frame):
        raise TimeoutError()

    # set the timeout handler
    signal.signal(signal.SIGALRM, handler) 
    signal.alarm(timeout_duration)
    try:
        result = func(*args, **kwargs)
    except TimeoutError as exc:
        result = default
    finally:
        signal.alarm(0)

    return result

def main():
    while True:
        moveto(newgame_p)
        click(0.3)
        time.sleep(6)
        os.system("maim /tmp/screen.png")
        g = screen.get_grid("/tmp/screen.png")
        r = timeout(solver.solve, args=(g,), timeout_duration=20)
        if r is None:
            continue
        _, steps = r
        print("executing")
        depth = 0
        print(steps)
        while depth in steps:
            c1, c2 = steps[depth]

            c1x, c1y = hexgrid.cartesian(c1, screen.scale)
            c1x, c1y = round(c1x + center[0]), round(center[1] - c1y)
            moveto((c1x, c1y))
            time.sleep(0.1)
            click(0.2)

            time.sleep(0.1)

            c2x, c2y = hexgrid.cartesian(c2, screen.scale)
            c2x, c2y = round(c2x + center[0]), round(center[1] - c2y)
            moveto((c2x, c2y))
            time.sleep(0.1)
            click(0.2)

            depth += 1


if __name__ == "__main__":
    time.sleep(3)
    main()
