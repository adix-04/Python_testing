import sounddevice as sd
import logging 
import subprocess
import os
import pandas as pd
from gtts import gTTS
from pydub.playback import play
import numpy as np
import io 
from pydub import AudioSegment

class WuWTest(object):
    def __init__(self,mcu_ip,input_excel,output_excel,lang,iteartions,directory):
        self.mcuIp = mcu_ip
        self.inputExcel = input_excel
        self.outputExcel = output_excel
        self.Lang = lang
        self.numIters = iteartions
        self.outDIr = directory
        self.command_wait_deviceStart="wait-for-device"

        self.audioDir = 'audio'

        logging.basicConfig(
                filename=f"{self.outDIr}/overall_log.txt",  
                filemode="w",  # if file exist, clear it then open and write
                level=logging.DEBUG,
                format="%(asctime)s:%(levelname)s:%(message)s",
                datefmt="%Y-%m-%d %I:%M:%S%p",
            )
        logging.Logger
    
    def main(self):
        print(self.inputExcel)
        print(self.mcuIp)
        print(self.outputExcel)
        print(self.Lang)
        print(self.outDIr)
        print(self.numIters)

    def test_init(self):
        command = 'adb devices'
        logging.info("Starting the WUW test run...")
        logging.info(f"The language now tested is {self.Lang}")
        adb_result=self.run_adb_command(f"connect {self.mcuIp}")
        adb_result=self.run_adb_command(self.command_wait_deviceStart)
        logging.info(adb_result)
        for i in range(3):
            result=subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                logging.error(f"adb command for devices failed, please check the error: {result.stderr.decode('utf-8')}")
                raise Exception(f'adb command failed failed: {result.stderr.decode("utf-8")}')
            if self.mcuIp in result.stdout.decode("utf-8"):
                logging.info(" the device is identified and adb can work")
                device_started=True
                break
            else:
                logging.error(f"The device is not identified , see the error: {result} ")
                print("device not found")
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
            return error  # or return a custom string if you want
        return output

     except Exception as e:
        print(f"[ERROR] Exception occurred while running adb: {e}")
        return str(e)

    def loadutterances(self,logger):
        df = pd.read_excel(self.inputExcel)
        print(df)
    
        for index, row in df.iterrows():
            utterance = row['Utterance']
            voice_type = row['Gender']
            lang_from_excel = row['Language']

            if self.Lang != lang_from_excel:
                continue

            if utterance:
                try:
                    print(f"Generating TTS for: {utterance}")
                    self.speak_utterance(text=utterance)

                    print(f"Played utterance {utterance}")
                    # Optionally save matched utterance

                except Exception as e:
                    logging.error(f"Failed to generate TTS for utterance '{utterance}': {e}")


    def speak_utterance(self,text, lang="en"):
        try:
            print(f"🔊 Speaking: {text}")
            tts = gTTS(text=text, lang=lang, slow=False)

            # Save MP3 to a bytes buffer (in-memory)
            mp3_fp = io.BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)

            # Load into pydub and play directly
            audio = AudioSegment.from_file(mp3_fp, format="mp3")
            play(audio)
            audio = gTTS(text=text,lang='ml',slow=False,tld="com.au")
            audio.save("output.mp3")
            os.system("mpg123 output.mp3")

        except Exception as e:
            print(f"Error: {e}")
