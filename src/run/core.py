import time
import random

class Test_begin:
    def __init__(self, mcu_ip, input_excel, directory, dlp_file, load, stack):
        self.mcuIp = mcu_ip
        self.inputExcel = input_excel
        self.outDIr = directory
        self.dlp = dlp_file
        self.load = load
        self.stack = stack

        # Simulate calculating load_time from Excel contents
        # Instead of reading Excel, just use random seconds for demo
        time.sleep(1)  # pretend some heavy processing
        self.load_time = random.randint(10, 30)  # total seconds
