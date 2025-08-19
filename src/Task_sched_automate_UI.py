# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtWidgets import (
#     QLabel, QMainWindow, QWidget, QPushButton, QSizePolicy,
#     QVBoxLayout, QHBoxLayout, QStackedWidget, QLineEdit, QGroupBox,
#      QScrollArea,QRadioButton,QFileDialog,QMessageBox,QComboBox
# )
# from PyQt5.QtGui import QIcon,QFont,QPixmap,QMovie
# from PyQt5.QtCore import Qt,QTimer
# from datetime import datetime
# from PyQt5.QtCore import pyqtSignal
# import Test_runner_GUI
# from styles import *
# import subprocess
# import os
# from TTS_main import Test_begin

# class Main_utils_page(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.sig_use = pyqtSignal()
#         self.page = self.main_page()
#         self.runnerlogDir = "Auto_Testrun_"+ datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
       
#     def main_page(self):
        
#         page = self.create_card()
#         main_layout = QHBoxLayout()
#         main_layout.setAlignment(Qt.AlignCenter)
#         main_layout.addWidget(page)
#         page.setLayout(main_layout)
#         return page 

   

#     def create_card(self):
#         card = QWidget()
#         card.setStyleSheet("background-color: #1E1E1E; border-radius: 12px;")

#         main_layout = QVBoxLayout(card)
#         main_layout.setSpacing(16)
#         # ----- Connection Details -----
#         connection_group = QGroupBox("Connection Details")
#         connection_group.setStyleSheet("""
#             QGroupBox {
#                 background-color: #2B2B2B;
#                 color: #CFCFCF;
#                 border-radius: 8px;
#                 margin-top: 4px;
#                 font-weight: bold;
#             }
#             QGroupBox::title {
#                 subcontrol-origin: margin;
#                 left: 10px;
#                 padding: 0 3px 0 3px;
#             }
#         """)
#         # Make it only as tall as needed
#         connection_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

#         conn_layout = QVBoxLayout(connection_group)
#         conn_layout.setContentsMargins(8, 8, 8, 8)  # tighter margins
#         conn_layout.setSpacing(8)                   # less vertical space

#         self.ip_path_edit = QLineEdit()
#         self.ip_path_edit.setPlaceholderText("IP Address")
#         self.ip_path_edit.setText("169.254.80.")
#         self.ip_path_edit.setStyleSheet("""
#             QLineEdit {
#                 background-color: #3B3B3B;
#                 color: white;
#                 border: 1px solid #555555;
#                 border-radius: 4px;
#                 padding: 3px;
#             }
#         """)
#         conn_layout.addWidget(self.ip_path_edit)

#         # ----- File Paths -----
#         file_group = QGroupBox("File Paths")
#         file_group.setStyleSheet(connection_group.styleSheet())
#         file_layout = QVBoxLayout(file_group)

#         # Path to Excel
#         self.exe_path_edit = QLineEdit()
#         self.exe_path_edit.setPlaceholderText("Path to Excel")
#         self.exe_path_edit.setStyleSheet(self.ip_path_edit.styleSheet())
#         browse_btn_excel = QPushButton("Browse")
#         browse_btn_excel.setFixedSize(100, 30)
#         browse_btn_excel.setStyleSheet("""
#             QPushButton {
#                 background-color: #4CAF50;
#                 color: white;
#                 border-radius: 4px;
#             }
#             QPushButton:hover {
#                 background-color: #3C8D40;
#             }
#         """)
#         browse_btn_excel.clicked.connect(lambda: self.exe_path_edit.setText(
#             QFileDialog.getOpenFileName(None, "Select Excel", "", "Excel Files (*.xlsx)")[0]
#         ))
#         exe_hbox = QHBoxLayout()
#         exe_hbox.addWidget(self.exe_path_edit)
#         exe_hbox.addWidget(browse_btn_excel)
#         file_layout.addLayout(exe_hbox)

