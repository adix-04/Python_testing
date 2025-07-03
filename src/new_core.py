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
from styles import *
class Main_utils_page(QWidget):
    def __init__(self):
        super().__init__()
        self.sig_use = pyqtSignal()
        self.page = self.main_page()
       
    def main_page(self):
        page = QWidget()
        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        
        # List of EXE paths and names
        exe_paths = [
            "C:/path/to/app1.exe", "C:/path/to/app2.exe", "C:/path/to/app3.exe",
            "C:/path/to/app4.exe", "C:/path/to/app5.exe", "C:/path/to/app6.exe"
        ]

        for i in range(6):
            card = QFrame()
            card.setFrameShape(QFrame.StyledPanel)
            card.setStyleSheet("background-color: #272757; border-radius: 12px; padding: 10px;")
            vbox = QVBoxLayout()
            label = QLabel(f"App {i+1}")
            label.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
            label.setAlignment(Qt.AlignCenter)
            exe_input = QLineEdit()
            exe_input.setPlaceholderText("Enter .exe file path for test")
            exe_input.setStyleSheet(my_style)

            time_input =  QLineEdit()
            time_input.setPlaceholderText("HH:MM format(eg 14:30)")
            time_input.setStyleSheet(my_style)
            run_btn = QPushButton("Run")
            run_btn.setStyleSheet("padding: 6px; background-color: #4CAF50; color: white; border-radius: 6px;")
            run_btn.clicked.connect(lambda _, path=exe_paths[i]: self.run_exe(path))
            vbox.addWidget(label)
            vbox.addWidget(exe_input)
            vbox.addWidget(time_input)
            vbox.addWidget(run_btn)
            card.setLayout(vbox)
            row = i // 3
            col = i % 3
            grid_layout.addWidget(card, row, col)

        main_layout.addLayout(grid_layout)
        page.setLayout(main_layout)
        return page



