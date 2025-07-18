from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QPainter,QFont,QPixmap,QPainterPath
from PyQt5.QtCore import Qt
import json
from PyQt5.QtCore import pyqtSignal
import Test_runner_GUI


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
                border-radius:100px;
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
        def make_round_pixmap(pixmap):
            size = min(pixmap.width(), pixmap.height())
            cropped = pixmap.scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        
            rounded = QPixmap(size, size)
            rounded.fill(Qt.transparent)

            path = QPainterPath()
            path.addEllipse(0, 0, size, size)

            painter = QPainter(rounded)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, cropped)
            painter.end()

            return rounded

# Apply to QLabel
        image = QLabel(self)
        pixmap = QPixmap('src/assets/download.png')
        round_pixmap = make_round_pixmap(pixmap)
        image.setPixmap(round_pixmap)
        image.setScaledContents(True)
        # Device Title
        # image = QLabel(self)
        # pixmap = QPixmap('src/assets/download.jpg')
        # image.setPixmap(pixmap)
        # image.setScaledContents(True)
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
        # print("emitting config signal")
        self.config_signal.emit(self.device)
    def emit_use(self):
        # print("emitting use signal")
        self.use_signal.emit(self.device)