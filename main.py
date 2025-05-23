from graphics import Window
from maze import Maze
import time # Import time for the new_maze_seed


def main():
    num_rows = 12
    num_cols = 16
    margin = 50
    screen_x = 800
    screen_y = 600 # Adjusted to make space for buttons
    cell_size_x = (screen_x - 2 * margin) // num_cols
    cell_size_y = (screen_y - 2 * margin - 50) // num_rows # Adjust for button bar height

    win = Window(screen_x, screen_y)
    # Pass a seed to ensure the initial maze is the same, or omit for random
    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)

    def handle_new_maze():
        # Using time.time() as a seed for randomness
        maze.regenerate(seed=time.time())

    def handle_solve_maze():
        is_solvable = maze.solve()
        if not is_solvable:
            print("Maze is not solvable")
        else:
            print("Maze is solvable")

    win.add_button("New Maze", handle_new_maze)
    win.add_button("Solve Maze", handle_solve_maze)

    win.wait_for_close()


main()
