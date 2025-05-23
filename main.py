from graphics import Window
from maze import Maze
import time # Import time for the new_maze_seed

# Default maze parameters
DEFAULT_NUM_ROWS = 12
DEFAULT_NUM_COLS = 16
DEFAULT_CELL_SIZE = 30 # Simplified to one value, assuming square cells for parameter input
MARGIN = 50
SCREEN_X = 800
SCREEN_Y = 600

def main():
    # Store current maze parameters, initialized to defaults
    current_maze_params = {
        "num_rows": DEFAULT_NUM_ROWS,
        "num_cols": DEFAULT_NUM_COLS,
        "cell_size_x": DEFAULT_CELL_SIZE,
        "cell_size_y": DEFAULT_CELL_SIZE
    }

    # Initial screen and cell calculations based on defaults for Window creation
    # Note: Window size is fixed. Canvas will adapt or clip if maze too big.
    win = Window(SCREEN_X - 2 * MARGIN, 
                 SCREEN_Y - 2 * MARGIN - 70, # Adjusted for param and button bars
                 DEFAULT_NUM_ROWS, 
                 DEFAULT_NUM_COLS, 
                 DEFAULT_CELL_SIZE)

    maze = Maze(MARGIN, MARGIN, 
                  current_maze_params["num_rows"], 
                  current_maze_params["num_cols"],
                  current_maze_params["cell_size_x"], 
                  current_maze_params["cell_size_y"], 
                  win)

    def handle_new_maze():
        win.update_solve_time_label("")
        params = win.get_maze_parameters()
        
        if params:
            new_rows, new_cols, new_cell_size = params
            current_maze_params["num_rows"] = new_rows
            current_maze_params["num_cols"] = new_cols
            current_maze_params["cell_size_x"] = new_cell_size
            current_maze_params["cell_size_y"] = new_cell_size # Assuming square cells from input
            
            # Adjust canvas size in Window if needed, or re-calculate cell sizes
            # For now, we assume fixed window/canvas and rely on user to pick fitting params.
            # The maze object itself will use the new parameters for its internal logic and drawing scale.

        maze.regenerate(seed=time.time(), 
                          num_rows=current_maze_params["num_rows"],
                          num_cols=current_maze_params["num_cols"],
                          cell_size_x=current_maze_params["cell_size_x"],
                          cell_size_y=current_maze_params["cell_size_y"])

    def handle_solve_maze(algorithm="dfs"):
        algo_name = "DFS"
        if algorithm == "bfs":
            algo_name = "BFS"
        elif algorithm == "astar":
            algo_name = "A*"
        
        win.update_solve_time_label(f"Solving with {algo_name}...")
        win.redraw()

        start_time = time.perf_counter()
        is_solvable = maze.solve(algorithm=algorithm) # Pass algorithm to maze.solve
        end_time = time.perf_counter()
        solve_duration = end_time - start_time

        if not is_solvable:
            win.update_solve_time_label(f"{algo_name}: Not solvable. (Tried for {solve_duration:.3f}s)")
            print(f"Maze ({algo_name}) is not solvable")
        else:
            win.update_solve_time_label(f"{algo_name}: Solved in {solve_duration:.3f} seconds!")
            print(f"Maze ({algo_name}) is solvable")

    win.add_button("New Maze", handle_new_maze)
    win.add_button("Solve DFS", lambda: handle_solve_maze(algorithm="dfs"))
    win.add_button("Solve BFS", lambda: handle_solve_maze(algorithm="bfs"))
    win.add_button("Solve A*", lambda: handle_solve_maze(algorithm="astar"))

    win.wait_for_close()


main()
