from pdf_manager import Pdf_manager

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QCheckBox, QFileDialog, QLineEdit, QGridLayout, QProgressBar, QLabel

class pdfui(QWidget):

    def __init__(self):
        super().__init__()

        self.front_edit = QLineEdit()
        self.back_edit = QLineEdit()
        self.out_edit = QLineEdit()
        self.remove_blank = QCheckBox()
        self.status = QLabel()
        self.merge_button = QPushButton("Merge")

        self.bar = QProgressBar()

        self.initUI()


    def initUI(self):   
        grid = QGridLayout()  
        self.setLayout(grid)

        label = QLabel("Front")
        grid.addWidget(label, 0, 0)
        grid.addWidget(self.front_edit, 0, 1)
        button = QPushButton("...")
        button.clicked.connect(self.select_front)
        grid.addWidget(button, 0, 2)

        label = QLabel("Back")
        grid.addWidget(label, 1, 0)
        grid.addWidget(self.back_edit, 1, 1)
        button = QPushButton("...")
        button.clicked.connect(self.select_back)
        grid.addWidget(button, 1, 2)
        
        label = QLabel("Output")
        grid.addWidget(label, 2, 0)
        grid.addWidget(self.out_edit, 2, 1)

        label = QLabel("Remove blank pages")
        grid.addWidget(label, 3, 0)
        grid.addWidget(self.remove_blank, 3, 1)

        
        grid.addWidget(self.status, 4, 0, 1, 3)

        grid.addWidget(self.bar, 5, 0, 1, 2)
        self.merge_button.clicked.connect(self.mergepdf)
        grid.addWidget(self.merge_button, 5, 2) 

    #    self.move(300, 150)
        self.setWindowTitle('Pdf-merger')  
        self.show()

    def mergepdf(self):
        self.merge_button.setEnabled(False)
        self.status.setText("")
        pdf_manager = Pdf_manager(self.front_edit.text(), self.back_edit.text(), self.out_edit.text(), self.remove_blank.isChecked())
        pdf_manager._signal.connect(self.setProgress)
        self.status.setText( pdf_manager.mergepdf())
        self.merge_button.setEnabled(True)

    def setProgress(self, msg):
        self.bar.setValue(int(msg))

    def select_front(self):
        stri = QFileDialog.getOpenFileName(filter=("Pdf Files (*.pdf)"))
        self.front_edit.setText(stri[0])
        self.out_edit.setText(stri[0].replace(".pdf", "-merged.pdf"))
        self.bar.setValue(0)
        self.status.setText("")

    def select_back(self):
        stri = QFileDialog.getOpenFileName(filter=("Pdf Files (*.pdf)"))
        self.back_edit.setText(stri[0])
        self.bar.setValue(0)
        self.status.setText("")
    