#         # Path to Log Folder
#         self.log_path_edit = QLineEdit()
#         self.log_path_edit.setPlaceholderText("Path to Log Folder")
#         self.log_path_edit.setStyleSheet(self.ip_path_edit.styleSheet())
#         browse_btn_log = QPushButton("Browse")
#         browse_btn_log.setFixedSize(100, 30)
#         browse_btn_log.setStyleSheet(browse_btn_excel.styleSheet())
#         browse_btn_log.clicked.connect(self.select_log_folder)
#         log_hbox = QHBoxLayout()
#         log_hbox.addWidget(self.log_path_edit)
#         log_hbox.addWidget(browse_btn_log)
#         file_layout.addLayout(log_hbox)

#         # Project File
#         self.fp_path_edit = QLineEdit()
#         self.fp_path_edit.setPlaceholderText("Project File (optional)")
#         self.fp_path_edit.setStyleSheet(self.ip_path_edit.styleSheet())
#         browse_btn_fp = QPushButton("Browse")
#         browse_btn_fp.setFixedSize(100, 30)
#         browse_btn_fp.setStyleSheet(browse_btn_excel.styleSheet())
#         browse_btn_fp.clicked.connect(lambda: self.fp_path_edit.setText(
#             QFileDialog.getOpenFileName(None, "Select DLP File", "", "DLP Files (*.DLP)")[0]
#         ))
#         fp_hbox = QHBoxLayout()
#         fp_hbox.addWidget(self.fp_path_edit)
#         fp_hbox.addWidget(browse_btn_fp)
#         file_layout.addLayout(fp_hbox)

#         # ----- Execution Settings -----
#         exec_group = QGroupBox("Execution Settings")
#         exec_group.setStyleSheet(connection_group.styleSheet())
#         exec_layout = QVBoxLayout(exec_group)

#         # Schedule Time
#         time_input = QLineEdit()
#         time_input.setPlaceholderText("Schedule Time (HH:MM)")
#         time_input.setStyleSheet(self.ip_path_edit.styleSheet())
#         exec_layout.addWidget(time_input)

#         # Radio buttons group
#         radio_layout = QVBoxLayout()
#         radio_layout.setContentsMargins(0, 0, 0, 0)
#         radio_layout.setSpacing(4)

#         radio_label = QLabel("Give CPU load through ADB")
#         radio_label.setStyleSheet("""
#             QLabel {
#                 color: #CFCFCF;
#                 background: transparent;
#                 font-size: 12px;
#             }
#         """)
#         radio_label.setFixedHeight(18)
#         radio_layout.addWidget(radio_label)
#         radio_buttons_row = QHBoxLayout()
#         radio_buttons_row.setContentsMargins(0, 0, 0, 0)
#         radio_buttons_row.setSpacing(12)
#         self.give_load = QRadioButton("Yes")
#         self.give_no_load = QRadioButton("No")
#         self.give_load.setStyleSheet("""
#         QRadioButton {
#             color: #CFCFCF;
#             background: transparent;
#         }
#         QRadioButton::indicator {
#             width: 16px;
#             height: 16px;
#             border-radius: 8px;  /* Make it circular */
#             border: 2px solid #999999;
#             background: transparent;
#         }
#         QRadioButton::indicator:checked {
#             border: 2px solid #2196F3;
#             background-color: qradialgradient(
#                 cx: 0.5, cy: 0.5, radius: 0.6,
#                 fx: 0.5, fy: 0.5,
#                 stop: 0 #2196F3, stop: 1 transparent
#             );
#         }
#     """)

