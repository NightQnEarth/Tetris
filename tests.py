import unittest
from model import logic_model, direction, position, figure
from model import falling_figure
from model.color import Color
from model.wall import Wall


class Tests(unittest.TestCase):
    LogicModel = None

    ITEM_TO_SYMBOL = {
        None: '.',
        Color.RED: str(Color.RED.value),
        Color.GREEN: str(Color.GREEN.value),
        Color.YELLOW: str(Color.YELLOW.value),
        Color.BLUE: str(Color.BLUE.value),
        Wall.WALL: 'x'
    }
    SYMBOL_TO_ITEM = {
        '.': None,
        str(Color.RED.value): Color.RED,
        str(Color.GREEN.value): Color.GREEN,
        str(Color.YELLOW.value): Color.YELLOW,
        str(Color.BLUE.value): Color.BLUE,
        'x': Wall.WALL
    }

    def matrix_to_string(self, matrix):
        return '\n'.join(
            ''.join(self.ITEM_TO_SYMBOL[item] for item in row)
            for row in matrix)

    def string_to_matrix(self, string):
        return [[self.SYMBOL_TO_ITEM[symbol] for symbol in line]
                for line in string.splitlines()]

    def make_action_and_compare_results(
            self, entered_, expected, action, *args):
        self.LogicModel.field.matrix = self.string_to_matrix(entered_)
        action(*args)
        actual = self.matrix_to_string(self.LogicModel.field.matrix)
        self.assertEqual(expected, actual)

    def create_and_shift_figure(self):
        positions = []
        shift = 4
        for _tuple in falling_figure.FIGURES_POSITIONS[figure.Figure.I_FIGURE]:
            positions.append(position.Position(
                _tuple[0] + shift, _tuple[1] + shift))
        self.LogicModel.falling_figure.positions_list = positions
        self.LogicModel.falling_figure.color = Color.RED

    def setUp(self):
        self.LogicModel = logic_model.LogicModel(10, 10)

    def test_remove_horizontal_line(self):
        entered_ = ("x....1....\n"
                    "222222222x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x")
        expected = ("x.........\n"
                    ".....1...x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x")
        self.make_action_and_compare_results(
            entered_, expected,
            self.LogicModel.field.remove_completed_rectangle,
            self.LogicModel.falling_figure)

    def test_remove_vertical_line(self):
        entered_ = ("x....1....\n"
                    ".....2...x\n"
                    "x....2....\n"
                    ".....2...x\n"
                    "x....2....\n"
                    ".....2...x\n"
                    "x....2....\n"
                    ".....2...x\n"
                    "x....2....\n"
                    ".....2...x")
        expected = ("x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".....1...x")
        self.make_action_and_compare_results(
            entered_, expected,
            self.LogicModel.field.remove_completed_rectangle,
            self.LogicModel.falling_figure)

    def test_remove_square(self):
        entered_ = ("x.22222...\n"
                    "...111...x\n"
                    "x..111....\n"
                    "...111...x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x")
        expected = ("x.2...2...\n"
                    ".........x\n"
                    "x.........\n"
                    "...222...x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x")
        self.make_action_and_compare_results(
            entered_, expected,
            self.LogicModel.field.remove_completed_rectangle,
            self.LogicModel.falling_figure)

    def test_remove_one_of_two_rectangle(self):
        entered_ = ("x1111.....\n"
                    ".1111....x\n"
                    "x1111.....\n"
                    ".1111....x\n"
                    "x222......\n"
                    ".222.....x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x")
        expected = ("x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x222......\n"
                    ".222.....x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x")
        self.make_action_and_compare_results(
            entered_, expected,
            self.LogicModel.field.remove_completed_rectangle,
            self.LogicModel.falling_figure)

    def test_remove_both_rectangle(self):
        entered_ = ("x333......\n"
                    ".333.....x\n"
                    "x333......\n"
                    "....444..x\n"
                    "x...444...\n"
                    "....444..x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x")
        expected = ("x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x")
        self.make_action_and_compare_results(
            entered_, expected,
            self.LogicModel.field.remove_completed_rectangle,
            self.LogicModel.falling_figure)

    def test_two_colors_rectangle(self):
        entered_ = ("x.........\n"
                    ".........x\n"
                    "x.........\n"
                    "...3311..x\n"
                    "x..3311...\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x")
        expected = ("x.........\n"
                    ".........x\n"
                    "x.........\n"
                    "...3311..x\n"
                    "x..3311...\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x")
        self.make_action_and_compare_results(
            entered_, expected,
            self.LogicModel.field.remove_completed_rectangle,
            self.LogicModel.falling_figure)

    def test_two_intersecting_rectangles(self):
        entered_ = ("x.........\n"
                    ".........x\n"
                    "x.444.....\n"
                    "..444....x\n"
                    "x.44222...\n"
                    "....222..x\n"
                    "x...222...\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x")
        expected = ("x.........\n"
                    ".........x\n"
                    "x.44......\n"
                    "..44.....x\n"
                    "x.44......\n"
                    "....4....x\n"
                    "x...4.....\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x")
        self.make_action_and_compare_results(
            entered_, expected,
            self.LogicModel.field.remove_completed_rectangle,
            self.LogicModel.falling_figure)

    def test_rectangle_with_walls(self):
        entered_ = ("x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x......111\n"
                    ".......11x\n"
                    "x......111\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x")
        expected = ("x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x......111\n"
                    ".......11x\n"
                    "x......111\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x")
        self.make_action_and_compare_results(
            entered_, expected,
            self.LogicModel.field.remove_completed_rectangle,
            self.LogicModel.falling_figure)

    def test_rectangle_with_empty_cells(self):
        entered_ = ("x...333...\n"
                    "....3.3..x\n"
                    "x...3.3...\n"
                    "....333..x\n"
                    "x.........\n"
                    ".22222...x\n"
                    "x22.22....\n"
                    ".2.2.2...x\n"
                    "x22.22....\n"
                    ".22222...x")
        expected = ("x...333...\n"
                    "....3.3..x\n"
                    "x...3.3...\n"
                    "....333..x\n"
                    "x.........\n"
                    ".22222...x\n"
                    "x22.22....\n"
                    ".2.2.2...x\n"
                    "x22.22....\n"
                    ".22222...x")
        self.make_action_and_compare_results(
            entered_, expected,
            self.LogicModel.field.remove_completed_rectangle,
            self.LogicModel.falling_figure)

    def test_consistently_destroy(self):
        entered_ = ("x.22222...\n"
                    "...222...x\n"
                    "x..333....\n"
                    "...111...x\n"
                    "x..111....\n"
                    "...111...x\n"
                    "x..111....\n"
                    "...333...x\n"
                    "x..333....\n"
                    "...222...x")
        expected = ("x.2...2...\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x")
        self.make_action_and_compare_results(
            entered_, expected,
            self.LogicModel.field.remove_completed_rectangle,
            self.LogicModel.falling_figure)

    def test_destroy_rectangles_with_different_squares(self):
        entered_ = ("x.........\n"
                    ".........x\n"
                    "x.....22..\n"
                    "......22.x\n"
                    "x111..22..\n"
                    ".111..22.x\n"
                    "x111..22..\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x")
        expected = ("x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x")
        self.make_action_and_compare_results(
            entered_, expected,
            self.LogicModel.field.remove_completed_rectangle,
            self.LogicModel.falling_figure)

    def test_clear_field(self):
        entered_ = ("x...2..3..\n"
                    ".........x\n"
                    "x.....2...\n"
                    "3........x\n"
                    "x.........\n"
                    "2.....433x\n"
                    "x.....3332\n"
                    "1.....333x\n"
                    "x........1\n"
                    ".........x")
        expected = ("x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x")
        self.LogicModel.field.clear_field()
        self.make_action_and_compare_results(entered_, expected,
                                             self.LogicModel.field.clear_field)

    def test_end_of_the_game(self):
        entered_ = ("x...33....\n"
                    "....3....x\n"
                    "x.2..3....\n"
                    "..4..3.2.x\n"
                    "x....32...\n"
                    "....22...x\n"
                    "x....4....\n"
                    ".....4...x\n"
                    "x....4....\n"
                    ".....1...x")
        self.LogicModel.field.matrix = self.string_to_matrix(entered_)
        self.assertTrue(self.LogicModel.end_of_the_game())

    def test_drop_figure(self):
        entered_ = ("x...1.....\n"
                    "....1....x\n"
                    "x...1.....\n"
                    "....1....x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x")
        expected = ("x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x...1.....\n"
                    "....1....x\n"
                    "x...1.....\n"
                    "....1....x")
        self.create_and_shift_figure()
        self.make_action_and_compare_results(
            entered_, expected,
            self.LogicModel.falling_figure.drop_figure)

    def test_update(self):
        self.LogicModel.update()
        self.assertTrue(any(self.LogicModel.field.matrix[0]))

    def test_move(self):
        entered_ = ("x...1.....\n"
                    "....1....x\n"
                    "x...1.....\n"
                    "....1....x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x")
        expected = ("x.........\n"
                    "....1....x\n"
                    "x...1.....\n"
                    "....1....x\n"
                    "x...1.....\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x")

        self.create_and_shift_figure()
        self.make_action_and_compare_results(
            entered_, expected, self.LogicModel.falling_figure.try_move,
            direction.Direction.DOWN)

    def test_rotate(self):
        entered_ = ("x...1.....\n"
                    "....1....x\n"
                    "x...1.....\n"
                    "....1....x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x")
        expected = ("x...1111..\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x\n"
                    "x.........\n"
                    ".........x")

        self.create_and_shift_figure()
        self.make_action_and_compare_results(
            entered_, expected, self.LogicModel.falling_figure.try_rotate_left)


if __name__ == '__main__':
    unittest.main()
