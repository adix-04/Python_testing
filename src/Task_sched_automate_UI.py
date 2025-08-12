from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QLabel, QMainWindow, QWidget, QPushButton, QSizePolicy,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QLineEdit, QGroupBox,
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

    '''
    def create_card(self):
        card = QWidget()
        card.setStyleSheet("border-radius: 12px;")

        # --- Add a background label ---
        background_label = QLabel(card)
        pixmap = QPixmap("/home/adin.n@acsiatech.com/Documents/work'/d8ipt8x-b87c1962-3077-43fd-8fab-890ab281e6b5.jpg")
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        background_label.setGeometry(card.rect())  
        background_label.lower()  # Send to back

        # --- Main layout ---
        vbox = QVBoxLayout(card)
        vbox.setAlignment(Qt.AlignTop)
        vbox.setSpacing(15)

        # Label header
        label = QLabel("Start A Task or Schedule One")
        label.setStyleSheet(my_style)
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName("headers")
        vbox.addWidget(label)

        # IP Address input
        ip_path_edit = QLineEdit()
        ip_path_edit.setPlaceholderText("IP Address")
        ip_path_edit.setStyleSheet(my_style)
        ip_path_edit.setText('169.254.80.')
        vbox.addWidget(ip_path_edit)

        # Excel File Input
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

        # Log Folder Input
        self.log_path_edit = QLineEdit()
        self.log_path_edit.setPlaceholderText("Path to Log Folder")
        self.log_path_edit.setStyleSheet(my_style)
        log_browse_btn = QPushButton("Browse")
        log_browse_btn.setStyleSheet(my_style)
        log_browse_btn.setFixedSize(100,30)

        log_browse_btn.clicked.connect(self.select_log_folder)

        # log_browse_btn.clicked.connect(lambda: log_path_edit.setText(
        #     QFileDialog.getExistingDirectory(self, 'Select Log Folder')
        # ))
        log_browse_btn.clicked.connect(self.select_log_folder)
        

        log_hbox = QHBoxLayout()
        log_hbox.addWidget(self.log_path_edit)
        log_hbox.addWidget(log_browse_btn)
        vbox.addLayout(log_hbox)

        # DLP Project File
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

        msg_label  = QLabel("*DLP File will be created at runtime with the given IP, optional")
        msg_label.setStyleSheet("color:white;background: transparent;")
        vbox.addLayout(fp_hbox)
        vbox.addWidget(msg_label)

        # Schedule time input
        time_input = QLineEdit()
        time_input.setStyleSheet(my_style)
        time_input.setPlaceholderText("Schedule Time (HH:MM, e.g., 14:30) optional")
        vbox.addWidget(time_input)
        msg_label1  = QLabel("*Windows feature to schedule this as a task")
        msg_label1.setStyleSheet("color:white; background: transparent;")

        vbox.addWidget(msg_label1)

        # Buttons + Options
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

        Give_load = QRadioButton("Yes ")
        Give_no_load = QRadioButton("No")
        Give_load.setStyleSheet("color: white;background: transparent;")
        Give_no_load.setStyleSheet("color: white;background: transparent;")

        checkbox_layout.addWidget(checkbox_label)
        checkbox_layout.addWidget(Give_load)
        checkbox_layout.addWidget(Give_no_load)

        tech_stack = QComboBox()
        tech_stack.addItem("BCA")
        tech_stack.addItem("Cerance")
        tech_stack.setStyleSheet(combo_sheet)
        checkbox_layout.addWidget(tech_stack)

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

        btn_hbox.addWidget(test_btn)
        btn_hbox.addWidget(schedule_btn)
        vbox.addLayout(checkbox_layout)
        vbox.addLayout(btn_hbox)

        # Keep background resizing
        card.resizeEvent = lambda event: background_label.setGeometry(card.rect())

        return card
'''


    def create_card(self):
        card = QWidget()
        card.setStyleSheet("background-color: #1E1E1E; border-radius: 12px;")

        main_layout = QVBoxLayout(card)
        main_layout.setSpacing(16)
        # ----- Connection Details -----
        connection_group = QGroupBox("Connection Details")
        connection_group.setStyleSheet("""
            QGroupBox {
                background-color: #2B2B2B;
                color: #CFCFCF;
                border-radius: 8px;
                margin-top: 4px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
        """)
        # Make it only as tall as needed
        connection_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        conn_layout = QVBoxLayout(connection_group)
        conn_layout.setContentsMargins(15, 15, 15, 15)  # tighter margins
        conn_layout.setSpacing(8)                   # less vertical space

        ip_path_edit = QLineEdit()
        ip_path_edit.setPlaceholderText("IP Address")
        ip_path_edit.setText("169.254.80.")
        ip_path_edit.setStyleSheet("""
            QLineEdit {
                background-color: #3B3B3B;
                color: white;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 3px;
            }
        """)
        conn_layout.addWidget(ip_path_edit)

        # ----- File Paths -----
        file_group = QGroupBox("File Paths")
        file_group.setStyleSheet(connection_group.styleSheet())
        file_layout = QVBoxLayout(file_group)

        # Path to Excel
        exe_path_edit = QLineEdit()
        exe_path_edit.setPlaceholderText("Path to Excel")
        exe_path_edit.setStyleSheet(ip_path_edit.styleSheet())
        browse_btn_excel = QPushButton("Browse")
        browse_btn_excel.setFixedSize(100, 30)
        browse_btn_excel.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #3C8D40;
            }
        """)
        browse_btn_excel.clicked.connect(lambda: exe_path_edit.setText(
            QFileDialog.getOpenFileName(None, "Select Excel", "", "Excel Files (*.xlsx)")[0]
        ))
        exe_hbox = QHBoxLayout()
        exe_hbox.addWidget(exe_path_edit)
        exe_hbox.addWidget(browse_btn_excel)
        file_layout.addLayout(exe_hbox)

        # Path to Log Folder
        self.log_path_edit = QLineEdit()
        self.log_path_edit.setPlaceholderText("Path to Log Folder")
        self.log_path_edit.setStyleSheet(ip_path_edit.styleSheet())
        browse_btn_log = QPushButton("Browse")
        browse_btn_log.setFixedSize(100, 30)
        browse_btn_log.setStyleSheet(browse_btn_excel.styleSheet())
        browse_btn_log.clicked.connect(self.select_log_folder)
        log_hbox = QHBoxLayout()
        log_hbox.addWidget(self.log_path_edit)
        log_hbox.addWidget(browse_btn_log)
        file_layout.addLayout(log_hbox)

        # Project File
        fp_path_edit = QLineEdit()
        fp_path_edit.setPlaceholderText("Project File (optional)")
        fp_path_edit.setStyleSheet(ip_path_edit.styleSheet())
        browse_btn_fp = QPushButton("Browse")
        browse_btn_fp.setFixedSize(100, 30)
        browse_btn_fp.setStyleSheet(browse_btn_excel.styleSheet())
        browse_btn_fp.clicked.connect(lambda: fp_path_edit.setText(
            QFileDialog.getOpenFileName(None, "Select DLP File", "", "DLP Files (*.DLP)")[0]
        ))
        fp_hbox = QHBoxLayout()
        fp_hbox.addWidget(fp_path_edit)
        fp_hbox.addWidget(browse_btn_fp)
        file_layout.addLayout(fp_hbox)

        # ----- Execution Settings -----
        exec_group = QGroupBox("Execution Settings")
        exec_group.setStyleSheet(connection_group.styleSheet())
        exec_layout = QVBoxLayout(exec_group)

        # Schedule Time
        time_input = QLineEdit()
        time_input.setPlaceholderText("Schedule Time (HH:MM)")
        time_input.setStyleSheet(ip_path_edit.styleSheet())
        exec_layout.addWidget(time_input)

        # Radio buttons group
        radio_layout = QVBoxLayout()
        radio_layout.setContentsMargins(0, 0, 0, 0)
        radio_layout.setSpacing(4)

        radio_label = QLabel("Give CPU load through ADB")
        radio_label.setStyleSheet("""
            QLabel {
                color: #CFCFCF;
                background: transparent;
                font-size: 12px;
            }
        """)
        radio_label.setFixedHeight(18)
        radio_layout.addWidget(radio_label)
        radio_buttons_row = QHBoxLayout()
        radio_buttons_row.setContentsMargins(0, 0, 0, 0)
        radio_buttons_row.setSpacing(12)
        give_load = QRadioButton("Yes")
        give_no_load = QRadioButton("No")
        give_load.setStyleSheet("""
        QRadioButton {
            color: #CFCFCF;
            background: transparent;
        }
        QRadioButton::indicator {
            width: 16px;
            height: 16px;
            border-radius: 8px;  /* Make it circular */
            border: 2px solid #999999;
            background: transparent;
        }
        QRadioButton::indicator:checked {
            border: 2px solid #2196F3;
            background-color: qradialgradient(
                cx: 0.5, cy: 0.5, radius: 0.6,
                fx: 0.5, fy: 0.5,
                stop: 0 #2196F3, stop: 1 transparent
            );
        }
    """)

        give_no_load.setStyleSheet("""
        QRadioButton {
            color: #CFCFCF;
            background: transparent;
        }
        QRadioButton::indicator {
            width: 16px;
            height: 16px;
            border-radius: 8px;
            border: 2px solid #999999;
            background: transparent;
        }
        QRadioButton::indicator:checked {
            border: 2px solid #2196F3;
            background-color: qradialgradient(
                cx: 0.5, cy: 0.5, radius: 0.6,
                fx: 0.5, fy: 0.5,
                stop: 0 #2196F3, stop: 1 transparent
            );
        }
    """)


        radio_buttons_row.addWidget(give_load)
        radio_buttons_row.addWidget(give_no_load)
        radio_buttons_row.addStretch()

        radio_layout.addLayout(radio_buttons_row)
        exec_layout.addLayout(radio_layout)

        # Dropdown
       # Dropdown label
        stack_label = QLabel("Select stack")
        stack_label.setStyleSheet("""
            QLabel {
                color: #CFCFCF;
                background: transparent;
                font-size: 12px;
            }
        """)
        stack_label.setFixedHeight(18)
        exec_layout.addWidget(stack_label)

        # Dropdown
        tech_stack = QComboBox()
        tech_stack.addItem("BCA")
        tech_stack.addItem("Cerance")
        tech_stack.setStyleSheet("""
            QComboBox {
                background-color: #3B3B3B;
                color: white;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 4px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #3B3B3B;
                color: white;
                selection-background-color: #007ACC;
                selection-color: white;
            }
        """)
        exec_layout.addWidget(tech_stack)


        # ----- Action Buttons -----
        btn_hbox = QHBoxLayout()
        test_btn = QPushButton("Start Test")
        test_btn.setFixedHeight(40)
        test_btn.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005A99;
            }
        """)
        test_btn.clicked.connect(lambda: Test_begin(
            mcu_ip=ip_path_edit.text(),
            input_excel=exe_path_edit.text(),
            directory=self.runnerlogDir,
            dlp_file=fp_path_edit.text(),
            load=give_load.isChecked(),
            stack=tech_stack.currentText()
        ))

        schedule_btn = QPushButton("Schedule")
        schedule_btn.setFixedHeight(40)
        schedule_btn.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #005A99;
            }
        """)
        schedule_btn.clicked.connect(lambda: self.create_and_schedule_task(
            exe_path_edit.text(),
            "MyApp_Task",
            time_input.text()
        ))

        btn_hbox.addWidget(test_btn)
        btn_hbox.addWidget(schedule_btn)

        # ----- Assemble Layout -----
        main_layout.addWidget(connection_group)
        main_layout.addWidget(file_group)
        main_layout.addWidget(exec_group)
        main_layout.addLayout(btn_hbox)

        return card

#     def create_card(self):
#         card = QWidget()
        
        
#         card.setStyleSheet("""
#     QWidget {
#         border-image: url(/home/adin.n@acsiatech.com/Downloads/2109565-3840x2160-desktop-4k-jet-fighter-background-photo.jpg) 0 0 0 0 stretch stretch;
#         border-radius: 12px;
#         padding: 2px;
#     }
# """)


