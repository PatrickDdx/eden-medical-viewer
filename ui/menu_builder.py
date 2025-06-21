from PyQt6.QtGui import QAction

def _build_file_menu(window, menu):
    """Constructs the File menu"""
    file_menu = menu.addMenu("File")

    open_dicom_action = QAction("Open DICOM", window)
    open_dicom_action.triggered.connect(window.open_dicom_file_func)
    file_menu.addAction(open_dicom_action)

    open_nifti_action = QAction("Open NIfTI", window)
    open_nifti_action.triggered.connect(window.open_nifti_func)
    file_menu.addAction(open_nifti_action)

    exit_action = QAction("Exit", window)
    exit_action.triggered.connect(window.close_application)
    file_menu.addAction(exit_action)

    file_menu.addSeparator()

    save_action = QAction("Save", window)
    save_action.triggered.connect(window.show_save_dialog)
    file_menu.addAction(save_action)

def _build_windowing_menu(window, menu):
    window_presets_menu = menu.addMenu("Windowing")

    for name in window.windowing_manager.window_presets:
        action = QAction(name, window)

        action.triggered.connect(lambda checked, n=name: window.viewer_widget.apply_window_preset(n))
        window_presets_menu.addAction(action)

    current_window = QAction("Current Window", window)
    current_window.triggered.connect(window.viewer_widget.get_current_window)
    window_presets_menu.addAction(current_window)

def _build_ai_menu(window, menu):
    ai_menu = menu.addMenu("AI")

    load_action = QAction("Load Model", window)
    load_action.triggered.connect(window.load_ai_model)
    ai_menu.addAction(load_action)

def _build_view_menu(window, menu):
    view_menu = menu.addMenu("View")

    play_cine = QAction("Play/Stop cine", window)
    play_cine.triggered.connect(window.viewer_widget.toggle_cine_loop)
    view_menu.addAction(play_cine)

    faster_cine = QAction("Faster cine", window)
    faster_cine.triggered.connect(window.viewer_widget.increase_cine_speed)
    view_menu.addAction(faster_cine)

    slower_cine = QAction("Slower cine", window)
    slower_cine.triggered.connect(window.viewer_widget.decrease_cine_speed)
    view_menu.addAction(slower_cine)

def _build_tools_menu(window, menu):
    tools_menu = menu.addMenu("Tools")

    toggle_floating_controls = QAction("Floating Controls", window)
    toggle_floating_controls.triggered.connect(lambda x: window.toggle_floating_controls(True))
    tools_menu.addAction(toggle_floating_controls)

def _build_help_menu(window, menu):
    help_menu = menu.addMenu("Help")