from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QLineEdit, QTextEdit,
    QFrame, QScrollArea,QSizePolicy,QGridLayout,QFileDialog,QMessageBox,QComboBox
)
from PyQt5.QtGui import QIcon,QFont,QPixmap,QMovie
from PyQt5.QtCore import Qt
import json
from PyQt5.QtCore import pyqtSignal
import new_ui

class Main_utils_page(QWidget):
    def __init__(self):
        super().__init__()
        self.sig_use = pyqtSignal()
        self.page = QWidget()
    def main_page(self):
        self.ui = new_ui.Ui_MainWindow()
        page = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        top_half = QWidget()
        top_layout = QHBoxLayout()
        self.label = QLabel("Input Custom Words to Speak")
        top_layout.addWidget(self.label)

        bottom_half = QWidget()
        bottom_layout = QHBoxLayout() 
        self.label = QLabel("Input Custom Words to Speak")
        bottom_layout.addWidget(self.label)

        top_half.setLayout(top_layout)
        bottom_half.setLayout(bottom_layout)
        main_layout.addWidget(top_half,1)
        main_layout.addWidget(bottom_half,1)
        page.setLayout(main_layout)
        self.ui.stackedWidget.addWidget(page)
        self.ui.stackedWidget.setCurrentWidget(page)
        return page


