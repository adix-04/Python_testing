import pyttsx3
from gtts import gTTS
import Test_runner_GUI
import os
from PyQt5.QtWidgets import *
import pandas as pd
import time as t


class tts_main():
    cols =[0]
    def __init__(self):
        self.ui_obj = Test_runner_GUI.Ui_MainWindow()
        
    def tts_converter(self,command):
        audio = gTTS(text=command,lang='en',slow=False,tld="com.au")
        audio.save("output.mp3")
        os.system("mpg123 output.mp3")
    def file_iter(self,file_path):
        data = pd.read_excel(file_path,usecols=self.cols)
        print(data)
        for index,row in data.iterrows():
         self.tts_converter("Hey Mini")
         t.sleep(2)
         self.tts_converter(row['commands'])
    def warn(self,mesg):
         msg = QMessageBox()
         msg.setIcon(QMessageBox.Warning)
         msg.setText(mesg)
         msg.setWindowTitle('മുന്നറിയിപ്പ്')
         msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
         msg.exec_()
     
 
    
    #   engine = pyttsx3.init()
    #   engine.setProperty("rate", 150)
    #   engine.say(command)
    #   engine.runAndWait()
    #   print("speak"+command)
    # def parse_input(self):
    #    text = self.ui_obj.Input_words.text().strip()
    #    if text == ' ':
    #       print("fail") 
    #    else:
    #      self.tts_converter(text)
    #      print(text)
          
        
       

if __name__ == '__main__':
   pass


