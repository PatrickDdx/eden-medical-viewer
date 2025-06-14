# ui/metadata_viewer.py
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget, QVBoxLayout, QHeaderView, QSizePolicy, QScrollArea
from PyQt6.QtCore import QSize

class DicomMetadataViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Name", "Value"])
        self.tree.setColumnCount(2)
        self.tree.setAlternatingRowColors(True)
        self.tree.setIndentation(16)
        self.tree.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.tree.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        layout.addStretch()  #stays at the top of the screen
        layout.setContentsMargins(12, 12, 12, 12)  # left, top, right, bottom
        layout.setSpacing(8)  # space between widgets

        self.setLayout(layout)

        #self.setMinimumWidth(300)

        self.tree.setStyleSheet("""
            QTreeWidget {
                background-color: #1e1e1e;
                alternate-background-color: #2a2a2a;
                color: #e0e0e0;
                border: 1px solid #3c3c3c;
                border-radius: 8px;
                font-family: -apple-system, "SF Pro", "Helvetica Neue", Arial, sans-serif;
                font-size: 13px;
            }

            QTreeWidget::item {
                padding: 6px 8px;
                selection-background-color: #3a7bd5;
                selection-color: #ffffff;
            }

            QTreeView::branch:has-children:!has-siblings:closed,
            QTreeView::branch:closed:has-children:has-siblings {
                border-image: none;
                image: url(:/icons/arrow-right-dark.png);  /* optional: use minimal arrow icons */
            }

            QTreeView::branch:open:has-children:!has-siblings,
            QTreeView::branch:open:has-children:has-siblings {
                border-image: none;
                image: url(:/icons/arrow-down-dark.png);
            }

            QHeaderView::section {
                background-color: #2e2e2e;
                color: #bbbbbb;
                padding: 6px;
                font-weight: 500;
                border: none;
            }

            QScrollBar:vertical {
                background: #1e1e1e;
                width: 12px;
                margin: 0px 0px 0px 0px;
            }

            QScrollBar::handle:vertical {
                background: #555;
                min-height: 20px;
                border-radius: 6px;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }

            QScrollBar::handle:vertical:hover {
                background: #777;
            }
        """)

    def display_metadata(self, metadata: dict):
        """Displays the key-value metadata dictionary"""
        self.tree.clear()

        for key,value in metadata.items():
            item = QTreeWidgetItem([str(key), str(value)])
            self.tree.addTopLevelItem(item)

        #self.adjust_height_simple()

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

    def sizeHint(self):
        return QSize(300,300)

