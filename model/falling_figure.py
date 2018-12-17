from model.color import Color
from model.wall import Wall
from model.direction import Direction
from model.figure import Figure
from model.position import Position
import random
import copy

FIGURES_POSITIONS = {
    Figure.I_FIGURE: [(-1, 0), (-2, 0), (-3, 0), (-4, 0)],
    Figure.J_FIGURE: [(-1, 0), (-2, 0), (-3, 0), (-1, -1)],
    Figure.L_FIGURE: [(-1, 0), (-2, 0), (-3, 0), (-1, 1)],
    Figure.O_FIGURE: [(-1, 0), (-2, 0), (-1, 1), (-2, 1)],
    Figure.S_FIGURE: [(-1, 0), (-2, 0), (-1, -1), (-2, 1)],
    Figure.T_FIGURE: [(-1, 0), (-2, 0), (-1, -1), (-1, 1)],
    Figure.N_FIGURE: [(-1, 0), (-2, 0), (-2, 1), (-3, 1)]
}


class FallingFigure:
    def __init__(self, logic_model):
        self.field = logic_model.field
        self.positions_list, self.color = _random_figure_generate(
            self.field.width, logic_model)
        self.display_figure_on_field()

    def try_move(self, direction):
        if self.check_move(direction):
            self.remove_figure_from_field()

            for positions in self.positions_list:
                if direction == Direction.LEFT:
                    positions.column -= 1
                elif direction == Direction.RIGHT:
                    positions.column += 1
                elif direction == Direction.UP:
                    positions.row -= 1
                else:
                    positions.row += 1

            self.display_figure_on_field()

    def check_move(self, direction):
        for position in self.positions_list:
            new_row = position.row
            new_column = position.column

            if direction == Direction.LEFT:
                new_column -= 1
            elif direction == Direction.RIGHT:
                new_column += 1
            elif direction == Direction.UP:
                new_row -= 1
            else:
                new_row += 1

            if not self._is_valid_position(new_row, new_column):
                return False

        return True

    def try_rotate_left(self):
        data_for_rotate = self._check_rotate_left()
        if data_for_rotate is not None:
            self.remove_figure_from_field()
            self.positions_list = data_for_rotate
            self.display_figure_on_field()

    def _check_rotate_left(self):
        min_row = self.field.height
        min_column = self.field.width
        for position in self.positions_list:
            if position.row < min_row:
                min_row = position.row
            if position.column < min_column:
                min_column = position.column

        new_min_row = self.field.height
        new_min_column = self.field.width
        new_positions = []
        for position in self.positions_list:
            new_row = min_row - (position.column - min_column)
            new_column = position.row - min_row + min_column

            new_positions.append(Position(new_row, new_column))

            if new_row < new_min_row:
                new_min_row = new_row
            if new_column < new_min_column:
                new_min_column = new_column

        if new_min_row < min_row:
            for new_position in new_positions:
                new_position.row += min_row - new_min_row
        if new_min_column < min_column:
            for new_position in new_positions:
                new_position.column += min_column - new_min_column

        for new_position in new_positions:
            if not self._is_valid_position(
                    new_position.row, new_position.column):
                return None

        return new_positions

    def _is_valid_position(self, row, column):
        if (row >= self.field.height or
                not 0 <= column < self.field.width):
            return False

        if self.field.matrix[row][column] == Wall.WALL:
            return False

        position_in_figure_flag = False
        for _position in self.positions_list:
            if row == _position.row and column == _position.column:
                position_in_figure_flag = True
                break

        if (not position_in_figure_flag and
            row >= 0 and column >= 0 and
                self.field.matrix[row][column]):
            return False

        return True

    def remove_figure_from_field(self):
        for position in self.positions_list:
            if position.row >= 0 and position.column >= 0:
                self.field.matrix[position.row][position.column] = None

    def display_figure_on_field(self):
        for position in self.positions_list:
            if position.row >= 0 and position.column >= 0:
                self.field.matrix[position.row][position.column] = self.color

    def drop_figure(self):
        while self.check_move(Direction.DOWN):
            self.try_move(Direction.DOWN)


def _random_figure_generate(field_width, logic_model):
    figures_list = list(FIGURES_POSITIONS.keys())

    if logic_model.current_figure is not None:
        logic_model.current_figure = logic_model.next_figure
        logic_model.current_color = logic_model.next_color
    else:
        logic_model.current_figure = random.choice(figures_list)
        logic_model.current_color = random.choice(list(Color))

    figures_list.remove(logic_model.current_figure)
    logic_model.next_figure = random.choice(figures_list)
    logic_model.next_color = random.choice(list(Color))

    figure_positions = copy.deepcopy(
        FIGURES_POSITIONS[logic_model.current_figure])

    shift_positions = []
    shift = field_width // 2 - 1
    for position in figure_positions:
        shift_positions.append(Position(position[0], position[1] + shift))

    return shift_positions, logic_model.current_color
