import os  
import sys  
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel, QLineEdit, QComboBox, QRadioButton, QButtonGroup  
from PyQt5.QtCore import QThread, pyqtSignal   #from another py file  
from datetime import datetime  
from PyQt5.QtGui import QIcon
from run import WuWTest
  
class KPIMeas_GUI(QWidget):  
    def __init__(self):  
        super(KPIMeas_GUI, self).__init__()  
        self.setWindowTitle('WUW Test Automation Runner')
        self.setWindowIcon(QIcon(":/icons/IAV_Logo.ico"))
        self.setGeometry(100, 100, 500, 400)
  
        self.timenow=datetime.now()  
        self.rundirectoryname="WUW_Recognition_Testrun_"+ self.timenow.strftime("%d_%m_%H_%M")  
        self.rundirectory = ""  
        self.txtfilepath = ""  
        self.excelfilepath = ""  
        self.report_name = "WUW_Recognition_Test_Report_IPA_.xlsx"  
        self.report_whole = None  
        self.lang = None  
        self.tech = None
        self.testCate = None  
        self.audio_path = None  
        self.excel_path = None  
        self.logs_path = None  
        self.ip = None  
        self.seatZone = False
        self.Iterations=5
        self.mic = ""
        self.delay = ""
  
        self.initUI()  
  
    def initUI(self):  
        self.main_layout = QVBoxLayout()  

        self.cate_label = QLabel("Select Test Category:")  
        self.main_layout.addWidget(self.cate_label) 

        self.cate_combo = QComboBox()  
        self.cate_combo.addItem("FRR Test")  
        self.cate_combo.addItem("FAR Test (ACA ONLY)")  
        self.main_layout.addWidget(self.cate_combo)  
  
        self.tech_label = QLabel("Select Tech Stack:")  
        self.main_layout.addWidget(self.tech_label)  

        self.tech_combo = QComboBox()  
        self.tech_combo.addItem("Cerence")  
        self.tech_combo.addItem("BCA")  
        self.tech_combo.addItem("LBCA") 
        self.main_layout.addWidget(self.tech_combo)  

        self.zone_choose = QLabel("Test with SeatZone features?")  
        self.main_layout.addWidget(self.zone_choose)
        self.trueSeatZone = QRadioButton("Yes (ACA ONLY)")
        self.falseSeatZone = QRadioButton("No")
        self.main_layout.addWidget(self.falseSeatZone)  
        self.falseSeatZone.setChecked(True)
        self.main_layout.addWidget(self.trueSeatZone)  


        self.zone_mic = QLabel("Select MIC:")  
        self.main_layout.addWidget(self.zone_mic)
        self.zone_mic = QComboBox()  
        self.zone_mic.addItem("FRONT_LEFT")  
        self.zone_mic.addItem("FRONT_RIGHT") 
        self.main_layout.addWidget(self.zone_mic)  

        self.delay_label = QLabel("Mic Delay (in ms)")  
        self.main_layout.addWidget(self.delay_label)  
        self.delay_entry = QLineEdit()  
        self.delay_entry.setText("200")
        self.main_layout.addWidget(self.delay_entry)  
  
        self.ip_label = QLabel("MCU IP Adress:")  
        self.main_layout.addWidget(self.ip_label)  
  
        self.ip_entry = QLineEdit()  
        self.ip_entry.setText('10.42.0.164:33255')
        self.main_layout.addWidget(self.ip_entry)  
  
        # self.audio_source_path_edit = QLineEdit(self)
        # #self.audio_source_path_edit.setMaximumWidth(100)
        # self.select_audio_button = QPushButton('Select Audio Source Folder', self)
        # self.select_audio_button.clicked.connect(self.select_audio_source_folder)
        # self.main_layout.addWidget(QLabel('Audio Source Path:'))
        # self.main_layout.addWidget(self.audio_source_path_edit)
        # self.main_layout.addWidget(self.select_audio_button)
  
        self.excel_label = QLabel("WUW List File:")  

        self.main_layout.addWidget(self.excel_label)  

      
        # Intent input file
        self.intent_file_edit = QLineEdit(self)
        self.intent_file_edit.setText('/home/adin.n@acsiatech.com/Downloads/4000-most-common-english-words-xlsx.xlsx')
        #self.intent_file_edit.setMaximumWidth(100)
        self.select_intent_file_button = QPushButton('Select WUW Input File', self)
        self.select_intent_file_button.clicked.connect(self.select_intent_input_file)
        self.main_layout.addWidget(self.intent_file_edit)
        self.main_layout.addWidget(self.select_intent_file_button)
  
        # Log folder
        self.log_folder_edit = QLineEdit(self)
        self.log_folder_edit.setText('/home/adin.n@acsiatech.com/Desktop/logs')
        #self.log_folder_edit.setMaximumWidth(100)
        self.select_log_folder_button = QPushButton('Select Log Folder', self)
        self.select_log_folder_button.clicked.connect(self.select_log_folder)
        self.main_layout.addWidget(QLabel('Log Folder:'))
        self.main_layout.addWidget(self.log_folder_edit)
        self.main_layout.addWidget(self.select_log_folder_button)
  
        self.report_label = QLabel("Report File Name:")  
        self.main_layout.addWidget(self.report_label)  
  
        self.report_entry = QLineEdit()  
        self.report_entry.setText(self.report_name)  
        self.main_layout.addWidget(self.report_entry)  

        
        self.IterationCount = QLineEdit()  
        self.IterationCount.setText("5")  
        self.main_layout.addWidget(self.IterationCount)  
  
        self.lang_label = QLabel("Select Language:")  
        self.main_layout.addWidget(self.lang_label)  
  
        self.lang_combo = QComboBox()  
        self.lang_combo.addItem("de_de")  
        self.lang_combo.addItem("en")  
        self.lang_combo.addItem("fr_ca")  
        self.lang_combo.addItem("en_uk")  
        self.lang_combo.addItem("es_mx")  
        self.lang_combo.addItem("nl_nl")  
        self.lang_combo.addItem("pt_pt")  
        self.lang_combo.addItem("it_it")  
        self.main_layout.addWidget(self.lang_combo)  
  
        self.start_button = QPushButton("Start Test")  
        self.start_button.clicked.connect(self.start_test)  
        self.main_layout.addWidget(self.start_button)  
  

        self.error_label = QLabel("")  
        self.main_layout.addWidget(self.error_label)  
           # Status Tooltip - Placeholder for simplicity
        self.status_tooltip = QLabel("Status: Idle")
        self.main_layout.addWidget(self.status_tooltip)
  
  
        self.setLayout(self.main_layout)  
  
    def select_audio_source_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Audio Source Folder')
        if folder_path:
            self.audio_source_path_edit.setText(folder_path)
            self.audio_path=folder_path
          
    def select_intent_input_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Select WUW Input File', '', 'Excel Files (*.xlsx *.xls)')
        if file_name:
            self.intent_file_edit.setText(file_name)
            self.excel_path=file_name

    def select_log_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Log Folder')
        if folder_path:
            self.log_folder_edit.setText(folder_path)
        self.rundirectory=os.path.join(self.log_folder_edit.text(),self.rundirectoryname)
        os.mkdir(self.rundirectory)

    def update_status(self, message):
        # Update the UI based on progress. Make sure updates here are thread-safe.
        # For example, updating status text:
        self.status_tooltip.setText(message)
        # Apply HTML styling to the message
        self.status_tooltip.setText(f'<h2><font color="red">{message}</font></h2>')

        # Additional styling, like setting background color, padding, etc.
        self.status_tooltip.setStyleSheet("background-color: lightgray; padding: 7px; border: 2px solid black; border-radius: 6px;")
        self.status_tooltip.setMargin(5)

  
    def start_test(self):  
        self.ip = self.ip_entry.text()
        self.report_name=self.report_entry.text()
        self.testCate = self.cate_combo.currentText()
        self.tech = self.tech_combo.currentText()  
        self.mic = self.zone_mic.currentText()
        self.delay = self.delay_entry.text()
        self.lang =self.lang_combo.currentText()
        self.logs_path=self.log_folder_edit.text()
        self.Iterations=self.IterationCount.text()
        self.seatZone = self.trueSeatZone.isChecked()
        self.report_whole = "\\" + self.report_name

        if self.testCate == "FRR Test":
            if self.excel_path and self.logs_path and self.tech != "Please selecet the Tech Stac here!" and self.ip and self.report_name and self.lang:
               self.update_status("Starting the test...")
               permission = True
            else:
               self.update_status("Please select all the paths / input & output file \n/ IP adress before starting the test.")
               permission = False
        if self.testCate == "FAR Test (ACA ONLY)":
            if self.logs_path and self.tech != "Please selecet the Tech Stac here!" and self.ip and self.report_name:
               self.update_status("Starting the test...")
               permission = True
            else:
               self.update_status("Please select all the paths / input & output file \n/ IP adress before starting the test.")
               permission = False
   
        if permission:
            if self.testCate == "FRR Test":
               self.update_status("Running FRR tests...")
               self.run_Wuw_FRR_Test()
            if self.testCate == "FAR Test (ACA ONLY)":
               self.update_status("Running FAR tests...")
               self.run_Wuw_FAR_Test()
        
   
    def run_Wuw_FAR_Test(self):
        self.args = "com.bmwgroup.assistant.alexa"
        if self.seatZone:
            if self.tech == "BCA":
                print("Running WUW FAR Test for BCA with Seat Zone Detection...\n")
            if self.tech == "LBCA":
                print("Running WUW FAR Test for LBCA with Seat Zone Detection...\n")
        else:
            if self.tech == "BCA":
                print("Running WUW FAR Test for BCA...\n")
            if self.tech == "LBCA":
                print("Running WUW FAR Test for LBCA...\n")
        # obj_wuwtest = WUWTest(self.tech, self.rundirectory, self.ip, self.excel_path, self.report_whole, self.audio_path,self.lang,self.Iterations,self.update_status,self.seatZone,self.mic,self.delay)
        # obj_wuwtest.test_init()
        # obj_wuwtest.WUWTest_FAR()
        obj_wuwtest = WuWTest(mcu_ip=self.ip,input_excel=self.excel_path,output_excel=self.report_whole,lang=self.lang,iteartions=self.Iterations,directory=self.rundirectory)
        obj_wuwtest.main()
        obj_wuwtest.test_init()

        print(f"Test Finished\n")
        self.update_status("WUW Measurement DONE")
    def run_Wuw_FRR_Test(self):
        if self.tech == "Cerence":
            self.args = "com.bmwgroup.speech.core"
            print("Running WUW FRR Test for Cerence...\n")
        else:
            self.args = "com.bmwgroup.assistant.alexa"
            if self.seatZone:
                if self.tech == "BCA":
                    print("Running WUW FRR Test for BCA with Seat Zone Detection...\n")
                if self.tech == "LBCA":
                    print("Running WUW FRR Test for LBCA with Seat Zone Detection...\n")
            else:
                if self.tech == "BCA":
                    print("Running WUW FRR Test for BCA...\n")
                if self.tech == "LBCA":
                    print("Running WUW FRR Test for LBCA...\n")
        # obj_wuwtest = WUWTest(self.tech, self.rundirectory, self.ip, self.excel_path, self.report_whole, self.audio_path,self.lang,self.Iterations,self.update_status,self.seatZone,self.mic,self.delay)
        # obj_wuwtest.test_init()
        # obj_wuwtest.WUWTest_FRR()
        obj_wuwtest = WuWTest(mcu_ip=self.ip,input_excel=self.excel_path,output_excel=self.report_whole,lang=self.lang,iteartions=self.Iterations,directory=self.rundirectory)
        obj_wuwtest.main()
        obj_wuwtest.test_init()

        print(f"Test Finished\n")
        self.update_status("WUW Measurement DONE")

if __name__ == '__main__':  
    app = QApplication(sys.argv)  
    ex = KPIMeas_GUI()  
    ex.show()  
    sys.exit(app.exec_())  