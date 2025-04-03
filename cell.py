from graphics import Line, Point


class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        if self.has_left_wall:
            self._win.draw_line(Line(Point(x1, y1), Point(x1, y2)))
        if self.has_top_wall:
            self._win.draw_line(Line(Point(x1, y1), Point(x2, y1)))
        if self.has_right_wall:
            self._win.draw_line(Line(Point(x2, y1), Point(x2, y2)))
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(x1, y2), Point(x2, y2)))

    def draw_move(self, to_cell, undo=False):
        fill_color = "gray" if undo else "red"
        self_center = Point(
            self._x1 + abs(self._x2 - self._x1) // 2,
            self._y1 + abs(self._y2 - self._y1) // 2,
        )
        to_cell_center = Point(
            to_cell._x1 + abs(to_cell._x2 - to_cell._x1) // 2,
            to_cell._y1 + abs(to_cell._y2 - to_cell._y1) // 2,
        )

        line = Line(self_center, to_cell_center)
        self._win.draw_line(line, fill_color)
