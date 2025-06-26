def dark_theme_global() -> str:
    return """

        /*
     * Ultra-Minimal, High-End Dark Theme
     * Inspired by Apple, Labelbox, V7 Labs, Photoshop
     */

    * {
        font-family: "Inter", "SF Pro Text", "Segoe UI", Arial, sans-serif;
        font-size: 13px;
        color: #f0f0f0;
        background: transparent;
    }

    /* --- Base Background --- */
    QMainWindow, QWidget {
        background-color: #121212;
    }

    /* --- Floating Toolbar --- */
    QWidget#FloatingControlsFrame {
        background-color: rgba(30, 30, 30, 0.85);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 4px;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.5);
    }

    QWidget#FloatingTitleBar {
        background-color: transparent;
        padding: 6px 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        font-weight: 600;
        color: #ffffff;
    }

    /* --- Save Dialog Specific Styling --- */
    QDialog {
        background-color: transparent; /* Needed for translucent background on the main frame */
    }

    QFrame#SaveDialogFrame {
        background-color: rgba(30, 30, 30, 0.9); /* Slightly more opaque than floating controls */
        border-radius: 12px; /* Slightly larger radius for a dialog */
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.6); /* More prominent shadow for a modal dialog */
    }

    /* --- Buttons --- */
    QPushButton {
        background-color: transparent;
        color: #f0f0f0;
        border: none;
        padding: 8px 16px; /* Slightly more padding for general buttons */
        border-radius: 8px; /* Slightly larger border-radius */
        font-weight: 500;
        transition: all 0.15s ease-in-out;
        min-width: 80px; /* Ensure buttons have a minimum width */
    }

    QPushButton:hover {
        background-color: rgba(255, 255, 255, 0.08); /* More subtle hover */
    }

    QPushButton:pressed {
        background-color: rgba(255, 255, 255, 0.15);
    }

    QPushButton:disabled {
        color: #666666;
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Specific button styling for Save Dialog */
    QPushButton#SaveActionButton {
        background-color: #0A84FF; /* Apple blue */
        color: white;
        font-weight: 600;
    }
    QPushButton#SaveActionButton:hover {
        background-color: #30A4FF;
    }
    QPushButton#SaveActionButton:pressed {
        background-color: #007ACC;
    }
    QPushButton#SaveActionButton:disabled {
        background-color: #1a4d7d;
        color: #999999;
    }

    QPushButton#CancelButton {
        background-color: transparent;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    QPushButton#CancelButton:hover {
        background-color: rgba(255, 255, 255, 0.05);
    }
    QPushButton#CancelButton:pressed {
        background-color: rgba(255, 255, 255, 0.1);
    }

    QPushButton#BrowseButton {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 6px 12px;
        min-width: 60px;
    }
    QPushButton#BrowseButton:hover {
        background-color: rgba(255, 255, 255, 0.1);
    }
    QPushButton#BrowseButton:pressed {
        background-color: rgba(255, 255, 255, 0.15);
    }

    QPushButton#FloatingCloseButton {
        background-color:#b3ff30;
        color: white;
        border: none;
        width: 4px;
        height: 4px;
        
        /* IMPORTANT: Override the general min-width and add min-height */
        min-width: 4px;   /* Must be less than or equal to desired width */
        max-width: 4x;   /* Set max-width to fix it */
        min-height: 4px;  /* Set min-height */
        max-height: 4px;  /* Set max-height to fix it */
        
        border-radius: 6px;
        font-size: 8px;
        font-weight: bold;
        margin: 0 4px;
    }

    QPushButton#FloatingCloseButton:hover {
        background-color: #ff307c;
    }

    /* --- Labels --- */
    QLabel {
        color: #e0e0e0; /* Slightly brighter for general labels */
        font-size: 13px;
        padding: 0;
    }

    QLabel#titleLabel {
        font-size: 14px;
        font-weight: 600;
        color: #ffffff;
    }

    /* --- Sliders --- */
    QSlider::groove:horizontal {
        height: 4px;
        background: #2c2c2e;
        border-radius: 2px;
    }

    QSlider::handle:horizontal {
        background: #0A84FF;
        width: 14px;
        height: 14px;
        border-radius: 7px;
        margin: -5px 0;
    }

    QSlider::add-page:horizontal {
        background: #3a3a3c;
        border-radius: 2px;
    }

    QSlider::sub-page:horizontal {
        background: #0A84FF;
        border-radius: 2px;
    }

    /* --- ProgressBar --- */
    QProgressBar {
        background-color: #1c1c1e;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        height: 10px;
        text-align: center;
    }

    QProgressBar::chunk {
        background-color: #30d158;
        border-radius: 6px;
    }

    /* --- Inputs --- */
    QLineEdit {
        background-color: rgba(255, 255, 255, 0.05);
        color: #f0f0f0;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 8px 10px; /* Increased padding */
    }

    QLineEdit:focus {
        border: 1px solid #0A84FF;
        background-color: rgba(255, 255, 255, 0.08);
    }

    /* --- QComboBox (Dropdown) --- */
    QComboBox {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 8px 10px;
        color: #f0f0f0;
        min-height: 28px; /* Ensure minimum height */
    }

    QComboBox:hover {
        background-color: rgba(255, 255, 255, 0.1);
    }

    QComboBox:focus {
        border: 1px solid #0A84FF;
        background-color: rgba(255, 255, 255, 0.08);
    }

    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 25px;
        border-left: 1px solid rgba(255, 255, 255, 0.1);
        border-top-right-radius: 8px;
        border-bottom-right-radius: 8px;
    }

    QComboBox::down-arrow {
        image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNNyAxMExMTIgMTVMMTcgMTBaIiBmaWxsPSIjRkZGRkZGMDAiLz48L3N2Zz4=); /* A simple down arrow SVG, you might want to replace with a more fitting one or use a font icon */
        width: 12px;
        height: 12px;
    }
    QComboBox::down-arrow:on {
        transform: rotate(180deg); /* Rotate arrow when dropdown is open */
    }

    QComboBox QAbstractItemView {
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 8px;
        background-color: #2c2c2e; /* Background for dropdown items */
        selection-background-color: #0A84FF; /* Selected item background */
        color: #f0f0f0; /* Text color for items */
        padding: 5px 0px;
    }
    QComboBox QAbstractItemView::item {
        min-height: 30px; /* Height for each item in the dropdown */
        padding: 5px 15px; /* Padding for each item */
    }
    QComboBox QAbstractItemView::item:selected {
        color: white;
    }

    /* --- Scrollbar --- */
    QScrollBar:vertical, QScrollBar:horizontal {
        background: transparent;
        width: 6px;
        margin: 2px;
    }

    QScrollBar::handle {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 3px;
    }

    QScrollBar::handle:hover {
        background: rgba(255, 255, 255, 0.2);
    }

    /* --- Tooltips --- */
    QToolTip {
        background-color: rgba(50, 50, 50, 0.95);
        color: #ffffff;
        border: 1px solid #3c3c3c;
        padding: 5px 10px;
        border-radius: 6px;
        font-size: 12px;
    }

    QMenuBar {
        background-color: #2b2b2b;
        color: #cccccc;
    }

    QMenuBar::item:selected {
        background: #0A84FF;
    }

    QMenu {
        background-color: #2b2b2b;
        color: #cccccc;
        border-radius: 8px; /* Rounded corners for context menus */
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    QMenu::item {
        padding: 8px 15px; /* Padding for menu items */
        background-color: transparent;
    }
    QMenu::item:selected {
        background-color: #007acc; /* Selection background */
        color: white;
        border-radius: 4px; /* Slightly rounded selection */
    }
    QMenu::separator {
        height: 1px;
        background-color: rgba(255, 255, 255, 0.1);
        margin: 5px 0px;
    }

    """
