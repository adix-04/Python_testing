import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel  
)
from PyQt5.QtCore import Qt
import serial


class ButtonControl(QWidget):
    
    def __init__(self):
        self.st_msg = ''
        super().__init__()
            # self.rack_status.setText("RACK NOT CONNECTED") 
        # Button commands: [ON, OFF] for each button
        self.button_commands = [
            ["HFBSM", "HFBCM"],  # Mute
            ["HFBSO", "HFBCO"],  # OBD
            ["HFBS0", "HFBC0"],  # CL30
            ["HFBSf", "HFBCf"],  # CL30F
            ["HFBSb", "HFBCb"]   # CL30B
        ]
        
        self.button_states = [False] * 5  #Track ON/OFF states
        self.connect()
        self.init_ui()
    def connect(self):
        try:
            self.ser = serial.Serial(port='COM7', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1) 
            self.st_msg = "Rack Connected" 
            print('connected')
            self.init_ui()
        except serial.SerialException:
            print('disconnected')
            self.st_msg = "Rack disconnected"
            self.init_ui()
            
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)
        # Title
        title = QLabel("Device Control Panel")
        title.setAlignment(Qt.AlignCenter)
        self.rack_status = QLabel(self.st_msg)
        self.rack_status.setStyleSheet("font-size: 24px; font-weight: bold;color:red;")
        self.rack_status.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;color:white;")
        layout.addWidget(title)
        layout.addWidget(self.rack_status)
        
        # Button names
        button_names = ['Mute', 'OBD', 'CL30', 'CL30F', 'CL30B']
        # Create buttons
        self.buttons = []
        for i, name in enumerate(button_names):
            btn = QPushButton(f"{name} ")
            btn.setFixedSize(200, 60)
            btn.setCheckable(True)
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #f0f0f0;
                    border: 2px solid #333;
                    border-radius: 10px;
                    font-size: 16px;
                }
                QPushButton:checked {
                    background-color: #66bb6a;
                    color: white;
                }
                """
            )
            btn.clicked.connect(lambda _, idx=i: self.toggle_button(idx))
            layout.addWidget(btn, alignment=Qt.AlignCenter)
            self.buttons.append(btn)
        ref_btn = QPushButton('Refresh')
        ref_btn.setFixedSize(250, 30)
        ref_btn.setStyleSheet(
            """
                QPushButton {
                    background-color: #f0f0f0;
                    border: 2px solid #333;
                    border-radius: 10px;
                    font-size: 10px;
                }
                 QPushButton:pressed {
                    background-color: #66bb6a;
                    color: white;
                } """
                )
        ref_btn.clicked.connect(self.connect)
        layout.addWidget(ref_btn)
        self.setLayout(layout)

    def toggle_button(self, button_idx):
        is_on = self.button_states[button_idx]
        
        if is_on:
            cmd = self.button_commands[button_idx][1]  # OFF command
            self.buttons[button_idx].setText(f"{self.buttons[button_idx].text().split(' (')[0]} ")
        else:
            cmd = self.button_commands[button_idx][0]  # ON command
            self.buttons[button_idx].setText(f"{self.buttons[button_idx].text().split(' (')[0]} ")
        
        self.button_states[button_idx] = not is_on
        self.ser.write(cmd.encode() + b'\n')

    def closeEvent(self, event):
        self.ser.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ButtonControl()
    window.show()
    sys.exit(app.exec_())