#         self.give_no_load.setStyleSheet("""
#         QRadioButton {
#             color: #CFCFCF;
#             background: transparent;
#         }
#         QRadioButton::indicator {
#             width: 16px;
#             height: 16px;
#             border-radius: 8px;
#             border: 2px solid #999999;
#             background: transparent;
#         }
#         QRadioButton::indicator:checked {
#             border: 2px solid #2196F3;
#             background-color: qradialgradient(
#                 cx: 0.5, cy: 0.5, radius: 0.6,
#                 fx: 0.5, fy: 0.5,
#                 stop: 0 #2196F3, stop: 1 transparent
#             );
#         }
#     """)


#         radio_buttons_row.addWidget(self.give_load)
#         radio_buttons_row.addWidget(self.give_no_load)
#         radio_buttons_row.addStretch()

#         radio_layout.addLayout(radio_buttons_row)
#         exec_layout.addLayout(radio_layout)

#         # Dropdown
#        # Dropdown label
#         stack_label = QLabel("Select stack")
#         stack_label.setStyleSheet("""
#             QLabel {
#                 color: #CFCFCF;
#                 background: transparent;
#                 font-size: 12px;
#             }
#         """)
#         stack_label.setFixedHeight(18)
#         exec_layout.addWidget(stack_label)

#         # Dropdown
#         self.tech_stack = QComboBox()
#         self.tech_stack.addItem("BCA")
#         self.tech_stack.addItem("Cerance")
#         self.tech_stack.setStyleSheet("""
#             QComboBox {
#                 background-color: #3B3B3B;
#                 color: white;
#                 border: 1px solid #555555;
#                 border-radius: 4px;
#                 padding: 4px;
#             }
#             QComboBox::drop-down {
#                 border: none;
#             }
#             QComboBox QAbstractItemView {
#                 background-color: #3B3B3B;
#                 color: white;
#                 selection-background-color: #007ACC;
#                 selection-color: white;
#             }
#         """)
#         exec_layout.addWidget(self.tech_stack)


#         # ----- Action Buttons -----
#         btn_hbox = QHBoxLayout()
#         test_btn = QPushButton("Start Test")
#         test_btn.setFixedHeight(40)
#         test_btn.setStyleSheet("""
#             QPushButton {
#                 background-color: #007ACC;
#                 color: white;
#                 border-radius: 4px;
#                 font-weight: bold;
#             }
#             QPushButton:hover {
#                 background-color: #005A99;
#             }
#         """)
#         # test_btn.clicked.connect(lambda: Test_begin(
#         #     mcu_ip=ip_path_edit.text(),
#         #     input_excel=exe_path_edit.text(),
#         #     directory=self.runnerlogDir,
#         #     dlp_file=fp_path_edit.text(),
#         #     load=give_load.isChecked(),
#         #     stack=tech_stack.currentText()
#         # ))
#         test_btn.clicked.connect(self.start_test)

#         schedule_btn = QPushButton("Schedule")
#         schedule_btn.setFixedHeight(40)
#         schedule_btn.setStyleSheet("""
#             QPushButton {
#                 background-color: #007ACC;
#                 color: white;
#                 border-radius: 4px;
#             }
#             QPushButton:hover {
#                 background-color: #005A99;
#             }
#         """)
#         schedule_btn.clicked.connect(lambda: self.create_and_schedule_task(
#             ip=self.ip_path_edit.text(),
#             excel=self.exe_path_edit.text(),
#             dir=self.runnerlogDir,
#             dlp=self.fp_path_edit.text(),
#             load=self.give_load.isChecked(),
#             stack=self.tech_stack.currentText(),
#             time_str=time_input.text()
#         ))

#         btn_hbox.addWidget(test_btn)
#         btn_hbox.addWidget(schedule_btn)
#         label_group = QGroupBox()
#         label_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum) 
#         label_group.setStyleSheet(connection_group.styleSheet())
#         label_layout =  QVBoxLayout(label_group)
#         self.status_label = QLabel(f"Total / Played  0/0")
#         self.status_label.setStyleSheet("""
#             QLabel {
#                 color: #CFCFCF;
#                 background: transparent;
#                 font-size: 12px;
#             }
#         """)

