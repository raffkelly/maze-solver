from cell import *
import time
import random


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
        seed=None
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            column = []
            for j in range(self._num_rows):
                column.append(Cell(self._win))
            self._cells.append(column)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate("maze")
    
    def _animate(self, type=None):
        if self._win is None:
            return
        self._win.redraw()
        if type == "undo":
            time.sleep(.1)
        elif type == "maze":
            time.sleep(.01)
        elif type == "solve":
            time.sleep(.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows -1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows -1)
    
    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            possible_directions = []
            if i > 0 and self._cells[i - 1][j].visited == False:
                possible_directions.append((i - 1, j, "left"))
            if i < (self._num_cols - 1) and self._cells[i + 1][j].visited == False:
                possible_directions.append((i + 1, j, "right"))
            if j > 0 and self._cells[i][j - 1].visited == False:
                possible_directions.append((i, j - 1, "up"))
            if j < (self._num_rows - 1) and self._cells[i][j + 1].visited == False:
                possible_directions.append((i, j + 1, "down"))
            if not possible_directions:
                self._draw_cell(i, j)
                return
            else:
                moving_direction = random.randrange(0, len(possible_directions))
                if possible_directions[moving_direction][2] == "left":
                    self._cells[i][j].has_left_wall = False
                    self._cells[i-1][j].has_right_wall = False
                elif possible_directions[moving_direction][2] == "right":
                    self._cells[i][j].has_right_wall = False
                    self._cells[i+1][j].has_left_wall = False
                elif possible_directions[moving_direction][2] == "down":
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[i][j+1].has_top_wall = False
                elif possible_directions[moving_direction][2] == "up":
                    self._cells[i][j].has_top_wall = False
                    self._cells[i][j-1].has_bottom_wall = False
                self._break_walls_r(possible_directions[moving_direction][0], possible_directions[moving_direction][1])
    
    def _reset_cells_visited(self):
            for i in range(self._num_cols):
                for j in range(self._num_rows):
                    self._cells[i][j].visited = False
    
    def solve_dfs(self):
        return self._solve_r_dfs(0, 0)
    
    def _solve_r_dfs(self, i, j):
        self._cells[i][j].visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        if i > 0 and self._cells[i - 1][j].visited == False and self._cells[i][j].has_left_wall == False:
            self._animate("solve")
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self._solve_r_dfs(i-1, j):
                return True
            else:
                self._animate("undo")
                self._cells[i][j].draw_move(self._cells[i-1][j], True)
        if i < (self._num_cols - 1) and self._cells[i + 1][j].visited == False and self._cells[i][j].has_right_wall == False:
            self._animate("solve")
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if self._solve_r_dfs(i+1, j):
                return True
            else:
                self._animate("undo")
                self._cells[i][j].draw_move(self._cells[i+1][j], True)            
        if j > 0 and self._cells[i][j - 1].visited == False and self._cells[i][j].has_top_wall == False:
            self._animate("solve")
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if self._solve_r_dfs(i, j-1):
                return True
            else:
                self._animate("undo")
                self._cells[i][j].draw_move(self._cells[i][j-1], True)            
        if j < (self._num_rows - 1) and self._cells[i][j + 1].visited == False and self._cells[i][j].has_bottom_wall == False:
            self._animate("solve")
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if self._solve_r_dfs(i, j+1):
                return True
            else:
                self._animate("undo")
                self._cells[i][j].draw_move(self._cells[i][j+1], True)
        return False
    
    def solve_bfs(self):
        self._solve_r_bfs(0, 0)
    
    def _solve_r_bfs(self, i, j):
        visited = []
        to_visit = []
        to_visit.append((i,j))
        path = {(i, j): None}
        while to_visit:
            current = to_visit.pop(0)
            i = current[0]
            j = current[1]
            visited.append(current)
            if current == (self._num_cols -1, self._num_rows -1):
                path_list = []
                while current is not None:
                    path_list.append(current)
                    current = path[current]
                path_list.reverse()
                break
            if i > 0 and self._cells[i][j].has_left_wall == False and (i-1, j) not in visited and (i-1, j) not in to_visit:
                to_visit.append((i-1, j))
                path[(i-1, j)] = current
            if i < (self._num_cols - 1) and self._cells[i][j].has_right_wall == False and (i+1, j) not in visited and (i+1, j) not in to_visit:
                to_visit.append((i+1, j))
                path[(i+1, j)] = current          
            if j > 0 and self._cells[i][j].has_top_wall == False and (i, j-1) not in visited and (i, j-1) not in to_visit:
                to_visit.append((i, j-1))
                path[(i, j-1)] = current          
            if j < (self._num_rows - 1) and self._cells[i][j].has_bottom_wall == False and (i, j+1) not in visited and (i, j+1) not in to_visit:
                to_visit.append((i, j+1))
                path[(i, j+1)] = current
        for i in range(len(path_list)):
            if i == len(path_list) - 1:
                return
            current_i = path_list[i][0]
            current_j = path_list[i][1]
            next_i = path_list[i+1][0]
            next_j = path_list[i+1][1]
            current_cell = self._cells[current_i][current_j]
            next_cell = self._cells[next_i][next_j]
            current_cell.draw_move(next_cell)
            self._animate("maze")