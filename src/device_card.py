from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QPainter,QFont,QPixmap,QPainterPath
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal



class DeviceCard(QWidget):
    config_signal = pyqtSignal(dict)
    use_signal = pyqtSignal(dict)

    def __init__(self, device):
        super().__init__()
        self.device = device

        # === Dark themed style ===
        self.setStyleSheet("""
            QWidget {
                border: 1px ;
                border-radius: 5px;
                background: transparent;
            }
            QLabel {
                color: black;
            }
            QPushButton {
                padding: 6px 12px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton#primary {
                background-color: #007ACC;
                color: white;
            }
            QPushButton#primary:hover { background-color: #005A99; }
            QPushButton#primary:pressed { background-color: #2E7D32; }

            QPushButton#secondary {
                background-color: #007ACC;
                color: white;
            }
            QPushButton#secondary:hover { background-color: #005A99; }
            QPushButton#secondary:pressed { background-color: #005A99; }
        """)

        # self.setFixedSize(240, 320)

       
        image = QLabel(self)
        pixmap = QPixmap('src/assets/download.png')
        image.setPixmap(pixmap)
        image.setFixedSize(250, 120)
       

        # === Device Title ===
        title = QLabel(device["name"])
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        # === Device Info ===
        info = QLabel(device["ip"])
        info.setStyleSheet("color: #000000; font-size: 12px; font-weight : bold")
        info.setAlignment(Qt.AlignCenter)

        # === Buttons ===
        btn_use = QPushButton("Use")
        btn_use.setObjectName("primary")
        btn_use.clicked.connect(self.emit_use)

        btn_config = QPushButton("Configure")
        btn_config.setObjectName("secondary")
        btn_config.clicked.connect(self.emit_config)

        btns = QHBoxLayout()
        btns.addStretch()
        btns.addWidget(btn_use)
        btns.addWidget(btn_config)
        btns.addStretch()

        # === Layout ===
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(image, alignment=Qt.AlignCenter)
        layout.addSpacing(8)
        layout.addWidget(title)
        layout.addWidget(info)
        layout.addSpacing(12)
        layout.addLayout(btns)
        layout.addStretch()
        self.setLayout(layout)

    def emit_config(self):
        self.config_signal.emit(self.device)

    def emit_use(self):
        self.use_signal.emit(self.device)