#         label_layout.addWidget(self.status_label)
#         # ----- Assemble Layout -----
#         main_layout.addWidget(connection_group)
#         main_layout.addWidget(file_group)
#         main_layout.addWidget(exec_group)
#         main_layout.addWidget(label_group)
#         main_layout.addLayout(btn_hbox)

#         return card


#     def select_log_folder(self):
#         folder_path = QFileDialog.getExistingDirectory(self, 'Select Log Folder')
#         if folder_path:
#             self.log_path_edit.setText(folder_path)
#             self.runnerlogDir=os.path.join(self.log_path_edit.text(),self.runnerlogDir)
#         os.mkdir(self.runnerlogDir)

#     def start_test(self):
#         self.test_obj = Test_begin(
#         mcu_ip=self.ip_path_edit.text(),
#         input_excel=self.exe_path_edit.text(),
#         directory=self.runnerlogDir,
#         dlp_file=self.fp_path_edit.text(),
#         load=self.give_load.isChecked(),
#         stack=self.tech_stack.currentText()
#     )
#         self.rem_load_time = self.test_obj.load_time
#         print(f"{self.test_obj.load_time}load time fron core")
#         self.status_label.setText(f"Time Remaining: {self.rem_load_time}s")
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.update_timer)
#         self.timer.start(1000)
#         self.test_obj.test_init()
#     def update_timer(self):
#         if self.rem_load_time > 0 :
#             self.rem_load_time -=1
#             self.status_label.setText(f"Time Remaining: {self.rem_load_time}s")
#         else :
#             self.timer.stop()


    
#     def create_and_schedule_task(self, ip, excel,dir,dlp,load,stack,time_str):
#         print("called sched task")
#         task_name = "MyAppTaskV1.0.1"
#         python_exe = os.path.abspath(os.sys.executable)
#         script_dir = os.path.dirname(os.path.abspath(__file__))
#         script_path = os.path.join(script_dir, "TTS_main.py")

#         # Ensure paths are properly quoted  like " c:/users/ " 
#         excel_path = f'"{excel}"'
#         dir_path = f'"{dir}"'
#         dlp_path = f'"{dlp}"'

#         # Create .bat file in same folder as script
#         bat_file = os.path.join(script_dir, f"{task_name}.bat")

#         bat_content = f"""@echo off
#     cd /d "{script_dir}"
#     "{python_exe}" "{script_path}" --ip {ip} --excel {excel_path} --dir {dir_path} --dlp {dlp_path} --load {load} --tech {stack}
#     pause
#     """

#         with open(bat_file, "w") as f:
#             f.write(bat_content)

#         print(f"Batch file created at: {bat_file}")
#          # Schedule task using schtasks , like running a command in linux (can bring improvements)
#         hour, minute = time_str.split(":")
#         # https://learn.microsoft.com/en-us/windows/win32/taskschd/schtasks  for your reference 
      
#         command = [
#             "schtasks",
#             "/Create",
#             "/SC", "ONCE",
#             "/TN", task_name,
#             "/TR", f'"{bat_file}"',
#             "/ST", f"{hour}:{minute}",
#             "/F"
#         ]
    
#         try:
#             subprocess.run(command, check=True)
#             QMessageBox.information(self, "Scheduled", f"Task '{task_name}' scheduled at {time_str}")
#         except subprocess.CalledProcessError as e:
#             QMessageBox.critical(self, "Error", f"Failed to schedule task:\n{str(e)}")
#         '''

#         return bat_file

#         '''
        
#     def create_tts_bat(ip, excel_path, dir_path, dlp_path, load, tech, bat_name="run_tts"):
#         # Get current Python executable and script directory
#         python_exe = os.path.abspath(os.sys.executable)
#         script_dir = os.path.dirname(os.path.abspath(__file__))
#         script_path = os.path.join(script_dir, "TTS_main.py")