#         vbox = QVBoxLayout()
#         vbox.setAlignment(Qt.AlignTop)
#         vbox.setSpacing(15)
#         # self.background_label = QLabel(self)
#         # pixmap = QPixmap("/home/adin.n@acsiatech.com/Downloads/2109565-3840x2160-desktop-4k-jet-fighter-background-photo.jpg")  # Replace with your image path
#         # self.background_label.setPixmap(pixmap)
#         # self.background_label.setScaledContents(True)
#         # self.background_label.setGeometry(0, 0, self.width(), self.height())
#         # vbox.addWidget(self.background_label)
#         label = QLabel("Start A Task or Schedule One")
#         label.setStyleSheet(my_style)
#         label.setAlignment(Qt.AlignCenter)
#         label.setObjectName("headers")
#         vbox.addWidget(label)
#         # ---------- IP Address Input ----------
#         ip_path_edit = QLineEdit()
#         ip_path_edit.setPlaceholderText("IP Address")
#         ip_path_edit.setStyleSheet(my_style)
#         ip_path_edit.setText('169.254.80.')
#         vbox.addWidget(ip_path_edit)

#         # ---------- Excel File Input ----------
#         exe_path_edit = QLineEdit()
#         exe_path_edit.setPlaceholderText("Path to Excel")
#         exe_path_edit.setStyleSheet(my_style)
#         browse_btn = QPushButton("Browse")
#         browse_btn.setStyleSheet(my_style)
#         browse_btn.setFixedSize(100,30)
#         browse_btn.clicked.connect(lambda: exe_path_edit.setText(
#             QFileDialog.getOpenFileName(None, "Select Excel", "", "Excel Files (*.xlsx)")[0]
#         ))

