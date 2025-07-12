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
class Main_utils_page(QWidget):
    def __init__(self):
        super().__init__()
        self.sig_use = pyqtSignal()
        self.page = self.main_page()
       
    def main_page(self):
        page = self.create_card()
        main_layout = QHBoxLayout()
        main_layout.addWidget(page)
        page.setLayout(main_layout)
        return page 
    
    def create_card(self):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("background-color: #272757; border-radius: 12px; padding: 2px;")
        vbox = QVBoxLayout()
        vbox.setSpacing(10)

        label = QLabel(f" Schdule a Task")
        label.setStyleSheet("color: white; font-weight: bold;")
        label.setAlignment(Qt.AlignCenter)
    
        exe_path_edit = QLineEdit()
        exe_path_edit.setPlaceholderText("Path to excel file")
        exe_path_edit.setStyleSheet(my_style)

        browse_btn = QPushButton("Browse")
        browse_btn.setStyleSheet(my_style)
        browse_btn.setMaximumWidth(80)
        browse_btn.clicked.connect(lambda: exe_path_edit.setText(QFileDialog.getOpenFileName(None, "Select EXE", "", "Executable Files (*.xlsx)")[0]))
         
        ip_add_path = QLineEdit()
        ip_add_path.setPlaceholderText("enter mcu ip address")
        ip_add_path.setStyleSheet(my_style)



        time_input = QLineEdit()
        time_input.setStyleSheet(my_style)
        time_input.setPlaceholderText("HH:MM (e.g., 14:30)")
        c = QLineEdit()
        c.setStyleSheet(my_style)
        c.setPlaceholderText("HH:MM (e.g., 14:30)")
        schedule_btn = QPushButton("Schedule")
        schedule_btn.setStyleSheet(my_style)
        schedule_btn.setMaximumWidth(80)
        schedule_btn.clicked.connect(lambda: self.create_and_schedule_task(
            exe_path_edit.text(),
            f"MyApp_Task_",
            time_input.text()
        ))

        vbox.addWidget(label)
        vbox.addWidget(exe_path_edit)
        vbox.addWidget(browse_btn)
        vbox.addWidget(ip_add_path)
        vbox.addWidget(time_input)
        vbox.addWidget(schedule_btn)
        card.setLayout(vbox)
        return card
    
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



