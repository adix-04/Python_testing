import sounddevice as sd
import logging 
import subprocess
import os
import pandas as pd
from gtts import gTTS
from pydub.playback import play
import getpass
import pyttsx3
from Update_Excel import Update_Excel
import threading
import time as time 
import re
from datetime import datetime
from Connect_DLT import Connet_DLT_class
import utils
from pathlib import Path
import re

class Test_begin(object):
    def __init__(self,mcu_ip,input_excel,directory,dlp_file,load,stack):
        self.mcuIp = mcu_ip
        self.inputExcel = input_excel
        self.outputExcel = f"Test_run_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
        self.Lang = 'en'
        self.numIters = 5
        self.outDIr = directory
        self.load = load
        #self.outDIr = self.outDIr + f"/Test_run_on_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        self.command_wait_deviceStart="wait-for-device"
        self.report_excel_file = "output_from_test_run.xlsx"
        self.report_excel_file = self.outDIr + self.report_excel_file
        self.dlp = dlp_file
        self.excel = Update_Excel()
        self.cache = f'C:/Users/{getpass.getuser()}/AppData/Local/dlt_viewer/cache'
        self.audioDir = 'audio'
        self.load_process = None


        self.utils = utils.tts_main()

        logging.basicConfig(
                filename=f"{self.outDIr}/overall_log.txt",  
                filemode="w",  # if file exist, clear it then open and write
                level=logging.DEBUG,
                format="%(asctime)s:%(levelname)s:%(message)s",
                datefmt="%Y-%m-%d %I:%M:%S%p",
            )
        logging.Logger

        self.newDlp = self.dlpfile_constructor('artifacts/file_DLT.dlp',self.mcuIp)
        self.dlt = Connet_DLT_class(self.cache,self.newDlp,self.outDIr)
        print(self.newDlp)
        self.main()
        self.test_init()
    
    def main(self):
        print(self.inputExcel)
        print(self.mcuIp)
        print(self.outputExcel)
        print(self.Lang)
        print(self.outDIr)
        print(self.numIters)
        print(self.load)

    def test_init(self):
        command = 'adb devices'
        logging.info("Starting the WUW test run...")
        logging.info(f"The language now tested is {self.Lang}")
        adb_result=self.run_adb_command(f"connect {self.mcuIp}")
        adb_result=self.run_adb_command(self.command_wait_deviceStart)
        print("after adb connect call")
        logging.info(adb_result)
        # for i in range(3):
        #     result=subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #     if result.returncode != 0:
        #         logging.error(f"adb command for devices failed, please check the error: {result.stderr.decode('utf-8')}")
        #         raise Exception(f'adb command failed failed: {result.stderr.decode("utf-8")}')
        #     if self.mcuIp in result.stdout.decode("utf-8"):
        #         logging.info(" the device is identified and adb can work")
        #         device_started=True
        #         break
        #     else:
        #         logging.error(f"The device is not identified , see the error: {result} ")
                #  print("device not found")
        logging.info("Now setting the audio outdevices")
        if self.inputExcel != None:
          self.loadutterances(logging)

    def run_adb_command(self, command):
     if "connect" in command:
        adb_command = "adb " + command
     else:
        adb_command = "adb -s " + self.mcuIp + " " + command

     try:
        result = subprocess.run(adb_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        error = result.stderr.decode('utf-8')

        if result.returncode != 0:
            print(f"[WARNING] ADB command failed: {error.strip()}")
            return error  
        return output

     except Exception as e:
        print(f"[ERROR] Exception occurred while running adb: {e}")
        return str(e)

    def loadutterances(self,logger):
        df = pd.read_excel(self.inputExcel)
        '''doing some maths here to calculate how much time of load we need to give based on how much of utterance we have'''
        load_time = (df.size) * 14  
        
        if self.load:
            print("give load")
            logging.info("Going to give some cpu stress")
            adb_thread = threading.Thread(target= lambda : self.run_load_adb_command(time=load_time))
            adb_thread.start()
        
        # print(df)
        for index, row in df.iterrows():
            utterance = row['Utterances']
            if utterance:
                try:
                    # print(f"Generating TTS for: {utterance}")
                    self.speak_utterance(text=utterance)
                    print(f"Played utterance {utterance}")
                except Exception as e:
                    print(e)
        # self.utils.warn(mesg="Test Completed ")
        self.utils.warn(mesg="Test Completed ")
        if self.load:
            try:
                if hasattr(self, 'load_process') and self.load_process and self.load_process.poll() is None:
                    self.load_process.terminate()
                print("ADB process terminated early.")
            except Exception as e:
                print(f"Error terminating ADB process: {e}")
            adb_thread.join()
    def tts(self,text):
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(text)
        engine.runAndWait()

    def speak_utterance(self, text, lang="en"):
        self.run_adb_command('shell input keyevent KEYCODE_HOME')
        self.dlt.cleaner()
        if self.load:
            print("give load")
            # self.run_adb_command('shell "/data/local/tmp/stressapptest-aarch64 -s 600 -M 1000 -m 2 -C 1 -W -n 127.0.0.1 --listen -i 1 --findfiles -f /data/local/tmp/file1 -f /data/local/tmp/file2"')
        # Start log collection thread and also do a clean up
          # Start log collection thread and also do a clean up
        stop_event = threading.Event()
        log_thread = threading.Thread(target=self.dlt.start_dlt)
        log_thread.start()

        time.sleep(1)

        self.run_adb_command('shell cmd car_service inject-custom-input 1012;sleep 0.2; cmd car_service inject-custom-input 1013')
        time.sleep(1)
        print(f"🔊 Speaking: {text}")
        self.tts(text)
        logging.info(f"Played utterance: {text}")
        time.sleep(10)

        stop_event.set()
        log_thread.join()
        self.dlt.stop_dlt()
        self.dlt.convert_dlt_log_text()
        self.dlt.check(uttearnce=text)
        # print("Gonna call the main thing here")
        time.sleep(1)
        logging.info(f"✅ Done with utterance '{text}'")
        print(f"[+] Done with utterance '{text}'")
        
    def run_load_adb_command(self,time):
        self.load_process = subprocess.Popen([
            "adb", "-s", "169.254.80.235", "shell", "/data/local/tmp/stressapptest-aarch64",
            "-s", str(time) , "-M", "600", "-m", "2", "-C", "1", "-W", "-n", "127.0.0.1",
            "--listen", "-i", "1", "--findfiles", "-f", "/data/local/tmp/file1", "-f", "/data/local/tmp/file2"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    def dlpfile_constructor(self,original_path,new_hostname):
         """
        Creates a new DLP file with updated hostname 
        
        Args:
            original_path (str): Path to the original DLP file
            new_hostname (str): New hostname to set (must be valid IP)
        """
         try:
            if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', new_hostname):
                raise ValueError(f"Invalid IP address format: {new_hostname}")
            
            # Read the original file content
            with open(original_path, 'r') as file:
                content = file.read()
            
            updated_content = re.sub(
                r'<hostname>(.*?)</hostname>|hostname>(.*?)<', 
                f'<hostname>{new_hostname}</hostname>', 
                content,
                flags=re.DOTALL
            )
            
            # Create new filename with sanitized IP
            original_file = Path(original_path)
            hostname_with_dash = new_hostname.replace('.', '-')
            new_filename = f"{original_file.stem}_{hostname_with_dash}{original_file.suffix}"
            
            # Check if file already exists
            if os.path.exists(new_filename):
                raise FileExistsError(f"Output file{new_filename} already exists")
            
            # Write the new file
            with open(new_filename, 'w') as file:
                file.write(updated_content)
                
            print(f"Successfully created: {new_filename}")
            
            
            return new_filename
            
         except FileNotFoundError:
            print(f"Error: File not found at {original_path}")
            return None
         except Exception as e:
            print(f"Error: {str(e)}")
            return None


        
if __name__ == '__main__':
   parser = argparse.ArgumentParser(description="run tts functions in headless mode")
   parser.add_argument('--ip',type=str,required=True,help="ip address of the ECU")
   parser.add_argument('--excel',type=str,required=True,help="excel containing utterances")

   args = parser.parse_args()

    print(f"Hello, {args.name}!")
    print(f"You are {args.age} years old.")