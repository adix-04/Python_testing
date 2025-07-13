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
from styles import *
import subprocess
import os
from TTS_main import Test_begin
class Main_utils_page(QWidget):
    def __init__(self):
        super().__init__()
        self.sig_use = pyqtSignal()
        self.page = self.main_page()
       
    def main_page(self):
        page = self.create_card()
        main_layout = QHBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(page)
        page.setLayout(main_layout)
        return page 
        return page 
    
    def create_card(self):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("background-color: #272757; border-radius: 12px; padding: 2px;")
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignCenter)
        vbox.setSpacing(10)

        label = QLabel(f"Task")
        label.setStyleSheet("color: white; font-weight: bold;")
        label.setAlignment(Qt.AlignCenter)
    
        exe_path_edit = QLineEdit()
        exe_path_edit.setPlaceholderText("Path to Excel")
        exe_path_edit.setStyleSheet(my_style)

        browse_btn = QPushButton("Browse")
        browse_btn.setStyleSheet(my_style)
        browse_btn.setMaximumWidth(80)
        browse_btn.clicked.connect(lambda: exe_path_edit.setText(QFileDialog.getOpenFileName(None, "Select Excel", "", "Executable Files (*.xlsx)")[0]))

        log_path_edit = QLineEdit()
        log_path_edit.setPlaceholderText("Path to Log folder")
        log_path_edit.setStyleSheet(my_style)

        log_browse_btn = QPushButton("Browse")
        log_browse_btn.setStyleSheet(my_style)
        log_browse_btn.setMaximumWidth(80)
        log_browse_btn.clicked.connect(lambda: log_path_edit.setText(QFileDialog.getExistingDirectory(self, 'Select Log Folder')))
        
        ip_path_edit = QLineEdit()
        ip_path_edit.setPlaceholderText("ip address")
        ip_path_edit.setStyleSheet(my_style)

        time_input = QLineEdit()
        time_input.setStyleSheet(my_style)
        time_input.setPlaceholderText("HH:MM (e.g., 14:30)")

        c = QLineEdit()
        c.setStyleSheet(my_style)
        c.setPlaceholderText("HH:MM (e.g., 14:30)")
    
        test_btn = QPushButton("start test")
        test_btn.setStyleSheet(my_style)
        test_btn.setMaximumWidth(80)
        test_btn.clicked.connect(lambda: Test_begin(
            mcu_ip=ip_path_edit.text(),
            input_excel=exe_path_edit.text(),
            directory=log_path_edit.text()
        ))
        schedule_btn = QPushButton("Schedule")
        schedule_btn.setStyleSheet(my_style)
        schedule_btn.setMaximumWidth(80)
        schedule_btn.clicked.connect(lambda: self.create_and_schedule_task(
            exe_path_edit.text(),
            f"MyApp_Task",
            time_input.text()
        ))
        vbox.addWidget(label)
        vbox.addWidget(ip_path_edit)
        vbox.addWidget(exe_path_edit)
        vbox.addWidget(browse_btn)
        vbox.addWidget(log_path_edit)
        vbox.addWidget(log_browse_btn)
        vbox.addWidget(time_input)
        vbox.addWidget(test_btn)
        vbox.addWidget(schedule_btn)

        card.setLayout(vbox)
        return card
    
    def printer(self):
        print("god")
        print(self.time_input.text())
        print(self.exe_input.text())
    # def select_log_folder(self):
    #     folder_path = QFileDialog.getExistingDirectory(self, 'Select Log Folder')
    #     if folder_path:
    #         self.log_folder_edit.setText(folder_path)
    #     self.rundirectory=os.path.join(self.log_folder_edit.text(),self.rundirectoryname)
    #     os.mkdir(self.rundirectory)
    
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



