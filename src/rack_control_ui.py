from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QLineEdit, QTextEdit,
    QFrame, QScrollArea,QSizePolicy,QGridLayout,QFileDialog,QMessageBox,QComboBox
)
from PyQt5.QtGui import QIcon,QFont,QPixmap,QMovie
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from styles import *
from t import Rack_main

class Main_rack_page(QWidget):
    def __init__(self):
        super().__init__()
        self.sig_use = pyqtSignal()
        self.rack = Rack_main()
        self.rack.rack_main()       
        self.page = self.main_page()
    def main_page(self):
        page = self.create_card()
        main_layout = QHBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(page)
        page.setLayout(main_layout)
        return page 
       
    
    def create_card(self):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("background-color: #272757; border-radius: 12px; padding: 2px;")
        vbox = QVBoxLayout()
        fHbox = QHBoxLayout()
        sHbox = QHBoxLayout()

        vbox.setAlignment(Qt.AlignCenter)
        vbox.setSpacing(10)

        browse_btn = QPushButton("Shut Down Clamps")
        browse_btn.setStyleSheet(my_style)
        browse_btn.setMinimumSize(100,100)
        browse_btn.clicked.connect(self.rack.func_stop_clamps)

        log_browse_btn = QPushButton("Start all Clamps")
        log_browse_btn.setStyleSheet(my_style)
        log_browse_btn.setMinimumSize(100,100)
        log_browse_btn.clicked.connect(self.rack.func_start_clamps)
    
        test_btn = QPushButton("start test")
        test_btn.setStyleSheet(my_style)
        test_btn.setMinimumSize(100,100)
      
        schedule_btn = QPushButton("Schedule")
        schedule_btn.setStyleSheet(my_style)
        schedule_btn.setMinimumSize(100,100)
       

        fHbox.addWidget(browse_btn)
        fHbox.addWidget(log_browse_btn)

        sHbox.addWidget(test_btn)
        sHbox.addWidget(schedule_btn)

        vbox.addLayout(fHbox)
        vbox.addLayout(sHbox)

        card.setLayout(vbox)
        return card
  
    
   