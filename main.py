from PyQt6.QtWidgets import QApplication
import sys

from ui.main_window import UIMainWindow
from ui.stylesheets import dark_theme_global_1, dark_theme_global_2, dark_theme_global_3


def main():
    app = QApplication(sys.argv)

    #Style
    #app.setStyleSheet(dark_theme_global_1())

    app.setStyleSheet(dark_theme_global_3())

    window = UIMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
