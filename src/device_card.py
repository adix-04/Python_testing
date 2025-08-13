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

        # === Dark themed style ===
        self.setStyleSheet("""
            QWidget {
                border: 1px solid #444;
                border-radius: 12px;
                background-color: #2b2b2b;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                padding: 6px 12px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton#primary {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#primary:hover { background-color: #45A049; }
            QPushButton#primary:pressed { background-color: #2E7D32; }

            QPushButton#secondary {
                background-color: #555;
                color: white;
            }
            QPushButton#secondary:hover { background-color: #666; }
            QPushButton#secondary:pressed { background-color: #444; }
        """)

        self.setFixedSize(240, 320)

        # === Helper to make round pixmap ===
        def make_round_pixmap(pixmap):
            size = min(pixmap.width(), pixmap.height())

            # Center crop manually
            x = (pixmap.width() - size) // 2
            y = (pixmap.height() - size) // 2
            cropped = pixmap.copy(x, y, size, size)
            cropped = cropped.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

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

        # === Image ===
        image = QLabel(self)
        pixmap = QPixmap('src/assets/download.png')
        round_pixmap = make_round_pixmap(pixmap)
        image.setPixmap(round_pixmap)
        image.setFixedSize(120, 120)
        image.setAlignment(Qt.AlignCenter)

        # === Device Title ===
        title = QLabel(device["name"])
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        # === Device Info ===
        info = QLabel(device["ip"])
        info.setStyleSheet("color: #bbb; font-size: 12px;")
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
