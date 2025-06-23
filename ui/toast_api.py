# toast_api.py
from ui.toast import Toast


def init_toast(parent):
    Toast.set_parent(parent)

def toast(message: str):
    from PyQt6.QtWidgets import QApplication
    if not QApplication.instance():
        raise RuntimeError("QApplication not running")

    Toast.instance().show_message(message)