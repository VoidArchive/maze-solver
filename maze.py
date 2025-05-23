from cell import Cell
import time
import random
from collections import deque 
import heapq 


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []
        if seed:
            random.seed(seed)
        else:
            random.seed(time.time())

        self.__create_cell()
        self.__break_entrance_and_exit()
        self._break_walls_iterative(0, 0)
        self.__reset_cell_visited()

    def __create_cell(self):
        for i in range(self.__num_cols):
            col_cells = []
            for j in range(self.__num_rows):
                col_cells.append(Cell(self.__win))
            self.__cells.append(col_cells)

        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i, j)

    def __draw_cell(self, i, j, animate=True):
        if self.__win is None:
            return
        x1 = self.__x1 + i * self.__cell_size_x
        y1 = self.__y1 + j * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        self.__cells[i][j].draw(x1, y1, x2, y2)
        if animate:
            self.__animate()

    def __animate(self):
        if self.__win is None:
            return
        self.__win.redraw()
        time.sleep(0.01)

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__cells[self.__num_cols - 1][self.__num_rows - 1].has_bottom_wall = False
        if self.__win is None:
            return
        self.__draw_cell(0, 0)
        self.__draw_cell(self.__num_cols - 1, self.__num_rows - 1)

    def _break_walls_iterative(self, start_i, start_j):
        stack = [] 
        self.__cells[start_i][start_j].visited = True
        stack.append((start_i, start_j))
        self.__animate() 

        while stack:
            curr_i, curr_j = stack[-1] 

            next_index_list = []
            if curr_i > 0 and not self.__cells[curr_i - 1][curr_j].visited: 
                next_index_list.append((curr_i - 1, curr_j))
            if curr_i < self.__num_cols - 1 and not self.__cells[curr_i + 1][curr_j].visited: 
                next_index_list.append((curr_i + 1, curr_j))
            if curr_j > 0 and not self.__cells[curr_i][curr_j - 1].visited: 
                next_index_list.append((curr_i, curr_j - 1))
            if curr_j < self.__num_rows - 1 and not self.__cells[curr_i][curr_j + 1].visited: 
                next_index_list.append((curr_i, curr_j + 1))

            if not next_index_list: 
                self.__draw_cell(curr_i, curr_j) 
                stack.pop()
                continue

            next_i, next_j = random.choice(next_index_list)

            if next_i == curr_i + 1: 
                self.__cells[curr_i][curr_j].has_right_wall = False
                self.__cells[next_i][curr_j].has_left_wall = False
            elif next_i == curr_i - 1: 
                self.__cells[curr_i][curr_j].has_left_wall = False
                self.__cells[next_i][curr_j].has_right_wall = False
            elif next_j == curr_j + 1: 
                self.__cells[curr_i][curr_j].has_bottom_wall = False
                self.__cells[next_i][curr_j + 1].has_top_wall = False 
            elif next_j == curr_j - 1: 
                self.__cells[curr_i][curr_j].has_top_wall = False
                self.__cells[next_i][curr_j - 1].has_bottom_wall = False 

            self.__draw_cell(curr_i, curr_j) 
            self.__cells[next_i][next_j].visited = True
            self.__draw_cell(next_i, next_j) 
            stack.append((next_i, next_j))
            self.__animate() 

    def __reset_cell_visited(self):
        for col in self.__cells:
            for cell in col:
                cell.visited = False

    def regenerate(self, seed=None, num_rows=None, num_cols=None, cell_size_x=None, cell_size_y=None):
        if self.__win is not None:
            self.__win.clear_canvas()
        
        if num_rows is not None:
            self.__num_rows = num_rows
        if num_cols is not None:
            self.__num_cols = num_cols
        if cell_size_x is not None:
            self.__cell_size_x = cell_size_x
        if cell_size_y is not None:
            self.__cell_size_y = cell_size_y
            
        if seed is not None:
            random.seed(seed)
        else:
            random.seed(time.time())

        self.__cells = []
        self.__create_cell()
        self.__break_entrance_and_exit()
        self._break_walls_iterative(0, 0)
        self.__reset_cell_visited()
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i, j, animate=False)
        if self.__win is not None:
            self.__win.redraw()

    def _solve_dfs_iterative(self):
        stack = [] 
        start_node = (0,0)
        end_node = (self.__num_cols - 1, self.__num_rows - 1)
        stack.append((start_node, [])) 
        visited_dfs = set()
        visited_dfs.add(start_node)

        while stack:
            (curr_i, curr_j), path = stack.pop()

            self.__cells[curr_i][curr_j].visited = True 
            if path: 
                (prev_cell_coords, current_cell_coords) = path[-1]
                self.__cells[prev_cell_coords[0]][prev_cell_coords[1]].draw_move(self.__cells[current_cell_coords[0]][current_cell_coords[1]])
                self.__animate()

            if (curr_i, curr_j) == end_node:
                if self.__win is not None:
                    self.__win.clear_canvas()
                    for r_i in range(self.__num_cols):
                        for r_j in range(self.__num_rows):
                            self.__draw_cell(r_i,r_j, animate=False)
                    self.__win.redraw()
                
                
                for path_segment in path:
                    (prev_i, prev_j), (next_i, next_j) = path_segment
                    self.__cells[prev_i][prev_j].draw_move(self.__cells[next_i][next_j])
                    self.__animate()
                return True 

            potential_moves = []
            if curr_i < self.__num_cols - 1 and not self.__cells[curr_i][curr_j].has_right_wall:
                potential_moves.append((curr_i + 1, curr_j))
            if curr_j < self.__num_rows - 1 and not self.__cells[curr_i][curr_j].has_bottom_wall:
                potential_moves.append((curr_i, curr_j + 1))
            if curr_i > 0 and not self.__cells[curr_i][curr_j].has_left_wall:
                potential_moves.append((curr_i - 1, curr_j))
            if curr_j > 0 and not self.__cells[curr_i][curr_j].has_top_wall:
                potential_moves.append((curr_i, curr_j - 1))
            
            found_next_step = False
            for next_i, next_j in reversed(potential_moves): 
                if (next_i, next_j) not in visited_dfs:
                    visited_dfs.add((next_i, next_j))
                    new_path_segment = ((curr_i, curr_j), (next_i, next_j))
                    stack.append(((next_i, next_j), path + [new_path_segment]))
                    found_next_step = True 
            
            if not found_next_step and path: 
                (prev_cell_coords, current_cell_coords) = path[-1]
                self.__cells[prev_cell_coords[0]][prev_cell_coords[1]].draw_move(self.__cells[current_cell_coords[0]][current_cell_coords[1]], True)
                self.__animate()

        return False

    def _solve_bfs(self):
        q = deque()
        q.append(((0,0), [])) 
        visited_bfs = set()
        visited_bfs.add((0,0))
        parent_map = {} 

        start_node = (0,0)
        end_node = (self.__num_cols - 1, self.__num_rows - 1)

        while q:
            (curr_i, curr_j), path = q.popleft()
            
            if (curr_i, curr_j) != start_node:
                prev_i, prev_j = parent_map[(curr_i, curr_j)]
                self.__cells[prev_i][prev_j].draw_move(self.__cells[curr_i][curr_j])
                self.__animate() 

            if (curr_i, curr_j) == end_node:
                
                solution_path = []
                temp_i, temp_j = end_node
                while (temp_i, temp_j) != start_node:
                    solution_path.append((temp_i, temp_j))
                    prev_i, prev_j = parent_map[(temp_i, temp_j)]
                    temp_i, temp_j = prev_i, prev_j
                solution_path.append(start_node)
                solution_path.reverse()

                
                if self.__win is not None:
                    self.__win.clear_canvas()
                    for r_i in range(self.__num_cols):
                        for r_j in range(self.__num_rows):
                            self.__draw_cell(r_i,r_j, animate=False)
                    self.__win.redraw()
                
                
                for k in range(len(solution_path) - 1):
                    p1_i, p1_j = solution_path[k]
                    p2_i, p2_j = solution_path[k+1]
                    self.__cells[p1_i][p1_j].draw_move(self.__cells[p2_i][p2_j])
                    self.__animate()
                return True

            
            possible_moves = []
            
            if curr_i > 0 and not self.__cells[curr_i][curr_j].has_left_wall:
                possible_moves.append((curr_i - 1, curr_j))
            
            if curr_i < self.__num_cols - 1 and not self.__cells[curr_i][curr_j].has_right_wall:
                possible_moves.append((curr_i + 1, curr_j))
            
            if curr_j > 0 and not self.__cells[curr_i][curr_j].has_top_wall:
                possible_moves.append((curr_i, curr_j - 1))
            
            if curr_j < self.__num_rows - 1 and not self.__cells[curr_i][curr_j].has_bottom_wall:
                possible_moves.append((curr_i, curr_j + 1))

            for next_i, next_j in possible_moves:
                if (next_i, next_j) not in visited_bfs:
                    visited_bfs.add((next_i, next_j))
                    parent_map[(next_i, next_j)] = (curr_i, curr_j)
                    new_path = list(path)
                    new_path.append((next_i, next_j))
                    q.append(((next_i, next_j), new_path))
                    
        
        return False 

    def _heuristic(self, p1_coords, p2_coords):
        
        return abs(p1_coords[0] - p2_coords[0]) + abs(p1_coords[1] - p2_coords[1])

    def _solve_astar(self):
        start_node = (0, 0)
        end_node = (self.__num_cols - 1, self.__num_rows - 1)

        open_set = []  
        heapq.heappush(open_set, (0, start_node)) 
        
        came_from = {} 

        g_score = { (i,j): float('inf') for i in range(self.__num_cols) for j in range(self.__num_rows) }
        g_score[start_node] = 0

        f_score = { (i,j): float('inf') for i in range(self.__num_cols) for j in range(self.__num_rows) }
        f_score[start_node] = self._heuristic(start_node, end_node)

        open_set_hash = {start_node} 

        while open_set:
            _, current_coords = heapq.heappop(open_set)
            open_set_hash.remove(current_coords)

            curr_i, curr_j = current_coords

            
            if current_coords != start_node:
                prev_i, prev_j = came_from[current_coords]
                self.__cells[prev_i][prev_j].draw_move(self.__cells[curr_i][curr_j])
                self.__animate()

            if current_coords == end_node:
                
                solution_path = []
                temp_coords = end_node
                while temp_coords in came_from:
                    solution_path.append(temp_coords)
                    temp_coords = came_from[temp_coords]
                solution_path.append(start_node)
                solution_path.reverse()

                if self.__win is not None:
                    self.__win.clear_canvas()
                    for r_i in range(self.__num_cols):
                        for r_j in range(self.__num_rows):
                            self.__draw_cell(r_i,r_j, animate=False)
                    self.__win.redraw()
                
                for k in range(len(solution_path) - 1):
                    p1_i, p1_j = solution_path[k]
                    p2_i, p2_j = solution_path[k+1]
                    self.__cells[p1_i][p1_j].draw_move(self.__cells[p2_i][p2_j])
                    self.__animate()
                return True

            
            possible_next_nodes = []
            
            if curr_i > 0 and not self.__cells[curr_i][curr_j].has_left_wall:
                possible_next_nodes.append((curr_i - 1, curr_j))
            
            if curr_i < self.__num_cols - 1 and not self.__cells[curr_i][curr_j].has_right_wall:
                possible_next_nodes.append((curr_i + 1, curr_j))
            
            if curr_j > 0 and not self.__cells[curr_i][curr_j].has_top_wall:
                possible_next_nodes.append((curr_i, curr_j - 1))
            
            if curr_j < self.__num_rows - 1 and not self.__cells[curr_i][curr_j].has_bottom_wall:
                possible_next_nodes.append((curr_i, curr_j + 1))

            for neighbor_coords in possible_next_nodes:
                tentative_g_score = g_score[current_coords] + 1 

                if tentative_g_score < g_score[neighbor_coords]:
                    came_from[neighbor_coords] = current_coords
                    g_score[neighbor_coords] = tentative_g_score
                    f_score[neighbor_coords] = tentative_g_score + self._heuristic(neighbor_coords, end_node)
                    if neighbor_coords not in open_set_hash:
                        heapq.heappush(open_set, (f_score[neighbor_coords], neighbor_coords))
                        open_set_hash.add(neighbor_coords)
        
        return False 

    def solve(self, algorithm="dfs"):
        self.__reset_cell_visited()
        if self.__win is not None:
            self.__win.clear_canvas()
            for i in range(self.__num_cols):
                for j in range(self.__num_rows):
                    self.__draw_cell(i,j, animate=False)
            self.__win.redraw()

        if algorithm == "dfs":
            return self._solve_dfs_iterative()
        elif algorithm == "bfs":
            return self._solve_bfs()
        elif algorithm == "astar":
            return self._solve_astar()
        else:
            print(f"Unknown algorithm: {algorithm}")
            return False