#         # Ensure paths are properly quoted for spaces
#         excel_path = f'"{excel_path}"'
#         dir_path = f'"{dir_path}"'
#         dlp_path = f'"{dlp_path}"'

#         # Create .bat file in same folder as script
#         bat_file = os.path.join(script_dir, f"{bat_name}.bat")

#         bat_content = f"""@echo off
#     cd /d "{script_dir}"
#     "{python_exe}" "{script_path}" --ip {ip} --excel {excel_path} --dir {dir_path} --dlp {dlp_path} --load {load} --tech {tech}
#     pause
#     """

#         with open(bat_file, "w") as f:
#             f.write(bat_content)

#         print(f"Batch file created at: {bat_file}")
#         return bat_file

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QLabel, QGraphicsBlurEffect, QWidget, QPushButton, QSizePolicy,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QLineEdit, QGroupBox,
    QScrollArea, QRadioButton, QFileDialog, QMessageBox, QComboBox
)
from PyQt5.QtGui import QIcon, QFont, QPixmap, QMovie
from PyQt5.QtCore import Qt, QTimer, QThread, QObject, pyqtSignal, pyqtSlot
from datetime import datetime
import subprocess
import os

from TTS_main import Test_begin


# ---------- Worker that runs the heavy core code off the GUI thread ----------
class Worker(QObject):
    finished = pyqtSignal()           # emitted when core function finishes normally
    error = pyqtSignal(str)           # emitted when an exception occurs when something goes wrong

    def __init__(self, core_obj: Test_begin):
        super().__init__()
        self.core = core_obj

    @pyqtSlot()
    def run(self):
        try:
            #heavy work; keep it out of the main thread
            self.core.test_init()
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))


