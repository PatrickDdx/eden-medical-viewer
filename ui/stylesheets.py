def dark_theme() -> str:
    return """
            QMainWindow {
                background-color: #2b2b2b;
            }

            QLabel {
                color: #eeeeee;
                font-size: 14px;
            }

            QSlider::groove:horizontal {
                border: 1px solid #444;
                height: 6px;
                background: #666;
                margin: 2px 0;
                border-radius: 3px;
            }

            QSlider::handle:horizontal {
                background: #00bcd4;
                border: 1px solid #5c5c5c;
                width: 14px;
                height: 14px;
                margin: -4px 0;
                border-radius: 7px;
            }

            QDockWidget {
                titlebar-close-icon: url(none);
                titlebar-normal-icon: url(none);
                font-weight: bold;
                color: #ffffff;
                border: 1px solid #444444;
                background-color: #333333;
                border-radius: 6px;
            }
            
            QDockWidget::title {
                background-color: #3d3d3d;
                padding: 4px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }

            QDockWidget:hover {
                border: 1px solid #00bcd4;
            }


            QMenuBar {
                background-color: #2b2b2b;
                color: #cccccc;
            }

            QMenuBar::item:selected {
                background: #444444;
            }

            QMenu {
                background-color: #2b2b2b;
                color: #cccccc;
            }

            QMenu::item:selected {
                background-color: #007acc;
                color: white;
            }


            QPushButton {
                background-color: #3c3c3c;
                color: white;
                border-radius: 4px;
                padding: 6px 12px;
            }

            QPushButton:hover {
                background-color: #555;
            }
        """



