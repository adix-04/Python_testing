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
from rack_commands import Rack_main

class Main_rack_page(QWidget):
    def __init__(self):
        super().__init__()
        self.sig_use = pyqtSignal()
        self.rack = Rack_main()
        self.rack.rack_main()       
        self.page = self.main_page()
        # self.rack.mute()
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
        card.setStyleSheet("background-color: #302D2D; border-radius: 12px; padding: 2px;")
        vbox = QVBoxLayout()
        label = QLabel("Clamp Settings in devlopment🏗️🛠️")
        label.setStyleSheet(my_style)
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName("headers")
        vbox.addWidget(label)
        fHbox = QHBoxLayout()
        sHbox = QHBoxLayout()

        vbox.setAlignment(Qt.AlignCenter)
        vbox.setSpacing(10)

        self.browse_btn = QPushButton("Shut Down Clamps")
        self.browse_btn.setStyleSheet(my_style)
        self.browse_btn.setMinimumSize(100,100)
        self.browse_btn.clicked.connect(self.rack.func_stop_clamps)

        self.log_browse_btn = QPushButton("Start all Clamps")
        self.log_browse_btn.setStyleSheet(my_style)
        self.log_browse_btn.setMinimumSize(100,100)
        self.log_browse_btn.clicked.connect(self.rack.func_start_clamps)
    
        self.test_btn = QPushButton("start test")
        self.test_btn.setStyleSheet(my_style)
        self.test_btn.setMinimumSize(100,100)
        # self.test_btn.clicked.connect(self.rack.mute)
      
        schedule_btn = QPushButton("Schedule")
        schedule_btn.setStyleSheet(my_style)
        schedule_btn.setMinimumSize(100,100)
       

        fHbox.addWidget(self.browse_btn)
        fHbox.addWidget(self.log_browse_btn)

        sHbox.addWidget(self.test_btn)
        sHbox.addWidget(schedule_btn)

        vbox.addLayout(fHbox)
        vbox.addLayout(sHbox)

        card.setLayout(vbox)
        return card
  
    
   