#         exe_hbox = QHBoxLayout()
#         exe_hbox.addWidget(exe_path_edit)
#         exe_hbox.addWidget(browse_btn)
#         vbox.addLayout(exe_hbox)

#         # ---------- Log Folder Input ----------
#         self.log_path_edit = QLineEdit()
#         self.log_path_edit.setPlaceholderText("Path to Log Folder")
#         self.log_path_edit.setStyleSheet(my_style)
#         log_browse_btn = QPushButton("Browse")
#         log_browse_btn.setStyleSheet(my_style)
#         log_browse_btn.setFixedSize(100,30)
#         # log_browse_btn.clicked.connect(lambda: log_path_edit.setText(
#         #     QFileDialog.getExistingDirectory(self, 'Select Log Folder')
#         # ))
#         log_browse_btn.clicked.connect(self.select_log_folder)
        
#         log_hbox = QHBoxLayout()
#         log_hbox.addWidget(self.log_path_edit)
#         log_hbox.addWidget(log_browse_btn)
#         vbox.addLayout(log_hbox)

#         # ---------- DLP Project File ----------
#         fp_path_edit = QLineEdit()
#         fp_path_edit.setPlaceholderText("Project file for DLT / ECU Configuration file to start dlt (*Rack wise)")
#         fp_path_edit.setStyleSheet(my_style)
#         fp_browse_btn = QPushButton("Browse")
#         fp_browse_btn.setStyleSheet(my_style)
#         fp_browse_btn.setFixedSize(100,30)
#         fp_browse_btn.clicked.connect(lambda: fp_path_edit.setText(
#             QFileDialog.getOpenFileName(None, "Select DLP File", "", "DLP Files (*.DLP)")[0]
#         ))

