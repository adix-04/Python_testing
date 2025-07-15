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
import threading
import time as time 
import re

class WuWTest(object):
    def __init__(self,mcu_ip,input_excel,output_excel,lang,iteartions,directory):
        self.mcuIp = mcu_ip
        self.inputExcel = input_excel
        self.outputExcel = output_excel
        self.Lang = lang
        self.numIters = iteartions
        self.outDIr = directory
        self.command_wait_deviceStart="wait-for-device"
        self.report_excel_file = "output_from_test_run.xlsx"


        self.report_excel_file = self.outDIr + self.report_excel_file


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

            if utterance:
                try:
                    print(f"Generating TTS for: {utterance}")
                    self.speak_utterance(text=utterance)
                    print(f"Played utterance {utterance}")

                except Exception as e:
                    print(e)
                    # logging.error(f"Failed to generate TTS for utterance '{utterance}': {e}")

    def speak_utterance(self, text, lang="en"):
      try:
        print(f"🔊 Speaking: {text}")
        tts = gTTS(text=text, lang=lang, slow=False)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        audio = AudioSegment.from_file(mp3_fp, format="mp3")

        # Start log collection thread
        stop_event = threading.Event()
        hitCount = [0]  # Mutable counter to collect hit info
        log_thread = threading.Thread(target=self.realtime_far_analyse, args=(hitCount, stop_event))
        log_thread.start()

        # Play the audio (this blocks until playback finishes)
        play(audio)
        logging.info(f"Played utterance: {text}")

        # Give a buffer after playback ends (to allow logs to come in)
        time.sleep(2)

        # Stop log collection
        stop_event.set()
        log_thread.join()

        logging.info(f"✅ Done with utterance '{text}'. Detected {hitCount[0]} WUWs.")
        print(f"[p] Done with utterance '{text}'. Detected {hitCount[0]} WUWs.")

      except Exception as e:
        print(f"Error during speak_utterance: {e}")

    def realtime_far_analyse(self,hitCount,stop_event):
        print("real time far check")
        log_file=f"{self.outDIr}/Target_log_WUW_FAR_Test.txt"
        columns = ['WUW','Shown on HMI','Selected MIC','Correct MIC?','Highest ranked MIC',  
                    'Ranking','Confidence','Standard Deviation','Conf.+StdDev','Avg(Conf.+StdDev)','GeoAvg(Conf, StdDev)',
                    'Other detected MIC', 'Ranking2', 'Confidence2', 'Standard Deviation2','Conf.+StdDev2','Avg(Conf.+StdDev)2','GeoAvg(Conf, StdDev)2']
        df = pd.DataFrame(columns=columns)
        with open(log_file, "w", encoding='ISO-8859-1') as file:
          print("opening logcat for device")
        #   process = subprocess.Popen(["adb", "-s", self.mcuIp, "logcat"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1, encoding='ISO-8859-1')
          process = subprocess.Popen(["adb" , "-s" ,"J7S8WCZTROEQ8L9D", "logcat"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1, encoding='ISO-8859-1')
          temp_data = {}
          while not stop_event.is_set():
            line = process.stdout.readline()
            file.writelines(f"{line}\n")
            file.flush()
            # if "SpeechRecognizerEngineImpl" in line and "newState=LISTENING" in line:
            if "Speech" in line :
                    if temp_data:
                        df.loc[len(df)] = [
                            temp_data.get('WUW', ''),
                            temp_data.get('Shown on HMI', False),
                            self.mic,
                            #temp_data.get('Detected?', False),
                            temp_data.get('Correct MIC?', False),
                            temp_data.get('Highest ranked MIC', ''),
                            temp_data.get('Ranking', ''),
                            temp_data.get('Confidence', ''),
                            temp_data.get('Standard Deviation', ''),
                            temp_data.get('Conf.+StdDev', ''),
                            temp_data.get('Avg(Conf.+StdDev)', ''),
                            temp_data.get('GeoAvg(Conf, StdDev)', ''),
                            temp_data.get('Other detected MIC', ''),
                            temp_data.get('Ranking2', ''),
                            temp_data.get('Confidence2', ''),
                            temp_data.get('Standard Deviation2', ''),
                            temp_data.get('Conf.+StdDev2', ''),
                            temp_data.get('Avg(Conf.+StdDev)2', ''),
                            temp_data.get('GeoAvg(Conf, StdDev)2', '')
                        ]
                        temp_data.clear()
                    temp_data['WUW'] = "BMW WUW"
                    temp_data['Shown on HMI'] = True
                    logging.info("WUW detected!") 
                    hitCount[0] += 1               
            if "getHighestRankedResult() Highest" in line:
                    temp_data['MIC'] = re.search("Highest: <Mic: (.*?),", line).group(1) if re.search("Highest: <Mic: (.*?),", line).group(1) else "No detection"
                    temp_data['Ranking'] = re.search("ranking: (.*?)>", line).group(1) if re.search("ranking: (.*?)>", line).group(1) else "No detection"
                    temp_data['Detected?'] = True
                    if temp_data['MIC'] == self.mic:
                        temp_data['Correct MIC?'] = True 
                    temp_data['Highest ranked MIC'] = temp_data['MIC']
                    logging.info(f"Mic: {temp_data['MIC']} detected, ranking is {temp_data['Ranking']}.")
            if "logRankings() 1 / 2: <Mic" in line:
                    match = re.search("ranking: \{ Total: (.*?), Conf: (.*?), StdDev: (.*?), Conf \+ StdDev: (.*?), Avg \(conf \+ stdDev\): (.*?), Geo avg \(conf, stdDev\): (.*?) \}",line)
                    temp_data['Confidence'] = match.group(2) if match.group(2) else "No detection"
                    temp_data['Standard Deviation'] = match.group(3) if match.group(3) else "No detection"
                    temp_data['Conf.+StdDev'] = match.group(4) if match.group(4) else "No detection"
                    temp_data['Avg(Conf.+StdDev)'] = match.group(5) if match.group(5) else "No detection"
                    temp_data['GeoAvg(Conf, StdDev)'] = match.group(6) if match.group(6) else "No detection"
                    logging.info(f"Confidence: {temp_data['Confidence']}, Standard Deviation: {temp_data['Standard Deviation']}, Conf.+StdDev: {temp_data['Conf.+StdDev']}, Avg(Conf.+StdDev): {temp_data['Avg(Conf.+StdDev)']}, GeoAvg(Conf, StdDev): {temp_data['GeoAvg(Conf, StdDev)']}.")

            if "logRankings() 2 / 2: <Mic" in line:
                    match = re.search("Mic: (.*?), ranking: \{ Total: (.*?), Conf: (.*?), StdDev: (.*?), Conf \+ StdDev: (.*?), Avg \(conf \+ stdDev\): (.*?), Geo avg \(conf, stdDev\): (.*?) \}",line)
                    temp_data['Other detected MIC'] = match.group(1) if match.group(1) else "No detection"
                    temp_data['Ranking2'] = match.group(2) if match.group(2) else "No detection"
                    temp_data['Confidence2'] = match.group(3) if match.group(3) else "No detection"
                    temp_data['Standard Deviation2'] = match.group(4) if match.group(4) else "No detection"
                    temp_data['Conf.+StdDev2'] = match.group(5) if match.group(5) else "No detection"
                    temp_data['Avg(Conf.+StdDev)2'] = match.group(6) if match.group(6) else "No detection"
                    temp_data['GeoAvg(Conf, StdDev)2'] = match.group(7) if match.group(7) else "No detection"
                    logging.info(f"Other MIC: {temp_data['Other detected MIC']}, Ranking: {temp_data['Ranking2']}, Confidence: {temp_data['Confidence2']}, Standard Deviation: {temp_data['Standard Deviation2']}, Conf.+StdDev: {temp_data['Conf.+StdDev2']}, Avg(Conf.+StdDev): {temp_data['Avg(Conf.+StdDev)2']}, GeoAvg(Conf, StdDev): {temp_data['GeoAvg(Conf, StdDev)2']}.")
                
            else:
                if "SpeechRecognizerEngineImpl" in line and "newState=LISTENING" in line:
                    logging.info("WUW detected!")
                    hitCount[0] += 1
        process.terminate()
        if temp_data:
            print("temp data is true")
            df.loc[len(df)] = [
                temp_data.get('WUW', ''),
                temp_data.get('Shown on HMI', False),
                self.mic,
                #temp_data.get('Detected?', False),
                temp_data.get('Correct MIC?', False),
                temp_data.get('Highest ranked MIC', ''),
                temp_data.get('Ranking', ''),
                temp_data.get('Confidence', ''),
                temp_data.get('Standard Deviation', ''),
                temp_data.get('Conf.+StdDev', ''),
                temp_data.get('Avg(Conf.+StdDev)', ''),
                temp_data.get('GeoAvg(Conf, StdDev)', ''),
                temp_data.get('Other detected MIC', ''),
                temp_data.get('Ranking2', ''),
                temp_data.get('Confidence2', ''),
                temp_data.get('Standard Deviation2', ''),
                temp_data.get('Conf.+StdDev2', ''),
                temp_data.get('Avg(Conf.+StdDev)2', ''),
                temp_data.get('GeoAvg(Conf, StdDev)2', '')
            ]
            print("gonna save the file")
            df.to_excel(self.report_excel_file, index=False)
