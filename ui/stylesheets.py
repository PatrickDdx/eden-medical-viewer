def dark_theme_global_4() -> str:
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

def dark_theme_global_3() -> str:
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
    
    /* --- Buttons --- */
    QPushButton {
        background-color: transparent;
        color: #f0f0f0;
        border: none;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.15s ease-in-out;
    }
    
    QPushButton:hover {
        background-color: rgba(255, 255, 255, 0.05);
    }
    
    QPushButton:pressed {
        background-color: rgba(255, 255, 255, 0.1);
    }
    
    QPushButton#FloatingCloseButton {
        background-color: #b3ff30;
        color: white;
        border: none;
        width: 9px;
        height: 9px;
        border-radius: 4px;
        font-size: 5px;
        font-weight: bold;
        margin: 0 4px;
    }
    
    QPushButton#FloatingCloseButton:hover {
        background-color: #ff307c;
    }
    
    /* --- Labels --- */
    QLabel {
        color: #f0f0f0;
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
    QLineEdit, QTextEdit {
        background-color: rgba(255, 255, 255, 0.05);
        color: #f0f0f0;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 6px 10px;
    }
    
    QLineEdit:focus, QTextEdit:focus {
        border: 1px solid #0A84FF;
        background-color: rgba(255, 255, 255, 0.08);
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
            }

            QMenu::item:selected {
                background-color: #007acc;
                color: white;
            }

    
    """

def dark_theme_global_2() -> str:
    return """
    
        /* Global */
    QWidget {
        background-color: #1C1C1E;
        color: #E5E5EA;
        font-family: -apple-system, "Segoe UI", "Helvetica Neue", sans-serif;
        font-size: 14px;
    }
    
    /* Main Window + Dialogs */
    QMainWindow, QDialog {
        background-color: #1C1C1E;
        border: 1px solid #3A3A3C;
        border-radius: 12px;
        padding: 16px;
    }
    
    /* Labels */
    QLabel {
        color: #E5E5EA;
    }
    
    QLabel[role="caption"] {
        font-size: 12px;
        color: #8E8E93;
    }
    
    QLabel[role="title"] {
        font-size: 20px;
        font-weight: 600;
        color: #FFFFFF;
    }
    
    /* Buttons */
    QPushButton {
        background-color: #0A84FF;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    QPushButton:hover {
        background-color: #007AFF;
    }
    
    QPushButton:pressed {
        background-color: #005BBB;
    }
    
    QPushButton:disabled {
        background-color: #3A3A3C;
        color: #636366;
    }
    
    /* Text Inputs */
    QLineEdit, QTextEdit {
        background-color: #2C2C2E;
        border: 1px solid #3A3A3C;
        border-radius: 8px;
        padding: 6px 10px;
        color: #E5E5EA;
    }
    
    QLineEdit:focus, QTextEdit:focus {
        border: 1px solid #0A84FF;
        outline: none;
    }
    
    /* Toolbars */
    QToolBar {
        background-color: #1C1C1E;
        border-bottom: 1px solid #3A3A3C;
        spacing: 6px;
    }
    
    /* GroupBox */
    QGroupBox {
        border: 1px solid #3A3A3C;
        border-radius: 12px;
        margin-top: 16px;
        background-color: #2C2C2E;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 6px;
        font-weight: 600;
        color: #E5E5EA;
    }
    
    /* Tables */
    QTableView {
        background-color: #1C1C1E;
        border: 1px solid #3A3A3C;
        gridline-color: #3A3A3C;
        alternate-background-color: #2C2C2E;
        color: #E5E5EA;
    }
    
    QHeaderView::section {
        background-color: #2C2C2E;
        color: #E5E5EA;
        padding: 6px;
        font-weight: 600;
        border: none;
        border-bottom: 1px solid #3A3A3C;
    }
    
    /* Scrollbars */
    QScrollBar:vertical, QScrollBar:horizontal {
        background: transparent;
        width: 8px;
        height: 8px;
        margin: 2px;
    }
    
    QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 4px;
    }
    
    QScrollBar::handle:hover {
        background: rgba(255, 255, 255, 0.25);
    }
    
    /* ComboBox */
    QComboBox {
        background-color: #2C2C2E;
        color: #E5E5EA;
        border: 1px solid #3A3A3C;
        border-radius: 8px;
        padding: 6px 10px;
    }
    
    QComboBox QAbstractItemView {
        background-color: #2C2C2E;
        selection-background-color: #0A84FF;
        selection-color: white;
    }
    
    /* Tooltip */
    QToolTip {
        background-color: #2C2C2E;
        color: #FFFFFF;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 12px;
        border: 1px solid #3A3A3C;
    }
    

    
    """

def dark_theme_global_1() -> str:
    """
    Perfected PyQt6 Stylesheet for a Professional, Clean, and Magical UI.
    Inspired by Apple, Labelbox, and V7 Labs.
    """
    return """
    /*
     * Perfected PyQt6 Stylesheet for a Professional, Clean, and Magical UI
     * Inspired by Apple, Labelbox, and V7 Labs.
     */

    /* --- Global Settings --- */
    * {
        /* Set a modern, clean font - ensure it's available on the system or bundled */
        font-family: "Inter", "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        font-size: 14px;
        color: #e0e0e0; /* Default text color: light gray */
        outline: none; /* Remove focus rectangle by default, style focus explicitly */
    }

    /* Base Window and Widget Backgrounds */
    QMainWindow, QWidget, QDockWidget {
        background-color: #1e1e1e; /* Deep charcoal base background */
    }

    /* --- QMenuBar and QMenu Styling --- */
    QMenuBar {
        background-color: #2b2b2b; /* Slightly lighter than base for distinction */
        border-bottom: 1px solid #3c3c3c; /* Subtle separator */
        padding: 0; /* No padding on the bar itself */
    }

    QMenuBar::item {
        padding: 10px 15px; /* Comfortable padding for menu items */
        background: transparent;
        border-radius: 6px; /* Slightly rounded corners */
        margin: 2px 4px; /* Space between items */
        transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out; /* Smooth transitions */
    }

    QMenuBar::item:selected {
        background-color: #3c3c3c; /* Hover/selected background */
        color: #ffffff; /* Brighter text on hover */
    }

    QMenu {
        background-color: #2b2b2b;
        border: 1px solid #3c3c3c;
        border-radius: 8px; /* Rounded menu corners */
        padding: 8px; /* Padding inside the menu */
        box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.4); /* Subtle shadow for depth */
    }

    QMenu::item {
        padding: 10px 25px 10px 15px; /* Padding for menu dropdown items */
        background: transparent;
        border-radius: 5px; /* Rounded corners for items */
        margin: 2px 0; /* Vertical spacing between items */
        transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out;
    }

    QMenu::item:selected {
        background-color: #3c3c3c; /* Highlight on hover */
        color: #ffffff;
    }

    QMenu::separator {
        height: 1px;
        background-color: #3c3c3c;
        margin: 5px 10px; /* Space around separators */
        border-radius: 0;
    }

    /* --- QLabel Styling --- */
    QLabel {
        color: #e0e0e0;
        padding: 0; /* Labels typically don't need padding unless specified for layout */
        font-size: 13px; /* Slightly smaller font for general labels */
    }

    QLabel#titleLabel { /* For custom floating window title */
        font-weight: bold;
        font-size: 15px; /* Larger, bolder for titles */
        color: #ffffff;
    }

    /* --- QSlider Styling --- */
    QSlider::groove:horizontal {
        border: 1px solid #3c3c3c; /* Groove border */
        height: 8px;
        background: #2b2b2b; /* Background of the groove */
        margin: 2px 0;
        border-radius: 4px; /* Rounded groove */
    }

    QSlider::handle:horizontal {
        background: #6c5ce7; /* Accent color for the handle */
        border: 1px solid #7a6ceb; /* Slightly darker border for depth */
        width: 18px; /* Larger handle for easier interaction */
        height: 18px;
        margin: -6px 0; /* Vertically center the handle on the groove */
        border-radius: 9px; /* Perfect circle handle */
        transition: background-color 0.2s ease-in-out, border-color 0.2s ease-in-out, width 0.2s ease-in-out, height 0.2s ease-in-out;
    }

    QSlider::handle:horizontal:hover {
        background-color: #8c7ee9; /* Lighter accent on hover */
        border-color: #9b8ffb;
        width: 20px; /* Slightly larger on hover */
        height: 20px;
        margin: -7px 0; /* Adjust margin for larger handle */
    }

    QSlider::handle:horizontal:pressed {
        background-color: #5a4cc6; /* Darker accent on pressed */
        border-color: #6c5ce7;
    }

    QSlider::add-page:horizontal {
        background: #3c3c3c; /* Part of the groove that's not yet "filled" */
        border-radius: 4px;
    }

    QSlider::sub-page:horizontal {
        background: #6c5ce7; /* Filled part of the groove (accent color) */
        border-radius: 4px;
    }

    /* --- QPushButton Styling --- */
    QPushButton {
        background-color: #3c3c3c; /* Default button background */
        color: #e0e0e0; /* Default button text color */
        border: 1px solid #4f4f4f; /* Subtle border */
        border-radius: 8px; /* Rounded button corners */
        padding: 8px 15px; /* Comfortable padding */
        min-height: 28px; /* Minimum height for consistency */
        transition: background-color 0.2s ease-in-out, border-color 0.2s ease-in-out, color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    }

    QPushButton:hover {
        background-color: #4f4f4f; /* Lighter on hover */
        border-color: #5a5a5a;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.3); /* Subtle hover shadow */
    }

    QPushButton:pressed {
        background-color: #2b2b2b; /* Darker on pressed */
        border-color: #3c3c3c;
        box-shadow: none; /* Remove shadow on press */
    }

    /* Special styling for the floating window close button */
    QPushButton#FloatingCloseButton {
        background-color: #e74c3c; /* Red accent for close */
        color: #ffffff;
        border: none; /* No border for this button */
        border-radius: 10px; /* Perfect circle */
        width: 20px;
        height: 20px;
        padding: 0;
        font-weight: bold;
        font-size: 12px;
        transition: background-color 0.2s ease-in-out;
    }

    QPushButton#FloatingCloseButton:hover {
        background-color: #c0392b; /* Darker red on hover */
        box-shadow: none;
    }

    QPushButton#FloatingCloseButton:pressed {
        background-color: #a53023; /* Even darker red on pressed */
    }

    /* --- QDockWidget Styling --- */
    QDockWidget {
        border: 1px solid #3c3c3c;
        border-radius: 8px; /* Rounded corners for dock widgets */
    }

    QDockWidget::title {
        background-color: #2b2b2b;
        padding: 8px; /* Padding for the title bar */
        text-align: center;
        border-bottom: 1px solid #3c3c3c;
        border-top-left-radius: 7px; /* Match outer border radius -1px */
        border-top-right-radius: 7px;
        font-weight: bold;
    }

    /* --- QProgressDialog and QProgressBar Styling --- */
    QProgressDialog {
        background-color: #2b2b2b;
        color: #e0e0e0;
        border: 1px solid #3c3c3c;
        border-radius: 10px; /* More rounded dialog */
        padding: 15px; /* Inner padding */
        box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.5); /* Prominent shadow */
    }

    QProgressDialog QLabel {
        padding: 5px 0;
        font-size: 14px;
    }

    QProgressBar {
        border: 1px solid #3c3c3c;
        border-radius: 6px;
        text-align: center;
        background-color: #2b2b2b;
        color: #e0e0e0; /* Text color for percentage */
        height: 18px; /* Standard height */
    }

    QProgressBar::chunk {
        background-color: #2ecc71; /* Green for progress (success color) */
        border-radius: 5px; /* Rounded chunks */
        transition: background-color 0.2s ease-in-out; /* Subtle animation */
    }

    /* --- Custom Floating Window (QFrame and QWidget inside) --- */
    QFrame#FloatingControlsFrame {
        background-color: #2b2b2b; /* Slightly lighter background for the frame */
        border: 1px solid #3c3c3c;
        border-radius: 12px; /* Prominent rounded corners for the floating panel */
        box-shadow: 0px 8px 25px rgba(0, 0, 0, 0.6); /* Deeper shadow for "floating" effect */
        padding: 0; /* The layout inside will handle padding */
    }

    QWidget#FloatingTitleBar {
        background-color: #2b2b2b;
        border-top-left-radius: 11px; /* Match outer frame radius -1px */
        border-top-right-radius: 11px;
        padding: 8px 15px; /* Generous padding for title bar */
        border-bottom: 1px solid #3c3c3c; /* Separator below title */
    }
    """

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



