from PyQt6.QtWidgets import QApplication
import sys

from ui.main_window import UIMainWindow

def main():
    app = QApplication(sys.argv)
    window = UIMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
