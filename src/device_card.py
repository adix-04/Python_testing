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


class DeviceCard(QWidget):
    config_signal = pyqtSignal(dict)
    use_signal = pyqtSignal(dict)
    def __init__(self, device):
        super().__init__()
        self.device = device
        self.sig = pyqtSignal()

        self.setStyleSheet("""
            QWidget {
                border: 1px solid #ccc;
                border-radius: 10px;
                background-color: #fefefe;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton#primary {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#secondary {
                background-color: #e0e0e0;
                color: black;
            }
        """)
        self.setFixedSize(240, 320)

        # Device Title
        image = QLabel(self)
        pixmap = QPixmap('src/assets/download.png')
        image.setPixmap(pixmap)
        image.setScaledContents(True)
        title = QLabel(device["name"])
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        # Device Info
        info = QLabel(device["ip"])
        info.setAlignment(Qt.AlignCenter)
        # Buttons
        btn_use = QPushButton("Use")
        btn_use.setObjectName("primary")
        btn_use.clicked.connect(self.emit_use)
        btn_config = QPushButton("Configure")
        btn_config.setObjectName("secondary")
        btn_config.clicked.connect(self.emit_config)
    
        btns = QHBoxLayout()
        btns.addWidget(btn_use)
        btns.addWidget(btn_config)
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(image)
        layout.addWidget(title)
        layout.addWidget(info)
        layout.addLayout(btns)
        layout.addStretch()
        self.setLayout(layout)
    def emit_config(self):
        print("emitting config signal")
        self.config_signal.emit(self.device)
    def emit_use(self):
        print("emitting use signal")
        self.use_signal.emit(self.device)