class Main_utils_page(QWidget):
    def __init__(self):
        super().__init__()
        self.page = self.main_page()

        self.runnerlogDir = "Auto_Testrun_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        # runtime holders
        self.test_obj = None
        self.timer = None
        self.rem_load_time = 0
        self.thread = None
        self.worker = None

    def main_page(self):
        page = self.create_card()
        main_layout = QHBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(page)
        page.setLayout(main_layout)
        return page

    def create_card(self):
        card = QWidget()
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(10)
       
        # card.setStyleSheet("background-color: #1E1E1E; border-radius: 12px;") 2B2B2B
        card.setStyleSheet("background : transparent")
        main_layout = QVBoxLayout(card)
        main_layout.setSpacing(16)

        # ----- Connection Details -----
        connection_group = QGroupBox("Connection Details")
        connection_group.setFixedSize(720,50)
        connection_group.setStyleSheet("""
            QGroupBox {
                color: #CFCFCF;
                border-radius: 8px;
                margin-top: 4px;
                font-weight: bold;
                font-size : 12x;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 0px 0 3px;
            }
        """)
        connection_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        conn_layout = QVBoxLayout(connection_group)
        conn_layout.setContentsMargins(8, 8, 8, 8)
        conn_layout.setSpacing(5)

        self.ip_path_edit = QLineEdit()
        self.ip_path_edit.setFixedSize(600,40)
        self.ip_path_edit.setPlaceholderText("IP Address")
        self.ip_path_edit.setText("169.254.80.")
        self.ip_path_edit.setStyleSheet("""
            QLineEdit {
                background-color: #3B3B3B;
                color: white;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 3px;
                font-size : 14px ;
            }
        """)
        conn_layout.addWidget(self.ip_path_edit)

        # ----- File Paths -----
        file_group = QGroupBox("File Paths")
        file_group.setStyleSheet(connection_group.styleSheet())
        file_layout = QVBoxLayout(file_group)
        file_group.setFixedSize(720,170)

        # Path to Excel
        self.exe_path_edit = QLineEdit()
        self.exe_path_edit.setFixedSize(600,40)
        self.exe_path_edit.setPlaceholderText("Path to Excel")
        self.exe_path_edit.setStyleSheet(self.ip_path_edit.styleSheet())
        browse_btn_excel = QPushButton("Browse")
        browse_btn_excel.setFixedSize(100, 40)
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
        browse_btn_excel.clicked.connect(lambda: self.exe_path_edit.setText(
            QFileDialog.getOpenFileName(None, "Select Excel", "", "Excel Files (*.xlsx)")[0]
        ))
        exe_hbox = QHBoxLayout()
        exe_hbox.addWidget(self.exe_path_edit)
        exe_hbox.addWidget(browse_btn_excel)
        file_layout.addLayout(exe_hbox)

        # Path to Log Folder
        self.log_path_edit = QLineEdit()
        self.log_path_edit.setFixedSize(600,40)
        self.log_path_edit.setPlaceholderText("Path to Log Folder")
        self.log_path_edit.setStyleSheet(self.ip_path_edit.styleSheet())
        browse_btn_log = QPushButton("Browse")
        browse_btn_log.setFixedSize(100, 40)
        browse_btn_log.setStyleSheet(browse_btn_excel.styleSheet())
        browse_btn_log.clicked.connect(self.select_log_folder)
        log_hbox = QHBoxLayout()
        log_hbox.addWidget(self.log_path_edit)
        log_hbox.addWidget(browse_btn_log)
        file_layout.addLayout(log_hbox)

        # Project File
        self.fp_path_edit = QLineEdit()
        self.fp_path_edit.setFixedSize(600,40)
        self.fp_path_edit.setPlaceholderText("Project File (optional)")
        self.fp_path_edit.setStyleSheet(self.ip_path_edit.styleSheet())
        browse_btn_fp = QPushButton("Browse")
        browse_btn_fp.setFixedSize(100, 40)
        browse_btn_fp.setStyleSheet(browse_btn_excel.styleSheet())
        browse_btn_fp.clicked.connect(lambda: self.fp_path_edit.setText(
            QFileDialog.getOpenFileName(None, "Select DLP File", "", "DLP Files (*.dlp *.DLP)")[0]
        ))
        fp_hbox = QHBoxLayout()
        fp_hbox.addWidget(self.fp_path_edit)
        fp_hbox.addWidget(browse_btn_fp)
        file_layout.addLayout(fp_hbox)

        # ----- Execution Settings -----
        exec_group = QGroupBox("Execution Settings")
        exec_group.setStyleSheet(connection_group.styleSheet())
        exec_group.setFixedSize(720,190)
        exec_layout = QVBoxLayout(exec_group)
        
        # Schedule Time
        self.time_input = QLineEdit()  # keep a handle for schedule
        self.time_input.setPlaceholderText("Schedule Time (HH:MM)")
        self.time_input.setFixedSize(600,40)
        self.time_input.setStyleSheet(self.ip_path_edit.styleSheet())

        exec_layout.addWidget(self.time_input)

        # Radio buttons group
        radio_layout = QVBoxLayout()
        radio_layout.setContentsMargins(0, 0, 0, 0)
        radio_layout.setSpacing(4)

        radio_label = QLabel("Give CPU load through ADB")
        radio_label.setStyleSheet("""
            QLabel {
                color: #CFCFCF;
                background: transparent;
                font-size: 10px;
                font-weight : bold;
            }
        """)
        radio_label.setFixedHeight(18)
        radio_layout.addWidget(radio_label)

        radio_buttons_row = QHBoxLayout()
        radio_buttons_row.setContentsMargins(0, 0, 0, 0)
        radio_buttons_row.setSpacing(12)
        self.give_load = QRadioButton("Yes")
        self.give_no_load = QRadioButton("No")
        self.give_no_load.setChecked(True)  # default to No

        radio_common = """
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
        """
        self.give_load.setStyleSheet(radio_common)
        self.give_no_load.setStyleSheet(radio_common)

        radio_buttons_row.addWidget(self.give_load)
        radio_buttons_row.addWidget(self.give_no_load)
        radio_buttons_row.addStretch()

        radio_layout.addLayout(radio_buttons_row)
        exec_layout.addLayout(radio_layout)

        # Dropdown label
        stack_label = QLabel("Select stack")
        stack_label.setStyleSheet("""
            QLabel {
                color: #CFCFCF;
                background: transparent;
                font-size: 12px;
                font-weight : bold;
            }
        """)
        # stack_label.setFixedHeight(18)
        exec_layout.addWidget(stack_label)

        # Dropdown
        self.tech_stack = QComboBox()
        self.tech_stack.setFixedSize(600,40)
        self.tech_stack.addItem("BCA")
        self.tech_stack.addItem("Cerance")
        self.tech_stack.setStyleSheet("""
            QComboBox {
                background-color: #3B3B3B;
                color: white;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 4px;
                
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background-color: #3B3B3B;
                color: white;
                selection-background-color: #007ACC;
                selection-color: white;
            }
        """)
        exec_layout.addWidget(self.tech_stack)

        # ----- Action Buttons + Status -----
        btn_hbox = QHBoxLayout()
        self.test_btn = QPushButton("Start Test")
        self.test_btn.setFixedHeight(40)
        self.test_btn.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #005A99; }
            QPushButton:disabled { background-color: #3b3b3b; color: #999; }
        """)
        self.test_btn.clicked.connect(self.start_test)

        schedule_btn = QPushButton("Schedule")
        schedule_btn.setFixedHeight(40)
        schedule_btn.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #005A99; }
        """)
        schedule_btn.clicked.connect(lambda: self.create_and_schedule_task(
            ip=self.ip_path_edit.text(),
            excel=self.exe_path_edit.text(),
            dir=self.runnerlogDir,
            dlp=self.fp_path_edit.text(),
            load=self.give_load.isChecked(),
            stack=self.tech_stack.currentText(),
            time_str=self.time_input.text()
        ))

        btn_hbox.addWidget(self.test_btn)
        btn_hbox.addWidget(schedule_btn)

        label_group = QGroupBox()
        label_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        label_group.setStyleSheet(connection_group.styleSheet())
        label_layout = QVBoxLayout(label_group)

        self.status_label = QLabel("Time Remaining: 0s")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #CFCFCF;
                background: transparent;
                font-size: 12px;
                font-weight : bold;
            }
        """)
        label_layout.addWidget(self.status_label)

        # ----- Assemble Layout -----
        main_layout.addWidget(connection_group)
        main_layout.addWidget(file_group)
        main_layout.addWidget(exec_group)
        main_layout.addWidget(label_group)
        main_layout.addLayout(btn_hbox)

        return card

    def select_log_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Log Folder')
        if folder_path:
            self.log_path_edit.setText(folder_path)
            self.runnerlogDir = os.path.join(self.log_path_edit.text(), self.runnerlogDir)
            try:
                os.makedirs(self.runnerlogDir, exist_ok=True)
            except Exception as e:
                QMessageBox.critical(self, "Folder Error", f"Could not create log folder:\n{e}")

    # ----------------- Test flow -----------------
    def start_test(self):
        # Build core object 
        self.test_obj = Test_begin(
            mcu_ip=self.ip_path_edit.text(),
            input_excel=self.exe_path_edit.text(),
            directory=self.runnerlogDir,
            dlp_file=self.fp_path_edit.text(),
            load=self.give_load.isChecked(),
            stack=self.tech_stack.currentText()
        )

        # Initialize countdown from core's computed load_time
        self.rem_load_time = int(getattr(self.test_obj, 'load_time', 0) or 0)
        self.status_label.setText(f"Time Remaining: {self.rem_load_time}s")

        # Start UI timer (1 Hz)
        if self.timer:
            self.timer.stop()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

        #disabling the test button while test running
        self.test_btn.setDisabled(True)

        self.thread = QThread(self)
        self.worker = Worker(self.test_obj)
        self.worker.moveToThread(self.thread)

        # Wire signals
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_core_finished)
        self.worker.error.connect(self.on_core_error)

      
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.error.connect(self.thread.quit)
        self.worker.error.connect(self.worker.deleteLater)

        self.thread.start()

    def update_timer(self):
        # countdown while the worker runs
        if self.rem_load_time > 0:
            self.rem_load_time -= 1
            self.status_label.setText(f"Time Remaining: {self.rem_load_time}s")
        else:
            # just stop the timer; core may still be finishing up a second later
            self.timer.stop()

    @pyqtSlot()
    def on_core_finished(self):
        # Stop timer if still running
        if self.timer and self.timer.isActive():
            self.timer.stop()
        self.status_label.setText("✅ Test finished")
        self.test_btn.setDisabled(False)

    @pyqtSlot(str)
    def on_core_error(self, message: str):
        if self.timer and self.timer.isActive():
            self.timer.stop()
        self.status_label.setText("❌ Error during test")
        self.test_btn.setDisabled(False)
        QMessageBox.critical(self, "Test Error", message)

    # ----------------- Scheduler / BAT creation -----------------
    def create_and_schedule_task(self, ip, excel, dir, dlp, load, stack, time_str):
        if not time_str or ":" not in time_str:
            QMessageBox.warning(self, "Invalid Time", "Please enter time as HH:MM")
            return

        task_name = "MyAppTaskV1.0.1"
        python_exe = os.path.abspath(os.sys.executable)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, "TTS_main.py")

        # Quote paths
        excel_path = f'"{excel}"'
        dir_path = f'"{dir}"'
        dlp_path = f'"{dlp}"'

        bat_file = os.path.join(script_dir, f"{task_name}.bat")
        bat_content = f"""@echo off
