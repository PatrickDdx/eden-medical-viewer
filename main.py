import sys
import warnings

from PyQt6.QtWidgets import QApplication
import pydicom

from ui.main_window import MainWindow
from ui.stylesheets import dark_theme_global_4

# Filter out the specific UserWarning from pydicom.valuerep related to invalid UI values
# The message pattern is crucial here.
# You might need to adjust the message string slightly if it changes in future pydicom versions.
warnings.filterwarnings(
    "ignore",
    message="Invalid value for VR UI: '.*'. Please see .* for allowed values for each VR.",
    category=UserWarning,
    module='pydicom.valuerep' # Specify the module where the warning originates
)

def main():
    app = QApplication(sys.argv)

    #Style
    app.setStyleSheet(dark_theme_global_4())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
