import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFileDialog, QComboBox, QRadioButton, QButtonGroup
)
from PyQt5.QtGui import QIcon


class IPATestUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IPA Test Automation Runner")
        self.setGeometry(200, 200, 520, 380)

        self.ip = ""
        self.excel_file = ""
        self.config_file = ""
        self.tech = "BCA"
        self.system_load = False
        self.iterations = 1

        self.timenow = datetime.now()
        self.rundirectoryname = "IPA_Testrun_" + self.timenow.strftime("%d_%m_%H_%M")
        self.rundirectory = ""

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(8)

        # IP Address
        ip_label = QLabel("IP Address:")
        self.ip_entry = QLineEdit()
        layout.addWidget(ip_label)
        layout.addWidget(self.ip_entry)

        # Excel File
        excel_label = QLabel("Excel File:")
        excel_layout = QHBoxLayout()
        self.excel_entry = QLineEdit()
        excel_button = QPushButton("Browse")
        excel_button.clicked.connect(self.browse_excel)
        excel_layout.addWidget(self.excel_entry)
        excel_layout.addWidget(excel_button)
        layout.addWidget(excel_label)
        layout.addLayout(excel_layout)

        # Config File
        config_label = QLabel("Configuration File:")
        config_layout = QHBoxLayout()
        self.config_entry = QLineEdit()
        config_button = QPushButton("Browse")
        config_button.clicked.connect(self.browse_config)
        config_layout.addWidget(self.config_entry)
        config_layout.addWidget(config_button)
        layout.addWidget(config_label)
        layout.addLayout(config_layout)

        # Tech Stack dropdown
        tech_label = QLabel("Tech Stack:")
        self.tech_combo = QComboBox()
        self.tech_combo.addItems(["BCA", "Cerence"])
        tech_layout = QHBoxLayout()
        tech_layout.addWidget(tech_label)
        tech_layout.addWidget(self.tech_combo)
        layout.addLayout(tech_layout)

        # System Load radio
        sysload_label = QLabel("Give System Load?")
        sysload_layout = QHBoxLayout()
        self.radio_yes = QRadioButton("Yes")
        self.radio_no = QRadioButton("No")
        self.radio_no.setChecked(True)
        sysload_group = QButtonGroup(self)
        sysload_group.addButton(self.radio_yes)
        sysload_group.addButton(self.radio_no)
        sysload_layout.addWidget(self.radio_yes)
        sysload_layout.addWidget(self.radio_no)
        layout.addWidget(sysload_label)
        layout.addLayout(sysload_layout)

        # Iterations dropdown
        iter_layout = QHBoxLayout()
        iter_label = QLabel("Iteration Count:")
        self.iter_combo = QComboBox()
        self.iter_combo.addItems([str(i) for i in range(1, 6)])
        iter_layout.addWidget(iter_label)
        iter_layout.addWidget(self.iter_combo)
        layout.addLayout(iter_layout)

        # Start Button
        start_button = QPushButton("Start Test")
        start_button.clicked.connect(self.start_test)
        layout.addWidget(start_button)

        # Status labels
        self.status_total = QLabel("Total / Played: 0 / 0")
        self.status_current = QLabel("Current Utterance: None")
        layout.addWidget(self.status_total)
        layout.addWidget(self.status_current)

        self.setLayout(layout)

    def browse_excel(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx *.xls)")
        if file_name:
            self.excel_entry.setText(file_name)
            self.excel_file = file_name

    def browse_config(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Configuration File", "", "All Files (*)")
        if file_name:
            self.config_entry.setText(file_name)
            self.config_file = file_name

    def update_status(self, total_played_text=None, current_utterance_text=None, error=False):
        if total_played_text is not None:
            self.status_total.setText(total_played_text)
        if current_utterance_text is not None:
            self.status_current.setText(current_utterance_text)

    def start_test(self):
        self.ip = self.ip_entry.text().strip()
        self.excel_file = self.excel_entry.text().strip()
        self.config_file = self.config_entry.text().strip()
        self.tech = self.tech_combo.currentText()
        self.system_load = self.radio_yes.isChecked()
        self.iterations = int(self.iter_combo.currentText())

        print(f"IP: {self.ip}")
        print(f"Excel: {self.excel_file}")
        print(f"Config: {self.config_file}")
        print(f"Tech Stack: {self.tech}")
        print(f"System Load: {self.system_load}")
        print(f"Iterations: {self.iterations}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = IPATestUI()
    win.show()
    sys.exit(app.exec_())
