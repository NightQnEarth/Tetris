from model.wall import Wall
from model.color import Color
from model.position import Position


class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = self._matrix_with_walls_create()
        self.scores = 0
        self.destroyed_rectangles_count = 0
        self.current_level = 1

    def _matrix_with_walls_create(self):
        matrix = [[None for _ in range(self.width)] for _ in range(
                  self.height)]
        for i in range(self.height):
            if i % 2 == 0:
                matrix[i][0] = Wall.WALL
            else:
                matrix[i][self.width - 1] = Wall.WALL

        return matrix

    def remove_completed_rectangle(self, falling_figure):
        completed_rectangle = self._search_max_area_rectangle()
        while completed_rectangle:
            for row in range(completed_rectangle[1].row,
                             completed_rectangle[2].row + 1):
                for column in range(completed_rectangle[1].column,
                                    completed_rectangle[2].column + 1):
                    self.matrix[row][column] = None

            self._move_down_after_remove_rectangle(completed_rectangle,
                                                   falling_figure)
            self.scores += round(completed_rectangle[0] * (self.current_level *
                                                           0.15 + 1))
            self.destroyed_rectangles_count += 1
            if self.destroyed_rectangles_count % 10 == 0:
                self.current_level += 1

            completed_rectangle = self._search_max_area_rectangle()

    def _move_down_after_remove_rectangle(self, removed_rectangle,
                                          falling_figure):
        falling_figure.remove_figure_from_field()
        for row in range(removed_rectangle[1].row - 1, -1, -1):
            for column in range(removed_rectangle[1].column,
                                removed_rectangle[2].column + 1):
                rectangle_height = (removed_rectangle[2].row -
                                    removed_rectangle[1].row + 1)
                if self.matrix[row][column] is not Wall.WALL:
                    self.matrix[row + rectangle_height][column] =\
                        self.matrix[row][column]
                    self.matrix[row][column] = None

    def _search_max_area_rectangle(self):
        max_area_rectangle = (0, None, None)
        for rectangle_color in list(Color):
            rectangle = self._search_completed_color_rectangle(rectangle_color)
            if rectangle[0] > max_area_rectangle[0]:
                max_area_rectangle = rectangle

        if max_area_rectangle[0] >= self.width - 1:
            max_area_rectangle = (max_area_rectangle[0],
                                  Position(max_area_rectangle[1][0],
                                           max_area_rectangle[1][1]),
                                  Position(max_area_rectangle[2][0],
                                           max_area_rectangle[2][1]))
        else:
            return None
        return max_area_rectangle

    def _search_completed_color_rectangle(self, rectangle_color):
        skipped_items = [None, Wall.WALL]
        for _color in list(Color):
            if _color != rectangle_color:
                skipped_items.append(_color)

        max_area_rectangle = (0, [])
        width_zero_matrix = [[0 for _ in range(self.width)] for _ in range(
            self.height)]
        height_zero_matrix = [[0 for _ in range(self.width)] for _ in range(
            self.height)]

        for row in range(self.height):
            for column in range(self.width):
                if self.matrix[row][column] in skipped_items:
                    continue

                if row == 0:
                    height_zero_matrix[row][column] = 1
                else:
                    height_zero_matrix[row][column] = \
                        height_zero_matrix[row - 1][column] + 1
                if column == 0:
                    width_zero_matrix[row][column] = 1
                else:
                    width_zero_matrix[row][column] = width_zero_matrix[row][
                        column] = width_zero_matrix[row][column - 1] + 1

                min_width = width_zero_matrix[row][column]
                for delta_height in range(height_zero_matrix[row][column]):
                    min_width = min(
                        min_width,
                        width_zero_matrix[row - delta_height][column])
                    area = (delta_height + 1) * min_width
                    if area > max_area_rectangle[0]:
                        max_area_rectangle = (
                            area,
                            (row - delta_height, column - min_width + 1),
                            (row, column)
                        )
        return max_area_rectangle

    def clear_field(self):
        for row in range(self.height):
            for column in range(self.width):
                if self.matrix[row][column] is not Wall.WALL:
                    self.matrix[row][column] = None

        self.scores = 0
