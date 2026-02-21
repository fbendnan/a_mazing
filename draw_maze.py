import curses

width = 10
height = 15
def main(stdscr):
    stdscr.clear()
    y = 8
    x = 15
    while True:
        stdscr.clear()
        
        max_y, max_x = stdscr.getmaxyx()
        y = max(0, min(y, max_y - 2))
        x = max(0, min(x, max_x - 2))
        stdscr.addstr(y, x, "P")
        stdscr.refresh()
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_UP:
            y -=1
        elif key == curses.KEY_DOWN:
            y +=1
        elif key == curses.KEY_LEFT:
            x -=1
        elif key == curses.KEY_RIGHT:
            x +=1


curses.wrapper(main)
