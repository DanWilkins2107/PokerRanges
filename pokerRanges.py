import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QGridLayout, QHBoxLayout, QComboBox, QInputDialog, QColorDialog, QMessageBox
from PyQt5.QtGui import QPalette, QLinearGradient, QBrush, QColor, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QPoint
from gridLabel import GridLabel
from data import Data

class RangeMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.data = Data()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Range Tester')
        self.setGeometry(100, 100, 1200, 600)

        main_layout = QHBoxLayout()

        layout = QVBoxLayout()

        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(173, 216, 230))  # light blue
        gradient.setColorAt(1.0, QColor(150, 200, 220))  # slightly darker light blue
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        title_font = QFont("Roboto", 24)
        title_font.setBold(True)
        self.title = QLabel('LEARN YOUR RANGES', self)
        self.title.setFont(title_font)
        self.title.setAlignment(Qt.AlignCenter)  # center the text
        layout.addWidget(self.title)

        self.frame = QFrame(self)
        self.frame.setStyleSheet("background-color: transparent;")

        frame_layout = QVBoxLayout()

        self.edit_button = QPushButton('Edit Ranges', self)
        self.edit_button.clicked.connect(self.editRanges)
        self.edit_button.setStyleSheet("background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #0095ff, stop: 1 #0066ff); border: 1px solid black; border-radius: 10px; font-size: 20px; font-weight: bold; padding: 10px;")
        frame_layout.addWidget(self.edit_button)

        self.test_button = QPushButton('Test Ranges', self)
        self.test_button.clicked.connect(self.testRanges)
        self.test_button.setStyleSheet("background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #0095ff, stop: 1 #0066ff); border: 1px solid black; border-radius: 10px; font-size: 20px; font-weight: bold; padding: 10px;")
        frame_layout.addWidget(self.test_button)

        self.frame.setLayout(frame_layout)
        layout.addWidget(self.frame)

        self.Values = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

        self.grid_frame = QFrame(self)
        self.grid_frame.setStyleSheet("background-color: transparent;")
        self.grid_frame.hide()

        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)

        self.last_widget = None
        self.clicked_widget = None

        self.labels = []
        for i in range(len(self.Values)):
            row = []
            for j in range(len(self.Values)):
                if i == j:
                    label = GridLabel(self.Values[i] + self.Values[j], self)
                elif i < j:
                    label = GridLabel(self.Values[i] + self.Values[j] + 's', self)
                else:
                    label = GridLabel(self.Values[j] + self.Values[i] + 'o', self)
                label.setAlignment(Qt.AlignCenter)
                grid_layout.addWidget(label, i, j)
                row.append(label)
            self.labels.append(row)

        self.grid_frame.setLayout(grid_layout)
        layout.addWidget(self.grid_frame)

        self.sidebar_frame = QFrame(self)
        self.sidebar_frame.setStyleSheet("background-color: white; border: 1px solid black;")
        self.sidebar_frame.setFixedWidth(200)
        self.sidebar_frame.hide()

        sidebar_layout = QVBoxLayout()

        self.stack_size_combo = QComboBox(self)
        self.stack_size_combo.currentTextChanged.connect(self.stackSizeChanged)
        sidebar_layout.addWidget(self.stack_size_combo)

        self.label_combo = QComboBox(self)
        self.label_combo.currentTextChanged.connect(self.labelChanged)
        sidebar_layout.addWidget(self.label_combo)

        self.add_stack_size_button = QPushButton('Add Stack Size', self)
        self.add_stack_size_button.clicked.connect(self.addStackSize)
        sidebar_layout.addWidget(self.add_stack_size_button)

        self.remove_stack_size_button = QPushButton('Remove Stack Size', self)
        self.remove_stack_size_button.clicked.connect(self.removeStackSize)
        sidebar_layout.addWidget(self.remove_stack_size_button)

        self.add_label_button = QPushButton('Add Label', self)
        self.add_label_button.clicked.connect(self.addLabel)
        sidebar_layout.addWidget(self.add_label_button)

        self.remove_label_button = QPushButton('Remove Label', self)
        self.remove_label_button.clicked.connect(self.removeLabel)
        sidebar_layout.addWidget(self.remove_label_button)

        self.sidebar_frame.setLayout(sidebar_layout)

        main_layout.addLayout(layout)
        main_layout.addWidget(self.sidebar_frame)

        self.setLayout(main_layout)

    def editRanges(self):
        self.title.hide()
        self.frame.hide()
        self.grid_frame.show()
        self.sidebar_frame.show()

    def testRanges(self):
        self.title.hide()
        self.frame.hide()
        print('Test Ranges clicked')

    def stackSizeChanged(self, text):
        self.data.setCurrentStackSize(text)
        self.updateLabels()

    def labelChanged(self, text):
        self.data.setCurrentLabel(text)

    def addStackSize(self):
        text, ok = QInputDialog.getText(self, 'Add Stack Size', 'Enter new stack size:')
        if ok and text:
            self.data.addStackSize(text)
            self.stack_size_combo.addItem(text)

    def removeStackSize(self):
        if self.data.getCurrentStackSize():
            self.data.removeStackSize(self.data.getCurrentStackSize())
            self.stack_size_combo.removeItem(self.stack_size_combo.currentIndex())

    def addLabel(self):
        if self.data.getCurrentStackSize():
            text, ok = QInputDialog.getText(self, 'Add Label', 'Enter new label:')
            if ok and text:
                self.data.addLabel(text)
                self.updateLabels()
        else:
            QMessageBox.warning(self, 'Error', 'Please select a stack size first.')

    def removeLabel(self):
        if self.data.getCurrentLabel():
            self.data.removeLabel(self.data.getCurrentLabel())
            self.updateLabels()

    def updateLabels(self):
        self.label_combo.clear()
        for label in self.data.getLabels():
            self.label_combo.addItem(label)
            label_layout = QHBoxLayout()
            label_button = QPushButton(label, self)
            label_button.clicked.connect(lambda checked, label=label: self.selectColor(label))
            label_layout.addWidget(label_button)
            self.label_layout.addLayout(label_layout)

    def selectColor(self, label):
        color = QColorDialog.getColor()
        if color.isValid():
            self.data.setLabelColor(label, color.name())
            print(self.data.getHighlightedHands())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont('Roboto-Regular.ttf')  # load the Roboto font
    ex = RangeMenu()
    ex.show()
    sys.exit(app.exec_())