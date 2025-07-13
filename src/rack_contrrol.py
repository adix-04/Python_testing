# rack_controller.py
import serial
from time import sleep

class RackController:
    def __init__(self, port='COM3'):
        self.port = port
        self.ser = serial.Serial(port=self.port, baudrate=115200, bytesize=8,
                                 parity='N', stopbits=1, timeout=1)
        sleep(0.1)
        self.clamps = ["cl30", "cl30f", "cl30b", "mute", "obd"]
        self.on = {'cl30': "HFBS0", 'cl30f': "HFBSf", 'cl30b': "HFBSb", 'mute': "HFBSM", 'obd': "HFBSO"}
        self.off = {'cl30': "HFBC0", 'cl30f': "HFBCf", 'cl30b': "HFBCb", 'mute': "HFBCM", 'obd': "HFBCO"}
        self.status = {'cl30': "HFBG0", 'cl30f': "HFBGf", 'cl30b': "HFBGb", 'mute': "HFBGM", 'obd': "HFBGO"}

    def send_command(self, cmd):
        self.ser.write(cmd.encode() + b'\n')
        return self.ser.readline().decode()

    def clamp_action(self, clamp, action):
        if action == "FIRMWARE":
            return "Firmware version: " + self.send_command("SV").strip()
        elif action == "ON":
            self.send_command(self.on[clamp])
            return f"{clamp} turned ON"
        elif action == "OFF":
            self.send_command(self.off[clamp])
            return f"{clamp} turned OFF"
        elif action == "RESTART":
            self.send_command(self.off[clamp])
            sleep(1)
            self.send_command(self.on[clamp])
            return f"{clamp} restarted"
        elif action == "STATUS":
            status = self.send_command(self.status[clamp])
            state = "ON" if status[4] == "1" else "OFF"
            return f"{clamp} status: {state}"

    def start_all(self):
        logs = []
        for c in self.clamps[:3]:
            logs.append(self.clamp_action(c, "ON"))
        return logs

    def shutdown_all(self):
        logs = []
        for c in self.clamps[:3]:
            logs.append(self.clamp_action(c, "OFF"))
        return logs

    def close(self):
        self.ser.close()
