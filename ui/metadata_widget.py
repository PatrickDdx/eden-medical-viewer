# ui/metadata_viewer.py
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget, QVBoxLayout

class DicomMetadataViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Name", "Value"])
        self.tree.setColumnCount(2)
        self.tree.setAlternatingRowColors(True)

        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        layout.addStretch()  #stays at the top of the screen
        self.setLayout(layout)

    def display_metadata(self, metadata: dict):
        """Displays the key-value metadata dictionary"""
        self.tree.clear()

        for key,value in metadata.items():
            item = QTreeWidgetItem([str(key), str(value)])
            self.tree.addTopLevelItem(item)

        self.adjust_height_simple()

    def extract_and_display_metadata(self, dicom_dataset):
        """expects a dicom dataset and extracts ALL the metadata and displays in a tree"""
        self.tree.clear()

        for elem in dicom_dataset:
            if elem.VR == "SQ":  # Handle sequences
                parent = QTreeWidgetItem([elem.name, "Sequence"])
                self.tree.addTopLevelItem(parent)
                for i, item in enumerate(elem.value):
                    item_node = QTreeWidgetItem([f"Item {i}", "", ""])
                    parent.addChild(item_node)
                    for sub_elem in item:
                        sub_item = QTreeWidgetItem([sub_elem.name, str(sub_elem.value)])
                        item_node.addChild(sub_item)
            else:
                item = QTreeWidgetItem([elem.name, str(elem.value)])
                self.tree.addTopLevelItem(item)

    def adjust_height_simple(self):
        row_count = self.tree.topLevelItemCount()
        if row_count == 0:
            self.tree.setFixedHeight(100)  # or some minimum
            return

        row_height = self.tree.sizeHintForRow(0)
        header_height = self.tree.header().height()
        new_height = header_height + (row_count * row_height) + 2  # +2 for borders

        self.tree.setFixedHeight(new_height)

