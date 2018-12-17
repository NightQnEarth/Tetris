from PyQt5.QtWidgets import QApplication
import sys
from view.game_window import GameWindow
from model import logic_model


if __name__ == '__main__':
    app = QApplication(sys.argv)
    _ = GameWindow(logic_model.LogicModel())
    sys.exit(app.exec())
