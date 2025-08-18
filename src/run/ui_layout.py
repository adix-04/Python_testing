from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QTimer
import pandas as pd


class UILayout(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.status_label = QLabel("Time Remaining: 0s")
        self.start_btn = QPushButton("Start Task")

        self.start_btn.clicked.connect(self.start_task)

        layout.addWidget(self.status_label)
        layout.addWidget(self.start_btn)
        self.setLayout(layout)

        self.remaining_seconds = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

    def start_task(self):
        # --- Here we calculate load_time directly ---
        excel_path = "C:/Users/Adin N S/Downloads/WuW_less_with_NAV.xlsx"
        try:
            df = pd.read_excel(excel_path)
            self.remaining_seconds = df.size * 15   # <-- your formula
        except Exception as e:
            print("Excel read failed:", e)
            self.remaining_seconds = 10  # fallback

        # Start countdown
        self.status_label.setText(f"Time Remaining: {self.remaining_seconds}s")
        self.timer.start(1000)

    def update_timer(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.status_label.setText(f"Time Remaining: {self.remaining_seconds}s")
        else:
            self.timer.stop()
            self.status_label.setText("Task Completed ✅")
