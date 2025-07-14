
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QMovie
import os
import sys
from gtts import gTTS
import speech_recognition as sr
import pandas as pd
import subprocess
import signal
import platform
import time as t
import pyttsx3
import TTS_main


cols = [0]
filename = ''
class Ui_MainWindow(object):
    filename = ''
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(446, 423)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: #272e2a")
        self.Speak_button = QtWidgets.QPushButton(self.centralwidget)
        self.Speak_button.setGeometry(QtCore.QRect(360, 330, 81, 31))
        self.Speak_button.setObjectName("Speak_button")
        self.Speak_button.setStyleSheet("""
            background-color: %s;
            padding: 1px;
            margin: 4px;
            border-radius: 6px;
        """ % ("#01ff01"))
        self.Input = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.Input.setGeometry(QtCore.QRect(0, 330, 351, 31))
        self.Input.setPlaceholderText("")
        self.Input.setObjectName("Input")
        self.Input.setStyleSheet("background-color: #545755")
        self.anim = QtWidgets.QLabel(self.centralwidget)
        self.anim.setGeometry(QtCore.QRect(70, 10, 431, 231))
        self.anim.setObjectName("anim")
        self.movie = QMovie("ld.gif")
        self.anim.setMovie(self.movie)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 270, 191, 27))
        self.pushButton_2.setObjectName("FileSlector")
        self.pushButton_2.setStyleSheet("""
            background-color: %s;
            padding: 1px;
            margin: 4px;
            border-radius: 6px;
        """ % ("#08c6f5"))
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(250, 270, 91, 27))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setStyleSheet("""
            background-color: %s;
            padding: 1px;
            margin: 4px;
            border-radius: 6px;
        """ % ("#01ff01"))
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(350, 270, 91, 27))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setStyleSheet("""
            background-color: %s;
            padding: 1px;
            margin: 4px;
            border-radius: 6px;
        """ % ("#ff0000"))
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 300, 431, 20))
        self.label.setStyleSheet("color :#ffffff")
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 446, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.retranslateUi(MainWindow)
        self.pushButton_2.clicked.connect(self.file)
        self.Speak_button.clicked.connect(self.speak)
        self.pushButton_3.clicked.connect(self.start_btn)
        self.pushButton_4.clicked.connect(self.exit)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Speak_button.setText(_translate("MainWindow", "Speak"))
        self.pushButton_2.setText(_translate("MainWindow", "Select File"))
        self.pushButton_3.setText(_translate("MainWindow", "Start"))
        self.pushButton_4.setText(_translate("MainWindow", "stop"))
        self.label.setText(_translate("MainWindow", "selected file:"))

    def animation_area(self):
        self.movie.start()
        
    def file(self):
      file_dialog = QFileDialog()
      file_dialog.setWindowTitle("Open File")
      file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
      file_dialog.setViewMode(QFileDialog.ViewMode.Detail)
      if file_dialog.exec():
         selected_files = file_dialog.selectedFiles()
         print("Selected File:", selected_files[0])
         self.filename = selected_files[0]
         self.label.setText(selected_files[0])
         print(self.filename)
    def start_btn(self):
        if self.filename.endswith('xlsx' or 'xls'):
            print("excel file found")
        else:
            self.warn(mesg="No file selected")
            return
        syestem = platform.system()
        print(syestem)
        # try:
        #     while subprocess.check_output(["fuser",self.filename], text=True):
        #         check_st(filename=self.filename,system=syestem)  
        # except subprocess.CalledProcessError:
        #     print("File is not open by any process. Proceeding.")
       
        file_iteration(filename=self.filename)
    def exit(self):
        sys.exit()
    def speak(self):
        text = self.Input.toPlainText()
        if text == '':
            self.warn(mesg="Enter some text to continue")
            return
        self.animation_area()
        tts_converter(text)
        self.Input.clear()
       # listen()
    def warn(self,mesg):
         msg = QMessageBox()
         msg.setIcon(QMessageBox.Warning)
         msg.setText(mesg)
         msg.setWindowTitle('Warning')
         msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
         msg.exec_()
        
def tts_converter(command):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.say(command)
    engine.runAndWait()


def listen():
    print("\033[1m\033[33;32m[-]audio played , listening now . . .")
    recognizer = sr.Recognizer()
    converted_text = "Empty"
        # for index,name in enumerate(sr.Microphone.list_microphone_names()):
        #     print(f"{index} , {name}")
    with sr.Microphone(device_index=4)as inputsource:
        print("\033[1m\033[33;32m[+]listening for audio...")
        recognizer.adjust_for_ambient_noise(inputsource,duration=.5)
        voiceinput = recognizer.record(inputsource,duration=10)
    try:
        converted_text = recognizer.recognize_google(voiceinput)
        print("\033[1m\033[33;32m[+]user said ,",converted_text)
    except KeyboardInterrupt:
        print("\033[1m\033[33;32mKeyboard : interupt happened")
        exit(0)
    except sr.exceptions.UnknownValueError:
        print("\033[1m\033[33;32m[*]exception : user said nothing")
        print(f'User said {converted_text}')
        return converted_text
    
def check_st(filename,system):
    if system == 'Linux':
        try: 
                output = subprocess.check_output(["fuser",filename], text=True)
                #print(output)
                lines = output.strip().split("/")  # Skip the header
                for line in lines:
                    print(line)
                    parts = line.split()
                    pid = int(parts[0])
                    print(f"File is open by PID {pid}, killing it...")
                    os.kill(pid, signal.SIGKILL)
                    print(f"Process {pid} killed.")
        except subprocess.CalledProcessError:
            print("File is not open by any process. Proceeding.")
            file_iteration(filename=filename)
    elif system == 'Windows':
            print('windows')

def file_iteration(filename):
    print(filename)
    data = pd.read_excel(filename,usecols=cols)
    print(data)
    for index,row in data.iterrows():
        tts_converter("Hey Mini")
        tts_converter(row['commands'])
        TTS_main.print_fun()
        t.sleep(5)
        # result = listen()
        # data.at[index,'Results'] = f'{result}'
        # data.to_excel('words.xlsx',index=False,engine='openpyxl')
        # print(result)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())





























        # self.Chat_scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        # self.Chat_scrollArea.setGeometry(QtCore.QRect(0, 0, 441, 261))
        # self.Chat_scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        # self.Chat_scrollArea.setWidgetResizable(True)
        # self.Chat_scrollArea.setObjectName("Chat_scrollArea")
        # self.Chat_container = QtWidgets.QWidget()
        # self.Chat_container.setGeometry(QtCore.QRect(0, 0, 439, 259))
        # self.Chat_container.setObjectName("Chat_container")
        # self.verticalLayoutWidget = QtWidgets.QWidget(self.Chat_container)
        # self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 441, 261))
        # self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        # self.caht_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        # self.caht_layout.setContentsMargins(0, 0, 0, 0)
        # self.caht_layout.setObjectName("caht_layout")
        # self.caht_layout.addStretch()
        # self.Chat_scrollArea.setWidget(self.Chat_container)