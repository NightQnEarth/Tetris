from PyQt5.QtWidgets import (
    QDesktopWidget, QMessageBox, QGridLayout, QWidget, QMainWindow, QLabel,
    QHBoxLayout, QVBoxLayout, QToolButton)
from PyQt5.QtGui import QCloseEvent, QIcon
from PyQt5.QtCore import Qt, QCoreApplication, QTimer
from os import path
from pathlib import Path
import pickle

from model.color import Color
from model.wall import Wall
from view.colors_modes import ColorsModes
from model.direction import Direction
from model import falling_figure


class GameWindow(QMainWindow):
    __COLORS_MATCHING = {
        Color.RED: 'red',
        Color.YELLOW: 'yellow',
        Color.GREEN: 'green',
        Color.BLUE: 'blue',
        Wall.WALL: 'gray',
        None: 'white'
    }
    __COLORS_MODES = {
        ColorsModes.OFF: 'cyan',
        ColorsModes.GRAY: 'gray',
        ColorsModes.ON: 'green'
    }
    __MODES_MULCT = {
        ColorsModes.OFF: 1,
        ColorsModes.GRAY: 0.75,
        ColorsModes.ON: 0.6
    }

    __TICK_TIME = 500
    __CELL_SIZE = 18
    __RECORD_TABLE_FILE = 'record_table.txt'

    def __init__(self, logic_model):
        super().__init__()

        self._record_list = self._record_list_create()
        if (not isinstance(self._record_list, list) or len(
                self._record_list) != 8):
            self._record_list = [None for _ in range(8)]

        self.logic_model = logic_model
        self._cells_matrix, self._cells_panel, self._record_panel = \
            self._central_widget_create()
        self.color_mode = ColorsModes.ON
        self.current_scores = 0
        self.current_rating_position = -1
        self._record_panel_update()
        self.current_level = self.logic_model.field.current_level

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._timer_tick)
        self.timer.start(self.__TICK_TIME)

        self.__window_tune()

    def __window_tune(self):
        self.setMaximumSize(
            self.__CELL_SIZE * (self.logic_model.field.width + 4),
            self.__CELL_SIZE * self.logic_model.field.height)
        self.setWindowTitle('Tetris')
        self.setWindowIcon(QIcon(path.join('icons', 'bird.png')))
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Scores: {}'.format(
            int(self.logic_model.field.scores)))
        self.toolbar = self.addToolBar('')
        self.color_mode_button = self.toolbar_create()
        self._move_center()
        self.show()

    def toolbar_create(self):
        color_mode_button = QToolButton()
        color_mode_button.setFocusPolicy(Qt.NoFocus)
        color_mode_button.setStyleSheet('background-color: {};'.format(
                self.__COLORS_MODES[ColorsModes.ON]))
        color_mode_button.setStatusTip('Change color mode')
        color_mode_button.setFixedSize(25, 25)
        color_mode_button.clicked.connect(self._change_color_mode)
        self.toolbar.setFloatable(False)

        self.toolbar.addWidget(color_mode_button)

        return color_mode_button

    def _change_color_mode(self):
        if not self.logic_model.fell_flag:
            if self.color_mode == ColorsModes.ON:
                self.color_mode = ColorsModes.OFF
            elif self.color_mode == ColorsModes.OFF:
                self.color_mode = ColorsModes.GRAY
            else:
                self.color_mode = ColorsModes.ON

            self.color_mode_button.setStyleSheet(
                'background-color: {};'.format(
                    self.__COLORS_MODES[self.color_mode])
            )

    def _record_list_create(self):
        if not Path(self.__RECORD_TABLE_FILE).exists():
            return [0 for _ in range(8)]
        else:
            try:
                with open(self.__RECORD_TABLE_FILE, 'rb') as file:
                    return pickle.load(file)
            except (IOError, FileNotFoundError, FileExistsError,
                    pickle.PickleError):
                return [0 for _ in range(8)]

    def _central_widget_create(self):
        h_box = QHBoxLayout()
        right_panel = QVBoxLayout()

        next_figure_panel = QGridLayout()
        next_figure_panel.setSpacing(2)

        cells_panel_size = 4
        cells_panel = [[None for _ in range(cells_panel_size)] for _ in
                       range(cells_panel_size)]

        for i in range(cells_panel_size):
            for j in range(cells_panel_size):
                cell = QLabel()
                cell.setFixedSize(self.__CELL_SIZE, self.__CELL_SIZE)
                cell.setStyleSheet('background-color: {};'.format(
                    self.__COLORS_MATCHING[None]))
                next_figure_panel.addWidget(cell, i, j)
                cells_panel[i][j] = cell

        right_panel.addLayout(next_figure_panel)
        right_panel.setSpacing(9 * self.__CELL_SIZE - 2)

        score_table = QGridLayout()
        score_table.setSpacing(2)
        lines_panel = [None for _ in range(8)]

        self._record_list.sort()
        records_count = 8
        for i in range(records_count):
            line = QLabel()
            line.setText('{}. result: {}'.format(i + 1, self._record_list[
                records_count - i - 1]))
            line.setStyleSheet('background-color: {};'.format(
                self.__COLORS_MATCHING[None]))
            line.setFixedSize(4 * self.__CELL_SIZE, self.__CELL_SIZE)
            score_table.addWidget(line, i, 1)
            lines_panel[i] = line

        right_panel.addLayout(score_table)

        grid = QGridLayout()
        grid.setSpacing(2)

        cells_matrix = [[None for _ in range(self.logic_model.field.width)]
                        for _ in range(self.logic_model.field.height)]

        for i in range(self.logic_model.field.height):
            for j in range(self.logic_model.field.width):
                cell = QLabel()
                cell.setFixedSize(self.__CELL_SIZE, self.__CELL_SIZE)
                cell.setStyleSheet('background-color: {};'.format(
                    self.__COLORS_MATCHING[self.logic_model.field.matrix[i][j]]
                ))
                grid.addWidget(cell, i, j)
                cells_matrix[i][j] = cell

        h_box.addLayout(grid)
        h_box.addLayout(right_panel)
        game_field_widget = QWidget()
        game_field_widget.setLayout(h_box)
        self.setCentralWidget(game_field_widget)

        return cells_matrix, cells_panel, lines_panel

    def _grid_update(self):
        for i in range(self.logic_model.field.height):
            for j in range(self.logic_model.field.width):
                color = self.__COLORS_MATCHING[
                    self.logic_model.field.matrix[i][j]]
                self._cells_matrix[i][j].setStyleSheet(
                    'background-color: {};'.format(color))

    def _next_figure_panel_update(self):
        for i in range(len(self._cells_panel)):
            for j in range(len(self._cells_panel[i])):
                self._cells_panel[i][j].setStyleSheet(
                    'background-color: {};'.format(
                        self.__COLORS_MATCHING[None]))
        row_shift = 3
        column_shift = 1
        figure = self.logic_model.next_figure
        for _tuple in falling_figure.FIGURES_POSITIONS[figure]:
            row = _tuple[0] + row_shift
            column = _tuple[1] + column_shift

            if self.color_mode == ColorsModes.ON:
                color = self.__COLORS_MATCHING[self.logic_model.next_color]
            elif self.color_mode == ColorsModes.GRAY:
                color = 'gray'
            else:
                color = self.__COLORS_MATCHING[None]

            self._cells_panel[row][column].setStyleSheet(
                'background-color: {};'.format(color))

    def _record_panel_update(self):
        self._record_list.sort()

        i = 0
        while (i < len(self._record_list) and
               self.logic_model.field.scores > self._record_list[i]):
            i += 1

        if i > 0 and i - 1 != self.current_rating_position:
            if self.current_rating_position >= 0:
                self._record_list.pop(self.current_rating_position)
            else:
                self._record_list.pop(0)
            self._record_list.insert(i - 1, self.logic_model.field.scores)
        elif i > 0:
            self._record_list[self.current_rating_position] = \
                self.logic_model.field.scores

        current_position = i - 1
        self.current_rating_position = current_position

        for i in range(len(self._record_list)):
            label = self._record_panel[7 - i]
            label.setText('{}. {}'.format(8 - i, self._record_list[i]))
            label.setStyleSheet(
                'background-color: {};'.format('white')
            )
            if i == self.current_rating_position:
                label.setStyleSheet(
                    'background-color: {};'.format('rgb(109, 242, 231)')
                )

    def _timer_tick(self):
        if not self.logic_model.end_of_the_game():
            self.logic_model.update()
            self._grid_update()
            self._next_figure_panel_update()
            if self.logic_model.fell_flag:
                self.color_mode_button.setDisabled(True)

            if self.current_scores < self.logic_model.field.scores:
                self.logic_model.field.scores = \
                    round(self.logic_model.field.scores * self.__MODES_MULCT[
                        self.color_mode])
                self.current_scores = self.logic_model.field.scores
                self._record_panel_update()

            if self.current_level < self.logic_model.field.current_level:
                self.current_level += 1
                self.__TICK_TIME = self.__TICK_TIME * 0.85
                self.timer.setInterval(self.__TICK_TIME)

            self.status_bar.showMessage('Scores: {}'.format(
                int(self.logic_model.field.scores)))
        else:
            self.timer.stop()
            self.status_bar.showMessage('End of the game')

    def _move_center(self):
        self.move(self.width() * -2, 0)
        self.show()
        exact_window_form = self.frameGeometry()
        exact_desktop_center = QDesktopWidget().availableGeometry().center()
        exact_window_form.moveCenter(exact_desktop_center)
        self.move(exact_window_form.topLeft())

    def closeEvent(self, event):
        self.timer.stop()
        self.status_bar.showMessage('Pause')
        caption = 'Confirm Exit'
        question = 'Are you sure you want to exit Tetris?'
        message_box = QMessageBox()
        reply = message_box.question(
            self,
            caption,
            question,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        if reply == message_box.Yes:
            try:
                with open(self.__RECORD_TABLE_FILE, 'wb') as file:
                    pickle.dump(self._record_list, file)
            except (IOError, FileNotFoundError, FileExistsError,
                    pickle.PickleError):
                    pass
            QCoreApplication.exit()
        else:
            event.ignore()

            self.status_bar.showMessage('Scores: {}'.format(
                int(self.logic_model.field.scores)))
            self.timer.start()

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Escape:
            self.closeEvent(QCloseEvent())

        elif key == Qt.Key_R:
            self.logic_model.field.clear_field()
            self.logic_model.next_figure = None
            self.logic_model.next_color = None
            self.logic_model.current_figure = None
            self.logic_model.current_color = None
            self.logic_model.falling_figure = falling_figure.FallingFigure(
                self.logic_model)
            self.logic_model.fell_flag = False
            self.color_mode_button.setEnabled(True)
            self.current_rating_position = -1
            self.current_scores = 0
            self._record_panel_update()
            self.timer.start()

        elif key == Qt.Key_P:
            if self.timer.isActive():
                self.status_bar.showMessage('Pause')
                self.timer.stop()
            elif not self.logic_model.end_of_the_game():
                self.timer.start()

        elif self.timer.isActive():
            if key == Qt.Key_Left:
                self.logic_model.falling_figure.try_move(Direction.LEFT)

            elif key == Qt.Key_Right:
                self.logic_model.falling_figure.try_move(Direction.RIGHT)

            elif key == Qt.Key_Down:
                self.logic_model.falling_figure.try_move(Direction.DOWN)

            elif key == Qt.Key_Up:
                self.logic_model.falling_figure.try_rotate_left()

            elif key == Qt.Key_Space:
                self.logic_model.falling_figure.drop_figure()
                self.logic_model.falling_figure = \
                    falling_figure.FallingFigure(self.logic_model)
                self.logic_model.field.remove_completed_rectangle(
                    self.logic_model.falling_figure)
                self.logic_model.fell_flag = True

        self._grid_update()
