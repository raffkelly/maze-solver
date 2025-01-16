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
        self._animate()
    
    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
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
    
    def _solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        if i > 0 and self._cells[i - 1][j].visited == False and self._cells[i][j].has_left_wall == False:
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self._solve_r(i-1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i-1][j], True)
        if i < (self._num_cols - 1) and self._cells[i + 1][j].visited == False and self._cells[i][j].has_right_wall == False:
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if self._solve_r(i+1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i+1][j], True)            
        if j > 0 and self._cells[i][j - 1].visited == False and self._cells[i][j].has_top_wall == False:
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if self._solve_r(i, j-1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j-1], True)            
        if j < (self._num_rows - 1) and self._cells[i][j + 1].visited == False and self._cells[i][j].has_bottom_wall == False:
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if self._solve_r(i, j+1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j+1], True)
        return False