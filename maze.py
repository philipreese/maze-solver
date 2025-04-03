import random
import time
from cell import Cell


class Maze:
    def __init__(
        self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        self._create_cells()
        self._break_entrance_and_exit()
        if seed:
            random.seed(seed)
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = [
            [Cell(self._win) for _ in range(self._num_rows)]
            for _ in range(self._num_cols)
        ]

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + (i * self._cell_size_x)
        y1 = self._y1 + (j * self._cell_size_y)
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self, refresh=0.001):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(refresh)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []

            # determine which cell(s) to visit next
            if i > 0 and not self._cells[i - 1][j].visited:
                to_visit.append((i - 1, j))
            if j > 0 and not self._cells[i][j - 1].visited:
                to_visit.append((i, j - 1))
            if i < len(self._cells) - 1 and not self._cells[i + 1][j].visited:
                to_visit.append((i + 1, j))
            if j < len(self._cells[i]) - 1 and not self._cells[i][j + 1].visited:
                to_visit.append((i, j + 1))

            # if there is nowhere to go from here just break out
            if not to_visit:
                self._draw_cell(i, j)
                return

            # randomly choose the next direction to go
            new_x, new_y = to_visit[random.randint(0, len(to_visit) - 1)]

            # knock out walls between this cell and the next cell(s)
            if new_x < i:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            elif new_y < j:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False
            elif new_x > i:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            elif new_y > j:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False

            # recursively visit the next cell
            self._break_walls_r(new_x, new_y)

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self._solve_r()

    def _solve_r(self, i=0, j=0):
        self._animate(0.08)
        current_cell = self._cells[i][j]
        current_cell.visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        # left
        if (
            i > 0
            and not current_cell.has_left_wall
            and not self._cells[i - 1][j].visited
        ):
            current_cell.draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            self._animate(0.08)
            current_cell.draw_move(self._cells[i - 1][j], undo=True)
        # top
        if (
            j > 0
            and not current_cell.has_top_wall
            and not self._cells[i][j - 1].visited
        ):
            current_cell.draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            self._animate(0.08)
            current_cell.draw_move(self._cells[i][j - 1], undo=True)
        # right
        if (
            i < len(self._cells) - 1
            and not current_cell.has_right_wall
            and not self._cells[i + 1][j].visited
        ):
            current_cell.draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            self._animate(0.08)
            current_cell.draw_move(self._cells[i + 1][j], undo=True)
        # bottom
        if (
            j < len(self._cells[i]) - 1
            and not current_cell.has_bottom_wall
            and not self._cells[i][j + 1].visited
        ):
            current_cell.draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            self._animate(0.08)
            current_cell.draw_move(self._cells[i][j + 1], undo=True)

        return False
