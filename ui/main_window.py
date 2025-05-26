from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt6.QtGui import QAction
import sys

from ui.viewer_widget import ViewerWidget


class UIMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EDEN")

        self.setupUI()
        self.setupMenuBar()
        self.create_central_widget() #Main display area

    def setupUI(self):
        self.setGeometry(110,62,1700,956) #(Xpos, Ypos, width, height)
        self.setMinimumSize(800,600)

    def create_central_widget(self):
        self.viewer_widget = ViewerWidget()
        self.setCentralWidget(self.viewer_widget)

    def setupMenuBar(self):
        menu = self.menuBar()

        #---------------------------------
        #creatin a menu dummy:
        dummy_menu = menu.addMenu("dummy")

        dummy_action = QAction("dummy action", self)
        dummy_action.triggered.connect(self.dummy_func)
        dummy_menu.addAction(dummy_action)

        #----------------------------


        # File Menu
        file_menu = menu.addMenu("File")

        open_action = QAction("Open DICOM", self)
        open_action.triggered.connect(self.open_dicom_file_func)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As", self)
        save_as_action.triggered.connect(self.save_as_func)
        file_menu.addAction(save_as_action)

        exit_action = QAction("Exit", self)
        file_menu.addAction(exit_action)

        #V View Menu
        view_menu = menu.addMenu("View")

        # AI Menu
        ai_menu = menu.addMenu("AI")

        load_action = QAction("Load Model", self)
        load_action.triggered.connect(self.load_ai_model)
        ai_menu.addAction(load_action)

        help_menu = menu.addMenu("Help")

    #-------------- Events -----------------------
    def dummy_func(self):
        print("dummy function clicked")

    #---------------------
    def open_dicom_file_func(self):
        print("open DICOM file clicked")
        file_path, _ = QFileDialog.getOpenFileName(self, "Open DICOM File", "", "DICOM Files (*.dcm);;All Files (*)")
        if file_path:
            print(f"open: {file_path}")

    def save_as_func(self):
        print("Save as clicked")

    def load_ai_model(self):
        model_path, _ = QFileDialog.getOpenFileName(self, "Load AI Model", "", "Model Files (*.h5 *pth *pkl *onnx *pb *tflite *keras *joblib *pmml);;All Files (*)")
        if model_path:
            print(f"loading following model: {model_path}")