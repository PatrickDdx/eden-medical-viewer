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

    open_image_action = QAction("Open Image" , window)
    open_image_action.triggered.connect(window.open_image_func)
    file_menu.addAction(open_image_action)

    file_menu.addSeparator()

    save_action = QAction("Save", window)
    save_action.triggered.connect(window.show_save_dialog)
    file_menu.addAction(save_action)

    file_menu.addSeparator()

    exit_action = QAction("Exit", window)
    exit_action.triggered.connect(window.close_application)
    file_menu.addAction(exit_action)

def _build_windowing_menu(window, menu):
    window_presets_menu = menu.addMenu("Windowing")

    for name in window.windowing_manager.window_presets:
        action = QAction(name, window)

        action.triggered.connect(lambda checked, n=name: window.viewer_widget.apply_window_preset(n))
        window_presets_menu.addAction(action)

    current_window = QAction("Current Window", window)
    current_window.triggered.connect(window.viewer_widget.get_current_window)
    window_presets_menu.addAction(current_window)

"""
def _build_ai_menu(window, menu):
    ai_menu = menu.addMenu("AI")

    load_action = QAction("Load Model", window)
    load_action.triggered.connect(window.load_ai_model)
    ai_menu.addAction(load_action)

    sam_action = QAction("Enable SAM", window)
    sam_action.setCheckable(True)
    sam_action.toggled.connect(window.viewer_widget.sam_handler.enable_sam)
    ai_menu.addAction(sam_action)
"""

def _build_view_menu(window, menu):
    view_menu = menu.addMenu("View")

    play_cine = QAction("Play/Stop cine", window)
    play_cine.triggered.connect(window.viewer_widget.cine_controller.toggle)
    view_menu.addAction(play_cine)

    faster_cine = QAction("Faster cine", window)
    faster_cine.triggered.connect(lambda _: window.viewer_widget.cine_controller.increase_speed())
    view_menu.addAction(faster_cine)

    slower_cine = QAction("Slower cine", window)
    slower_cine.triggered.connect(lambda _: window.viewer_widget.cine_controller.decrease_speed())
    view_menu.addAction(slower_cine)

def _build_tools_menu(window, menu):
    tools_menu = menu.addMenu("Tools")

    toggle_floating_controls = QAction("Floating Controls", window)
    toggle_floating_controls.triggered.connect(lambda x: window.toggle_floating_controls(True))
    tools_menu.addAction(toggle_floating_controls)

    window.measure_action = QAction("Measure", window)
    window.measure_action.setCheckable(True)
    window.measure_action.toggled.connect(window.viewer_widget.measure_handler.enable_measure)
    tools_menu.addAction(window.measure_action)

    delete_measurements_action = QAction("Delete Measurements", window)
    delete_measurements_action.triggered.connect(window.viewer_widget.measure_handler.delete_all_measurements)
    tools_menu.addAction(delete_measurements_action)
