import sys
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QHBoxLayout 
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
        # Close existing connection if open
        if hasattr(self, "ser") and self.ser.is_open:
            print('self.ser.close()')

        try:
            self.ser = serial.Serial(
                port='COM3',
                baudrate=115200,
                bytesize=8,
                parity='N',
                stopbits=1,
                timeout=1
            )
            self.st_msg = "Rack Connected"
            print("connected")
            if hasattr(self, "rack_status"):
                self.rack_status.setText(self.st_msg)
                self.rack_status.setStyleSheet("font-size: 22px; font-weight: bold; color: lime;")

        except serial.SerialException:
            self.st_msg = "Rack disconnected"
            print(" serial.SerialException disconnected")
            if hasattr(self, "rack_status"):
                self.rack_status.setText(self.st_msg)
                self.rack_status.setStyleSheet("font-size: 22px; font-weight: bold; color: red;")

        except Exception:
            print( ' Exception disconnected')
            self.st_msg = "Rack Disconnected"
            if hasattr(self, "rack_status"):
                self.rack_status.setText(self.st_msg)
                self.rack_status.setStyleSheet("font-size: 22px; font-weight: bold; color: red;")

            
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # === Title ===
        title = QLabel("Device Control Panel")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: white;")
        layout.addWidget(title)

        # === Rack Status ===
        self.rack_status = QLabel(self.st_msg)
        self.rack_status.setAlignment(Qt.AlignCenter)
        self.rack_status.setStyleSheet("font-size: 22px; font-weight: bold; color: red;")
        layout.addWidget(self.rack_status)

        # === Button Styles ===
        btn_style_on = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 6px;
                min-width: 100px;
                min-height: 40px;
            }
            QPushButton:hover { background-color: #45A049; }
            QPushButton:pressed { background-color: #2E7D32; }
        """
        btn_style_off = """
            QPushButton {
                background-color: #F44336;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 6px;
                min-width: 100px;
                min-height: 40px;
            }
            QPushButton:hover { background-color: #E53935; }
            QPushButton:pressed { background-color: #B71C1C; }
        """

        # === Grid Layout for Controls ===
        grid = QGridLayout()
        grid.setSpacing(15)

        button_names = ['Mute', 'OBD', 'CL30', 'CL30F', 'CL30B']
        for row, name in enumerate(button_names):
            label = QLabel(name)
            label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")

            btn_on = QPushButton("ON")
            btn_on.setStyleSheet(btn_style_on)
            btn_on.clicked.connect(lambda _, idx=row: self.send_command(idx, True))
            grid.addWidget(label, row, 1, alignment=Qt.AlignRight)

            grid.addWidget(btn_on, row, 0)

            btn_off = QPushButton("OFF")
            btn_off.setStyleSheet(btn_style_off)
            btn_off.clicked.connect(lambda _, idx=row: self.send_command(idx, False))
            grid.addWidget(btn_off, row, 2)

        # === Wrap grid in a centered container ===
        grid_container = QWidget()
        grid_container.setLayout(grid)
        grid_layout = QHBoxLayout()
        grid_layout.addStretch()
        grid_layout.addWidget(grid_container)
        grid_layout.addStretch()
        layout.addLayout(grid_layout)

        # === Refresh Button Centered ===
        ref_btn = QPushButton("🔄 Refresh")
        ref_btn.setFixedHeight(40)
        ref_btn.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 6px 12px;
                min-width: 50px;
            }
            QPushButton:hover { background-color: #005A99; }
            QPushButton:pressed { background-color: #004C80; }
        """)
        ref_btn.clicked.connect(self.connect)
        layout.addWidget(ref_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)


    def send_command(self, button_idx, turn_on):
        """Send ON or OFF command directly ."""
        cmd = self.button_commands[button_idx][0] if turn_on else self.button_commands[button_idx][1]
        self.ser.write(cmd.encode() + b'\n')


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
