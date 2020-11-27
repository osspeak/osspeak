import threading
import time

import screengrid

def foo():
    main_grid = screengrid.Grid()
    main_grid.overlay(click=True)
    time.sleep(5)
    main_grid.font_color = 100, 100, 100

def main():
    threading.Thread(target=foo, daemon=True).start()
    input()

if __name__ == '__main__':
    main()