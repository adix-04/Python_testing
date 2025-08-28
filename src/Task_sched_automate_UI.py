from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QLineEdit, QTextEdit,
    QFrame, QScrollArea,QRadioButton,QFileDialog,QMessageBox,QComboBox
)
from PyQt5.QtGui import QIcon,QFont,QPixmap,QMovie
from PyQt5.QtCore import Qt
from datetime import datetime
from PyQt5.QtCore import pyqtSignal
import Test_runner_GUI
from styles import *
import subprocess
import os
from TTS_main import Test_begin

class Main_utils_page(QWidget):
    def __init__(self):
        super().__init__()
        self.sig_use = pyqtSignal()
        self.page = self.main_page()
        self.runnerlogDir = "Auto_Testrun_"+ datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        
       
    def main_page(self):
        page = self.create_card()
        main_layout = QHBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(page)
        page.setLayout(main_layout)
        return page 
    
    def create_card(self):
        card = QWidget()
        card.setStyleSheet("background-color: #302D2D; border-radius: 12px; padding: 2px;")
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)
        vbox.setSpacing(15)

        label = QLabel("Start A Task or Schedule One")
        label.setStyleSheet(my_style)
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName("headers")
        vbox.addWidget(label)
        # ---------- IP Address Input ----------
        ip_path_edit = QLineEdit()
        ip_path_edit.setPlaceholderText("IP Address")
        ip_path_edit.setStyleSheet(my_style)
        ip_path_edit.setText('169.254.80.')
        vbox.addWidget(ip_path_edit)

        # ---------- Excel File Input ----------
        exe_path_edit = QLineEdit()
        exe_path_edit.setPlaceholderText("Path to Excel")
        exe_path_edit.setStyleSheet(my_style)
        browse_btn = QPushButton("Browse")
        browse_btn.setStyleSheet(my_style)
        browse_btn.setFixedSize(100,30)
        browse_btn.clicked.connect(lambda: exe_path_edit.setText(
            QFileDialog.getOpenFileName(None, "Select Excel", "", "Excel Files (*.xlsx)")[0]
        ))

        exe_hbox = QHBoxLayout()
        exe_hbox.addWidget(exe_path_edit)
        exe_hbox.addWidget(browse_btn)
        vbox.addLayout(exe_hbox)

        # ---------- Log Folder Input ----------
        self.log_path_edit = QLineEdit()
        self.log_path_edit.setPlaceholderText("Path to Log Folder")
        self.log_path_edit.setStyleSheet(my_style)
        log_browse_btn = QPushButton("Browse")
        log_browse_btn.setStyleSheet(my_style)
        log_browse_btn.setFixedSize(100,30)
        # log_browse_btn.clicked.connect(lambda: log_path_edit.setText(
        #     QFileDialog.getExistingDirectory(self, 'Select Log Folder')
        # ))
        log_browse_btn.clicked.connect(self.select_log_folder)
        
        log_hbox = QHBoxLayout()
        log_hbox.addWidget(self.log_path_edit)
        log_hbox.addWidget(log_browse_btn)
        vbox.addLayout(log_hbox)

        # ---------- DLP Project File ----------
        fp_path_edit = QLineEdit()
        fp_path_edit.setPlaceholderText("Project file for DLT / ECU Configuration file to start dlt (*Rack wise)")
        fp_path_edit.setStyleSheet(my_style)
        fp_browse_btn = QPushButton("Browse")
        fp_browse_btn.setStyleSheet(my_style)
        fp_browse_btn.setFixedSize(100,30)
        fp_browse_btn.clicked.connect(lambda: fp_path_edit.setText(
            QFileDialog.getOpenFileName(None, "Select DLP File", "", "DLP Files (*.DLP)")[0]
        ))

        fp_hbox = QHBoxLayout()
        fp_hbox.addWidget(fp_path_edit)
        fp_hbox.addWidget(fp_browse_btn)
        msg_label  = QLabel("*DLP File will created on runtime with the given ip so this is optional part")
        msg_label.setStyleSheet("color:white;")
        
        vbox.addLayout(fp_hbox)
        vbox.addWidget(msg_label)
        # ---------- Time Input ----------
        time_input = QLineEdit()
        time_input.setStyleSheet(my_style)
        time_input.setPlaceholderText("Schedule Time (HH:MM, e.g., 14:30) optional IN DEVLOPMENT")
        vbox.addWidget(time_input)
        msg_label1  = QLabel("*Windows feature to schdule this as a task using task schduler. Run in headless mode")
        msg_label1.setStyleSheet("color:white;")
        vbox.addWidget(msg_label1)

        # ---------- Buttons ----------
        btn_hbox = QHBoxLayout()

        schedule_btn = QPushButton("Schedule")
        schedule_btn.setStyleSheet(my_style)
        schedule_btn.setFixedSize(100,50)
        schedule_btn.clicked.connect(lambda: self.create_and_schedule_task(
            exe_path_edit.text(),
            "MyApp_Task",
            time_input.text()
        ))
        checkbox_layout = QVBoxLayout()
        checkbox_label = QLabel("Give load to system?")
        checkbox_label.setStyleSheet(my_style)
        Give_load = QRadioButton("Yes (System may break🚨)")
        Give_no_load = QRadioButton("No (Much safer)")
        Give_load.setStyleSheet("color: white;")
        Give_no_load.setStyleSheet("color: white;")
        checkbox_layout.addWidget(checkbox_label)
        checkbox_layout.addWidget(Give_load)
        checkbox_layout.addWidget(Give_no_load)
        tech_stack = QComboBox()
        tech_stack.addItem("BCA")
        tech_stack.addItem("Cerance")
        test_btn = QPushButton("Start Test")
        test_btn.setStyleSheet(my_style)
        test_btn.setFixedSize(100,50)

        test_btn.clicked.connect(lambda: Test_begin(
        mcu_ip=ip_path_edit.text(),
        input_excel=exe_path_edit.text(),
        directory=self.runnerlogDir,
        dlp_file=fp_path_edit.text(),
        load=Give_load.isChecked(),
        stack=tech_stack.currentText()
        ))

        tech_stack.setStyleSheet(combo_sheet)
        checkbox_layout.addWidget(tech_stack)
        vbox.addLayout(checkbox_layout)
        btn_hbox.addWidget(test_btn)
        btn_hbox.addWidget(schedule_btn)
        vbox.addLayout(btn_hbox)
        # ---------- Final Card Layout ----------
        card.setLayout(vbox)
        return card

    def select_log_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Log Folder')
        if folder_path:
            self.log_path_edit.setText(folder_path)
            self.runnerlogDir=os.path.join(self.log_path_edit.text(),self.runnerlogDir)
        os.mkdir(self.runnerlogDir)

    def printer(self):
        print("god")
        print(self.time_input.text())
        print(self.exe_input.text())

    
    def create_and_schedule_task(self, exe_path, task_name, time_str):
        print(exe_path)
        print(task_name)
        print(time_str)
        cwd = os.getcwd()+'/bats'
       #we Create .bat file (i dont know how much safe is this one)
        os.makedirs(cwd, exist_ok=True)  # Create the directory if it doesn't exist
        bat_path = os.path.join(cwd, f"{task_name}.bat")
        # bat_path = os.path.join(cwd , f"{task_name}.bat")
        with open(bat_path, 'w') as f:
            f.write(f'start "" "{exe_path}"\n')
    
        # Schedule task using schtasks , like running a command in linux (can bring improvements)
        hour, minute = time_str.split(":")
        # https://learn.microsoft.com/en-us/windows/win32/taskschd/schtasks  for your reference 
        # this is definetley gonna break the system
        command = [
            "schtasks",
            "/Create",
            "/SC", "DAILY",
            "/TN", task_name,
            "/TR", f'"{bat_path}"',
            "/ST", f"{hour}:{minute}",
            "/F"
        ]
    
        try:
            subprocess.run(command, check=True)
            QMessageBox.information(self, "Scheduled", f"Task '{task_name}' scheduled at {time_str}")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Failed to schedule task:\n{str(e)}")