cd /d "{script_dir}"
"{python_exe}" "{script_path}" --ip {ip} --excel {excel_path} --dir {dir_path} --dlp {dlp_path} --load {str(load).lower()} --tech {stack}
pause
"""

        try:
            with open(bat_file, "w", encoding="utf-8") as f:
                f.write(bat_content)
        except Exception as e:
            QMessageBox.critical(self, "BAT Error", f"Failed to write BAT file:\n{e}")
            return

        try:
            hour, minute = time_str.split(":")
        except ValueError:
            QMessageBox.warning(self, "Invalid Time", "Please enter time as HH:MM")
            return

        command = [
            "schtasks", "/Create",
            "/SC", "ONCE",
            "/TN", task_name,
            "/TR", f'"{bat_file}"',
            "/ST", f"{hour}:{minute}",
            "/F"
        ]

        try:
            subprocess.run(command, check=True)
            QMessageBox.information(self, "Scheduled", f"Task '{task_name}' scheduled at {time_str}")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Failed to schedule task:\n{str(e)}")

    # Optional helper (if you still want a standalone creator)
    def create_tts_bat(self, ip, excel_path, dir_path, dlp_path, load, tech, bat_name="run_tts"):
        python_exe = os.path.abspath(os.sys.executable)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, "TTS_main.py")

        excel_path = f'"{excel_path}"'
        dir_path = f'"{dir_path}"'
        dlp_path = f'"{dlp_path}"'

        bat_file = os.path.join(script_dir, f"{bat_name}.bat")
        bat_content = f"""@echo off
cd /d "{script_dir}"
"{python_exe}" "{script_path}" --ip {ip} --excel {excel_path} --dir {dir_path} --dlp {dlp_path} --load {str(load).lower()} --tech {tech}
pause
"""
        with open(bat_file, "w", encoding="utf-8") as f:
            f.write(bat_content)
        print(f"Batch file created at: {bat_file}")
        return bat_file
