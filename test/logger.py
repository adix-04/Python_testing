import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFileDialog, QComboBox, QRadioButton, QButtonGroup
)
from PyQt5.QtGui import QIcon
from datetime import datetime


class IPATestUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IPA Test Automation Runner")
        self.setWindowIcon(QIcon(":/icons/IAV_Logo.ico"))
        self.setGeometry(200, 200, 500, 350)

        # Store values
        self.ip = ""
        self.excel_file = ""
        self.config_file = ""
        self.system_load = False
        self.iterations = 1

        # Timestamped run directory
        self.timenow = datetime.now()
        self.rundirectoryname = "IPA_Testrun_" + self.timenow.strftime("%d_%m_%H_%M")
        self.rundirectory = ""

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

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

        # System Load (Yes/No)
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

        # Iteration Count
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
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Configuration File", "", "Config Files (*.txt *.cfg *.ini);;All Files (*)")
        if file_name:
            self.config_entry.setText(file_name)
            self.config_file = file_name

    def start_test(self):
        self.ip = self.ip_entry.text()
        self.system_load = self.radio_yes.isChecked()
        self.iterations = int(self.iter_combo.currentText())

        # Check inputs
        if not self.ip or not self.excel_file or not self.config_file:
            self.update_status("Please provide all required inputs.", error=True)
            return

        # Create run directory
        self.rundirectory = os.path.join(os.getcwd(), self.rundirectoryname)
        os.makedirs(self.rundirectory, exist_ok=True)

        self.update_status(f"Starting IPA Test on {self.ip}...", error=False)

        # TODO: Replace with your actual test runner logic
        print(f"Running with: IP={self.ip}, Excel={self.excel_file}, Config={self.config_file}, "
              f"SystemLoad={self.system_load}, Iterations={self.iterations}")

    def update_status(self, message, error=False):
        color = "red" if error else "green"
        self.status_total.setText(f'<font color="{color}">{message}</font>')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = IPATestUI()
    win.show()
    sys.exit(app.exec_())
