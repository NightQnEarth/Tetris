from model.direction import Direction
from model import field, falling_figure


class LogicModel:
    __FIELD_WIDTH = 10
    __FIELD_HEIGHT = 20

    def __init__(self, width=__FIELD_WIDTH, height=__FIELD_HEIGHT):
        self.current_figure = None
        self.current_color = None
        self.next_figure = None
        self.next_color = None

        self.field = field.Field(width, height)
        self.falling_figure = falling_figure.FallingFigure(self)
        self.fell_flag = False

    def update(self):
        if self.falling_figure.check_move(Direction.DOWN):
            self.falling_figure.try_move(Direction.DOWN)
        else:
            self.fell_flag = True
            self.falling_figure = falling_figure.FallingFigure(self)
            self.falling_figure.try_move(Direction.DOWN)
            self.field.remove_completed_rectangle(self.falling_figure)

    def end_of_the_game(self):
        figure_not_on_field_flag = False
        for position in self.falling_figure.positions_list:
            if position.row < 0:
                figure_not_on_field_flag = True
                break

        return (not self.falling_figure.check_move(Direction.DOWN) and
                figure_not_on_field_flag)