#         fp_hbox = QHBoxLayout()
#         fp_hbox.addWidget(fp_path_edit)
#         fp_hbox.addWidget(fp_browse_btn)
#         msg_label  = QLabel("*DLP File will created on runtime with the given ip so this is optional part")
#         msg_label.setStyleSheet("color:white;")
        
#         vbox.addLayout(fp_hbox)
#         vbox.addWidget(msg_label)
#         # ---------- Time Input ----------
#         time_input = QLineEdit()
#         time_input.setStyleSheet(my_style)
#         time_input.setPlaceholderText("Schedule Time (HH:MM, e.g., 14:30) optional IN DEVLOPMENT")
#         vbox.addWidget(time_input)
#         msg_label1  = QLabel("*Windows feature to schdule this as a task using task schduler. Run in headless mode")
#         msg_label1.setStyleSheet("color:white;")
#         vbox.addWidget(msg_label1)

#         # ---------- Buttons ----------
#         btn_hbox = QHBoxLayout()

#         schedule_btn = QPushButton("Schedule")
#         schedule_btn.setStyleSheet(my_style)
#         schedule_btn.setFixedSize(100,50)
#         schedule_btn.clicked.connect(lambda: self.create_and_schedule_task(
#             exe_path_edit.text(),
#             "MyApp_Task",
#             time_input.text()
#         ))
#         checkbox_layout = QVBoxLayout()
#         checkbox_label = QLabel("Give load to system?")
#         checkbox_label.setStyleSheet(my_style)
#         Give_load = QRadioButton("Yes (System may break)")
#         Give_no_load = QRadioButton("No (Much safer)")
#         Give_load.setStyleSheet("color: white;")
#         Give_no_load.setStyleSheet("color: white;")
#         checkbox_layout.addWidget(checkbox_label)
#         checkbox_layout.addWidget(Give_load)
#         checkbox_layout.addWidget(Give_no_load)
#         tech_stack = QComboBox()
#         tech_stack.addItem("BCA")
#         tech_stack.addItem("Cerance")
#         test_btn = QPushButton("Start Test")
#         test_btn.setStyleSheet(my_style)
#         test_btn.setFixedSize(100,50)

#         test_btn.clicked.connect(lambda: Test_begin(
#         mcu_ip=ip_path_edit.text(),
#         input_excel=exe_path_edit.text(),
#         directory=self.runnerlogDir,
#         dlp_file=fp_path_edit.text(),
#         load=Give_load.isChecked(),
#         stack=tech_stack.currentText()
#         ))

#         tech_stack.setStyleSheet(combo_sheet)
#         checkbox_layout.addWidget(tech_stack)
#         vbox.addLayout(checkbox_layout)
#         btn_hbox.addWidget(test_btn)
#         btn_hbox.addWidget(schedule_btn)
#         vbox.addLayout(btn_hbox)
#         # ---------- Final Card Layout ----------
#         card.setLayout(vbox)
#         return card

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



