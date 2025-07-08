import re
import threading
import time
import pygame
import numpy as np
from pydub import AudioSegment
import logging
import pandas as pd
import os
import subprocess
import sounddevice as sd
import datetime
from datetime import datetime

#from WUW_rest_time_calculator import extract_remaining_audio_duratio

class WUWTest(object):
    def __init__(self, tech, directory, mcuip, iexcelpath, oexcelname, audiopath, lang, iterations, updatesignal, seatZone, mic, delay):
        # initialize pygame mixer
        pygame.mixer.init()
        self.tech = tech
        self.rundirectory= directory #r"D:\00_Haonan_KE\04_KPITest"
        self.matched_utterances = dict()
        self.voiceTypes=dict()
        self.Iterationcocunt=iterations
        self.Intent_KPI_Values = dict()
        self.command_wait_deviceStart="wait-for-device"
        #self.ip='169.254.143.18'
        self.ip = mcuip #'169.254.8.177'
        #self.output_device= "Main Output 1/2 (Audient EVO8)"
        #self.windows_sound_host= "MME"
        #self.input_device= "Mic | Line 1/2 (Audient EVO8)"
        #self.input_excel_file=r"D:\test_automation\KPI_Test\input_intent.xlsx"
        self.input_excel_file = iexcelpath #r"D:\00_Haonan_KE\04_KPITest\input_intent.xlsx"
        self.report_excel_file = oexcelname
        self.audio_folder_path = audiopath #r"D:\00_Haonan_KE\04_KPITest\Audio"
        self.language=lang
        self.UpdateSignal=updatesignal
        self.seatZone = seatZone
        self.mic = mic
        self.delay = delay


        self.report_excel_file = self.rundirectory + self.report_excel_file

        self.test_finished = False

        print(self.tech)
        print(self.rundirectory)
        print(self.ip)
        print(self.Iterationcocunt)
        print(self.input_excel_file)
        print(self.report_excel_file)

    ############################# Init of the logger 
        logging.basicConfig(
                filename=f"{self.rundirectory}/overall_log.txt",  
                filemode="w",  # if file exist, clear it then open and write
                level=logging.DEBUG,
                format="%(asctime)s:%(levelname)s:%(message)s",
                datefmt="%Y-%m-%d %I:%M:%S%p",
            )
        logging.Logger
        self.test_init()

    def test_init(self):
        command = 'adb devices'
        logging.info("Starting the WUW test run...")
        logging.info(f"The language now tested is {self.language}")
        adb_result=self.run_adb_command(f"connect {self.ip}")
        adb_result=self.run_adb_command(self.command_wait_deviceStart)
        logging.info(adb_result)
        for i in range(3):
            result=subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                logging.error(f"adb command for devices failed, please check the error: {result.stderr.decode('utf-8')}")
                raise Exception(f'adb command failed failed: {result.stderr.decode("utf-8")}')
            if self.ip in result.stdout.decode("utf-8"):
                logging.info(" the device is identified and adb can work")
                device_started=True
                break
            else:
                logging.error(f"The device is not identified , see the error: {result} ")
                print("device not found")
        #logging.info("Now setting the audio outdevices")
        # self.setvirtualaudiodevices(logging)
        if self.input_excel_file != None:
          self.loadutterances(logging)

    def run_adb_command(self,command):
        if "connect" in command:
            adb_command="adb"+" "+command
        else:
            adb_command = "adb -s "+self.ip+" "+command
        result = subprocess.run(adb_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Check if the command failed
        if result.returncode != 0:
            raise Exception(f'ADB command failed: {result.stderr.decode("utf-8")}')
    
        return result.stdout.decode('utf-8')
    
    def setvirtualaudiodevices(self,logger):
        # Query all devices
        devices = sd.query_devices()
        hostapis = sd.query_hostapis()
        ## get the index of the voicemeter virtual devices

        for i, device in enumerate(devices):
            if((device['name'] == self.output_device) and (hostapis[device['hostapi']]['name'] ==self.windows_sound_host) ):
                print(f"{i}: {device['name']}")
                output_device_index = i
            if(device['name'] == self.input_device and (hostapis[device['hostapi']]['name'] ==self.windows_sound_host)):
                print(f"{i}: {device['name']}")
                input_device_index=i

        # Set the default devices
        sd.default.device =[input_device_index, output_device_index]
        logger.info("The currently set input/output devices are "+self.input_device +"and"+self.output_device)
        return 1
    
    def loadutterances(self,logger):
        df = pd.read_excel(self.input_excel_file)
        total_audio=0
        # get list of audio files
        audio_files = [f for f in os.listdir(self.audio_folder_path) if f.endswith('.mp3')]  # get audio file names and put then in a list -> e.g. [file1.wav, file2.wav, <...>]
        
      
        # iterate over values in column A
        for index,row in df.iterrows():
            # get the cell value
            utterance = row['Utterance']
            voice_type=row['Gender']
            lang_from_excel=row['Language']
            filename_excel=row['AudioFile']
            if self.language != lang_from_excel:    # to find matched utterance in excel with correct language
                continue
            if(utterance):
                # check if this name is in any of the audio files
                for audiofile in audio_files:  # audiofile(string) is a single element in the list "audio_files" -> e.g. file1.wav
                    if self.language not in audiofile :
                        continue
                    filename=os.path.splitext(audiofile)[0]        # e.g. de_de_Intent_Wakeword_1.mp3 -> de_de_Intent_Wakeword_1
                    filename_excel=filename_excel.split('/')[-1]   # e.g. utterances/Alexa/it_it/ReadSpeaker/de_de_Intent_Wakeword_1.mp3 -> de_de_Intent_Wakeword_1.mp3
                    filename_excel=filename_excel.split('.')[0]    # e.g. de_de_Intent_Wakeword_1.mp3 -> de_de_Intent_Wakeword_1
                    # Load the actuall utterance to the file if exists in Title of mp3 file
                    '''if "wav" in audiofile:
                        # Load the WAV file metadata
                        audiofiledata = TinyTag.get(os.path.join(self.audio_folder_path, audiofile))
                    else:
                        #audiofiledata = eyed3.load(os.path.join(self.audio_folder_path, audiofile)) 
                        audiofiledata = TinyTag.get(os.path.join(self.audio_folder_path, audiofile))
                    
                    if (audiofiledata.tag == None):
                        utterance_from_mp3="No data found"
                    else:
                        utterance_from_mp3=audiofiledata.tag.title'''
                    if filename_excel == filename and filename_excel not in self.voiceTypes.keys():  #check if mp3 file name file matches target file name in excel // check if file name already existed as key in dict voiceTypes 
                        
                        if utterance in self.matched_utterances.keys(): # check if utterance of the file already existed as key in dict matched_utterances
                            self.matched_utterances[utterance].append(os.path.join(self.audio_folder_path, audiofile)) # if {utterance} key already existed, append file path to list [{utterancePath1},{utterancePath2},<...>]  // in our case: different audio file paths dependent on different speakers of one same utterance 
                        else:
                            self.matched_utterances[utterance]= [os.path.join(self.audio_folder_path, audiofile)] # if no key -> add new utterance key and list

                        self.voiceTypes[filename_excel]=voice_type # add audio file name as key (list name) to dict voiceTypes, append voice_Type as list element
                        total_audio +=1
        
        ###logging
        utterance_found=len(self.matched_utterances.keys()) #length of keys -> number of [{utterance}] list
        logger.info(f"The total number of matched utterances with audio files found are {utterance_found} and total audio files are {total_audio}") 
        logger.info(f"{self.voiceTypes}")
        return 1
    

    def WUWTest_FAR(self):
            
        hitCount = [0]
        logging.info("Gonna start WUW FAR test...")
        audio_files = [f for f in os.listdir(self.audio_folder_path) if f.endswith('.mp3')]


        for value in audio_files:
            stop_event = threading.Event()
            log_thread = threading.Thread(target=self.realtime_far_analyse, args=(hitCount, stop_event))
            log_thread.start()

            file_path = os.path.join(self.audio_folder_path, value)
            audio = AudioSegment.from_mp3(file_path)
            print(f"Now playing the file {value}")
            logging.info(f"Now playing the file {value}")


            if self.seatZone:
                samples = self.adjust_audio_for_SeatZone_test(audio)
            else:
                samples = np.array(audio.get_array_of_samples())
                if audio.channels == 2:
                    samples = np.reshape(samples, (-1, 2))
        
            sd.play(samples, audio.frame_rate)
            sd.wait()
            time.sleep(5) 

            stop_event.set()  
            log_thread.join()  


        print(f"The total number of WUW detection in current audio file is {hitCount[0]}")
        logging.info(f"Test finished, the total number of WUW detection for current audio file is {hitCount[0]}")

        

    def WUWTest_FRR(self):
        if self.seatZone: # 13.11.2024
            if self.tech == "BCA":
                columns = ['WUW','Iteration','Voice','FileName','Language','Shown on HMI', 'Cloud WUW Event Decision','Local WUW Event Decision','WUW Response Time',
                           'Selected MIC', 'Correct MIC?','Highest ranked MIC','Mic_1','Ranking','Confidence','Standard Deviation','Conf.+StdDev','Avg(Conf.+StdDev)','GeoAvg(Conf, StdDev)','Threshold',
                           'Other detected MIC', 'Ranking2', 'Confidence2', 'Standard Deviation2','Conf.+StdDev2','Avg(Conf.+StdDev)2','GeoAvg(Conf, StdDev)2']
            if self.tech == "LBCA":
                columns = ['WUW','Iteration','Voice','FileName','Language','Shown on HMI','Local WUW Event Decision','WUW Response Time',
                           'Selected MIC','Correct MIC?','Highest ranked MIC','Ranking','Confidence','Standard Deviation','Conf.+StdDev','Avg(Conf.+StdDev)','GeoAvg(Conf, StdDev)','WUW Response Time','Threshold',
                           'Other detected MIC', 'Ranking2', 'Confidence2', 'Standard Deviation2','Conf.+StdDev2','Avg(Conf.+StdDev)2','GeoAvg(Conf, StdDev)2']
        else:
            if self.tech == "BCA":
                columns = ['WUW','Iteration','Voice','FileName','Language','Shown on HMI','Cloud WUW Event Decision','Local WUW Event Decision','WUW Response Time'] # 25.07.24 shown on HMI
            elif self.tech == "LBCA":
                columns = ['WUW','Iteration','Voice','FileName','Language','Shown on HMI','Local WUW Event Decision','WUW Response Time'] # 25.07.24 shown on HMI
            else:
                columns = ['WUW','Iteration','Voice','FileName','Language','Local WUW Event Decision','WUW Response Time'] 
 
        # Generate data frame for output excel file
        df = pd.DataFrame(columns=columns)   # with column names = list above

        for key,values in self.matched_utterances.items():  # key indicates a list (here: list of audio file paths of one utterance) 
            logging.info(f"Gonna start WUW Measurement with the utterance {key}")  

            for value in values:  # values are utterance mp3 file paths
                
                print(f"Currently being played utterance is {value}\nRunning...")
                filename=os.path.splitext(os.path.basename(value))[0]  # e.g. <...>/de_de_Intent_Wakeword_1.mp3 -> de_de_Intent_Wakeword_1
                voicetype=self.voiceTypes[filename] # voicetype is a list
              
                for i in range(int(self.Iterationcocunt)):
                    res = {}
                    #wait for n seconds before starting the new test
                    time.sleep(20)
                    self.UpdateSignal(f"Current Iteration:{i}")
                    #Start logcat logs for the entire test duration
                    current_target_time=self.run_adb_command("shell date +'%s.%N'")
                    #overall_log_file=f"{self.rundirectory}/overall_Target_log_KPI_Test.txt"
                    self.start_collecting_logs()  # function see below
                    audio = AudioSegment.from_mp3(value)
                    if key =="BMW":
                        audio_len_diff = audio.duration_seconds - 0.5
                    else:
                        audio_len_diff = audio.duration_seconds - 1
                    #audio_len_diff = extract_remaining_audio_duration(audio)
                    
                    logging.info(f"Now playing the file {value} AND length is {audio_len_diff}")


                    if self.seatZone:
                        samples = self.adjust_audio_for_SeatZone_test(audio)
                    else:
                        samples = np.array(audio.get_array_of_samples())
                        if audio.channels == 2:
                            samples = np.reshape(samples, (-1, 2))
                            
                    sd.play(samples, audio.frame_rate)
                    ###wait till playing finishes
                    sd.wait()
                    #From end of utterrance, measurement starts

                    start_meas_time = self.run_adb_command("shell date +'%s.%N'")
                    start_meas_pc_time = datetime.now()

                    # Parse the current target time into a datetime object
                    current_target_time_seconds, current_target_time_nanoseconds = current_target_time.split('.')
                    current_target_time_dt = datetime.fromtimestamp(int(current_target_time_seconds) + int(current_target_time_nanoseconds) / 1e9)

                    # Format the current target time
                    current_target_time_formatted = current_target_time_dt.strftime('%H:%M:%S.%f')[:-3]
                    ### Waiting for log syncing with the target
                    time.sleep(5)
                    #going to home screen to end the dialog
                    self.run_adb_command("shell input keyevent KEYCODE_HOME")
                   
                    #Stop log collection after test
                    self.stop_collecting_logs() # function see below

                    end_time_target=self.run_adb_command("shell date +'%s.%N'")
                     # Parse the current target time into a datetime object
                    end_target_time_seconds, end_target_time_nanoseconds = end_time_target.split('.')
                    end_target_time_dt = datetime.fromtimestamp(int(end_target_time_seconds) + int(end_target_time_nanoseconds) / 1e9)

                    # Format the current target time
                    end_target_time_formatted = end_target_time_dt.strftime('%H:%M:%S.%f')[:-3]
                    logs = self.get_logcat_logs(current_target_time_formatted, end_target_time_formatted,logging)  # function see below
                    self.save_individual_logs(logs, value)
                    logging.info(f"Now logs are retreived from the device for the played intent")
                    self.append_logs(logs) # function see below

                    if self.tech == "Cerence":
                        res = self.get_wuw_rsp_time_Cerence(start_meas_time,logs,i,key,start_meas_pc_time,audio_len_diff,voicetype,i,filename)
                    else:   
                        if self.seatZone:
                            res = self.get_wuw_rsp_time_ACA_SeatZone(start_meas_time,logs,i,key,start_meas_pc_time,audio_len_diff,voicetype,i,filename)
                        else:
                            res = self.get_wuw_rsp_time_ACA(start_meas_time,logs,i,key,start_meas_pc_time,audio_len_diff,voicetype,i,filename)  # calculate time data etc, #function see below

                    if self.seatZone:
                        if self.tech == "BCA":
                            df.loc[len(df)] = [
                                res.get('WUW', ''),
                                res.get('Iteration',''),
                                res.get('Voice', ''),
                                res.get('FileName', ''),
                                res.get('Language', ''),
                                res.get('Shown on HMI', ''),
                                res.get('Cloud WUW Event Decision', ''),
                                res.get('Local WUW Event Decision', ''),
                                res.get('WUW Response Time', ''),
                                self.mic,
                                #res.get('Detected?', ''),
                                res.get('Correct MIC?', ''),
                                str(res.get('Highest ranked MIC', '')),
                                res.get('Mic_1', ''),
                                res.get('Ranking_1', ''),
                                res.get('Confidence_1', ''),
                                res.get('StandardDeviation_1', ''),
                                res.get('ConfStdDev_1', ''),
                                res.get('AvgConfStdDev_1', ''),
                                res.get('GeoAvg_1', ''),
                                res.get('Threshold', ''),
                                res.get('Mic_2', ''),
                                res.get('Ranking_2', ''),
                                res.get('Confidence_2', ''),
                                res.get('StandardDeviation_2', ''),
                                res.get('ConfStdDev_2', ''),
                                res.get('AvgConfStdDev_2', ''),
                                res.get('GeoAvg_2', '')]
                        elif self.tech == "LBCA":
                            df.loc[len(df)] = [
                                res.get('WUW', ''),
                                res.get('Iteration',''),
                                res.get('Voice', ''),
                                res.get('FileName', ''),
                                res.get('Language', ''),
                                res.get('Shown on HMI', ''),
                                res.get('Local WUW Event Decision', ''),
                                res.get('WUW Response Time', ''),
                                self.mic,
                                #res.get('Detected?', ''),
                                res.get('Correct MIC?', ''),
                                str(res.get('Highest ranked MIC', '')),
                                res.get('Mic_1', ''),
                                res.get('Ranking_1', ''),
                                res.get('Confidence_1', ''),
                                res.get('StandardDeviation_1', ''),
                                res.get('ConfStdDev_1', ''),
                                res.get('AvgConfStdDev_1', ''),
                                res.get('GeoAvg_1', ''),
                                res.get('Threshold', ''),
                                res.get('Mic_2', ''),
                                res.get('Ranking_2', ''),
                                res.get('Confidence_2', ''),
                                res.get('StandardDeviation_2', ''),
                                res.get('ConfStdDev_2', ''),
                                res.get('AvgConfStdDev_2', ''),
                                res.get('GeoAvg_2', '')]
                    else:
                        if self.tech == "BCA":
                            df.loc[len(df)] = [
                                res.get('WUW', ''),
                                res.get('Iteration',''),
                                res.get('Voice', ''),
                                res.get('FileName', ''),
                                res.get('Language', ''),
                                res.get('Shown on HMI', ''),
                                res.get('Cloud WUW Event Decision', ''),
                                res.get('Local WUW Event Decision', ''),
                                res.get('WUW Response Time', '')]
                        if self.tech == "LBCA":
                            df.loc[len(df)] = [
                                res.get('WUW', ''),
                                res.get('Iteration',''),
                                res.get('Voice', ''),
                                res.get('FileName', ''),
                                res.get('Language', ''),
                                res.get('Shown on HMI', ''),
                                res.get('Local WUW Event Decision', ''),
                                res.get('WUW Response Time', '')]
                        if self.tech == "Cerence": 
                            df.loc[len(df)] = [
                                res.get('WUW', ''),
                                res.get('Iteration',''),
                                res.get('Voice', ''),
                                res.get('FileName', ''),
                                res.get('Language', ''),
                                res.get('Local WUW Event Decision', ''),
                                res.get('WUW Response Time', '')]

                    ''
                    '''if key in self.Intent_KPI_Values.keys():
                         if voicetype in self.Intent_KPI_Values[key]:  
                            self.Intent_KPI_Values[key][voicetype].append(speech_response_time)  
                         else:  
                            self.Intent_KPI_Values[key][voicetype] = [speech_response_time]  
                    else:
                            self.Intent_KPI_Values[key] = {voicetype: [speech_response_time]} '''
                
                    print(f"Current uterrance iteration finished.\n")
                    time.sleep(8)

                
            
            print(df.to_string(index=False))

         
        # Specify the Excel file name and path
            
        #report_excel_file = r'D:\00_Haonan_KE\04_KPITest\New run\KPI_Report_IPA_APP_VERSION_5_11_0.xlsx'

        # Write the DataFrame to an Excel file
        df.to_excel(self.report_excel_file, index=False)
        
        print("WUW recognition test DONE.")
        self.test_finished = True


        '''for key,values in self.Intent_KPI_Values.items():   
            try:
                average = sum(values) / len(values)
                print(f"For Intent:{key} :The average speech response time is {average}")
                logging.info(f"For Intent:{key} ;The average speech response time is {average}")
            except (Exception)as msg:
                logging.error(f"the intent {key} has no response time saved")
            logging.info(self.Intent_KPI_Values)'''

    
    

    def get_wuw_rsp_time_ACA(self,start_measurement,logs,iteration,WUW,pc_time,audio_len_diff,voicetype,i,filename):
        res = {}
        #speech_response_time=0
        #total_response_time=0
        
        # Define a regular expression pattern for log timestamps
        pattern =   r'^\d{2}-\d{2} (\d{2}:\d{2}:\d{2}\.\d{3})' # r for raw string -> all symbols seen as single element without specific meanings
        json_pattern = r'{.*}'
        
        wakeUpWord = WUW.split(',')[0]  # get WuW -> if just wuw as utterance in excel still ok (no operations will be executed without ",")

        time_dt = datetime.fromtimestamp(float(start_measurement)) # target time from abd command, see above
        target_time_formatted = time_dt.strftime('%H:%M:%S.%f')  
        target_time_formatted= datetime.strptime(target_time_formatted, '%H:%M:%S.%f')
        #FInd difference between target and system time
        time_difference=(pc_time-time_dt).total_seconds()
        logging.info(f"The WUW time extraction function is started for iteration: {iteration}")  # iteration = i in KPI Test, see above
    
        logging.info(f"The time difference between System time and target time for : {iteration} in utterance {WUW} is {time_difference} seconds")


        isWakeupdetected = False
        isTrueWakeUp = False
        localWUWdecision = False
        logline=None
        wuw_response_time = 0
 
        for line in logs:  # logs = return from get logcat logs, func see below
            if "SpeechRecognizerEngineImpl" in line and "newState=LISTENING" in line:
                isWakeupdetected = True
                WUW_Detection_time=(re.match(pattern,line)).group(1) # get time data from log flie line
                WUW_Detection_time = datetime.strptime(WUW_Detection_time, '%H:%M:%S.%f')
                wuw_response_time=(WUW_Detection_time-target_time_formatted).total_seconds()
                wuw_response_time = wuw_response_time + audio_len_diff
                print(f"For Intent:{WUW} ; Iteration: {iteration}:The total WUW response time is {wuw_response_time}")
                #logline=line
            if "AHE-LRG-SluFinalProcessor" in line and "IsFalseWakewordSession=false" in line:
                localWUWdecision= True
                #logline=line
            if "directive=namespace" in line and "RequestProcessingStarted" in line:   # its the cloud decision
                isTrueWakeUp = True
                #logline=line
        if wakeUpWord.strip().lower() =="alexa" and isWakeupdetected:
                #speech_response_time=self.cal_WUW_respTime(logline,start_measurement,time_difference)
                self.UpdateSignal(f"Wakeword Detected: {isWakeupdetected}")
        elif isTrueWakeUp:
                #speech_response_time=self.cal_WUW_respTime(logline,start_measurement,time_difference)
                self.UpdateSignal(f"Wakeword Detected: {isTrueWakeUp}")
        logging.info(f"the status for wakeword detected:{isWakeupdetected} and if truewakeup seen : {isTrueWakeUp}")
        
        res["WUW"] = wakeUpWord
        res["Shown on HMI"] = isWakeupdetected
        res["Cloud WUW Event Decision"] = isTrueWakeUp
        res["Local WUW Event Decision"] = localWUWdecision
        res["WUW Response Time"] = wuw_response_time
        res["Voice"] = voicetype
        res["FileName"] = filename
        res["Language"] = self.language
        res["Iteration"] = i+1
                
        #print(f"For utterance:{WUW} ; Iteration: {iteration}:The total speech response time is {speech_response_time}")
        #logging.info(f"For utterance:{WUW} ; Iteration: {iteration}:The total speech response time is {speech_response_time}")
       
            
        #logging.info(f"the different WUW meansrurements for utterance :{WUW} in iteration {iteration} are {speech_response_time} seconds with start time :{start_measurement} and {total_response_time}")       
        
        return res
    

    def get_wuw_rsp_time_ACA_SeatZone(self,start_measurement,logs,iteration,WUW,pc_time,audio_overhead,voicetype,i,filename):
        res = {}
        logrankings:list = []
        Mic = ""
        threshold = ""
        Detected = False
        CorrectMIC = False
        HighestRankedMIC: list = []
        Ranking = ""
        Confidence = ""
        StandardDeviation = ""
        ConfStdDev = ""
        AvgConfStdDev = ""
        GeoAvg = ""
        wuw_response_time = 0
         # Define a regular expression pattern for log timestamps
        pattern =   r'^\d{2}-\d{2} (\d{2}:\d{2}:\d{2}\.\d{3})' # r for raw string -> all symbols seen as single element without specific meanings


        
        wakeUpWord = WUW.split(',')[0]  # get WuW -> if just wuw as utterance in excel still ok (no operations will be executed without ",")

        time_dt = datetime.fromtimestamp(float(start_measurement)) # target time from abd command, see above
        target_time_formatted = time_dt.strftime('%H:%M:%S.%f')  
        target_time_formatted= datetime.strptime(target_time_formatted, '%H:%M:%S.%f')
        #FInd difference between target and system time
        time_difference=(pc_time-time_dt).total_seconds()
        logging.info(f"The WUW time extraction function is started for iteration: {iteration}")  # iteration = i in KPI Test, see above
    
        logging.info(f"The time difference between System time and target time for : {iteration} in utterance {WUW} is {time_difference} seconds")


        isWakeupdetected = False
        isTrueWakeUp = False
        localWUWdecision = False
       
 
        for line in logs:  # logs = return from get logcat logs, func see below
            if "SpeechRecognizerEngineImpl" in line and "newState=LISTENING" in line:
                WUW_Detection_time=(re.match(pattern,line)).group(1) # get time data from log flie line
                WUW_Detection_time = datetime.strptime(WUW_Detection_time, '%H:%M:%S.%f')
                wuw_response_time=(WUW_Detection_time-target_time_formatted).total_seconds()
                wuw_response_time = wuw_response_time + audio_overhead
                logging.info(f"the start time is --> {target_time_formatted}, and wuw response is at --> {wuw_response_time}")
                print(f"For Intent:{WUW} ; Iteration: {iteration}:The total WUW response time is {wuw_response_time}")
                isWakeupdetected = True
            if "AHE-LRG-SluFinalProcessor" in line and "IsFalseWakewordSession=false" in line:
                localWUWdecision= True
            if "directive=namespace" in line and "RequestProcessingStarted" in line:   # its the cloud decision
                isTrueWakeUp = True

            if "getHighestRankedResult() Highest" in line:
                Mic = re.search("Highest: <Mic: (.*?),",line).group(1)
                Ranking = re.search("ranking: (.*?)>",line).group(1)
                Detected = True
                if Mic == self.mic:
                    CorrectMIC = True
                HighestRankedMIC.append(Mic)
            if "logRankings()" in line and ": <Mic" in line:
                logging.info(f"The log ranking  is found for wuw {WUW} and the line is {line}")
                match = re.search("Mic: (.*?), ranking: \{ Total: (.*?), Conf: (.*?), StdDev: (.*?), Conf \+ StdDev: (.*?), Avg \(conf \+ stdDev\): (.*?), Geo avg \(conf, stdDev\): (.*?) \}",line)
                Mic = match.group(1)
                Ranking = match.group(2)
                Confidence = match.group(3)
                StandardDeviation = match.group(4)
                ConfStdDev = match.group(5)
                AvgConfStdDev = match.group(6)
                GeoAvg = match.group(7)
                
                rank_1 = {}
                rank_1['Mic'] = Mic
                rank_1['Ranking'] = Ranking
                rank_1['Confidence'] = Confidence
                rank_1['StandardDeviation'] = StandardDeviation
                rank_1['ConfStdDev'] = ConfStdDev
                rank_1['AvgConfStdDev'] = AvgConfStdDev
                rank_1['GeoAvg'] = GeoAvg
                logrankings.append(rank_1)
                
            if "onWuWEvent()" in line and self.mic in line:
                strp_text = line.split("Thr:")[-1]
                threshold = strp_text.split(',')[0]

        if wakeUpWord.strip().lower() =="alexa" and isWakeupdetected:
                self.UpdateSignal(f"Wakeword Detected: {isWakeupdetected}")
        elif isTrueWakeUp:
                self.UpdateSignal(f"Wakeword Detected: {isTrueWakeUp}")
        logging.info(f"the status for wakeword detected:{isWakeupdetected} and if truewakeup seen : {isTrueWakeUp}")

        res["WUW"] = wakeUpWord
        res["Shown on HMI"] = isWakeupdetected
        res["Cloud WUW Event Decision"] = isTrueWakeUp
        res["Local WUW Event Decision"] = localWUWdecision
        for idx,logrank in enumerate(logrankings,start=1):
            for key,value in logrank.items():
                res[key+'_'+str(idx)] = value
            logging.info(f"the detected rankings are ...{logrank}")

    
        res["Detected?"] = Detected
        res["Correct MIC?"] = CorrectMIC
        res["Highest ranked MIC"] = HighestRankedMIC
        res["Ranking"] = Ranking
        res["WUW Response Time"] = wuw_response_time
        res["Threshold"] = threshold
        res["Voice"] = voicetype
        res["FileName"] = filename
        res["Language"] = self.language
        res["Iteration"] = i+1

        return res
    
    def get_wuw_rsp_time_Cerence(self,start_measurement,logs,iteration,WUW,pc_time,audio_overhead,voicetype,i,filename):
        res = {}
        #speech_response_time=0
        #total_response_time=0
        pattern =   r'^\d{2}-\d{2} (\d{2}:\d{2}:\d{2}\.\d{3})'
        wakeUpWord = WUW.split(',')[0]  # get WuW

        logging.info(f"The WUW time extraction function is started for iteration: {iteration}")  # iteration = i in KPI Test, see above
        # Convert time string to datetime object  
        time_dt = datetime.fromtimestamp(float(start_measurement)) # target time from abd command, see above
        target_time_formatted = time_dt.strftime('%H:%M:%S.%f')  
        target_time_formatted= datetime.strptime(target_time_formatted, '%H:%M:%S.%f')
        #FInd difference between target and system time
        time_difference=(pc_time-time_dt).total_seconds()
        logging.info(f"The time difference between System time and target time for : {iteration} in utterance {WUW} is {time_difference} seconds")

        isWakeupdetected = False
        logline=None
       
 
        for line in logs:  # logs = return from get logcat logs, func see below
            if "CSS_RecognizerListener_onResult result=" and "wuw_customized" in line:
                isWakeupdetected = True
                WUW_Detection_time=(re.match(pattern,line)).group(1) # get time data from log flie line
                WUW_Detection_time = datetime.strptime(WUW_Detection_time, '%H:%M:%S.%f')
                wuw_response_time=(WUW_Detection_time-target_time_formatted).total_seconds()
                wuw_response_time = wuw_response_time + audio_overhead
                logline=line
        if isWakeupdetected:
            #speech_response_time=self.cal_WUW_respTime(logline,start_measurement,time_difference)
            self.UpdateSignal(f"Wakeword Detected: {isWakeupdetected}")
        logging.info(f"the status for wakeword detected:{isWakeupdetected}")

        res["WUW"] = wakeUpWord
        res["Local WUW Event Decision"] = isWakeupdetected
        res["WUW Response Time"] = wuw_response_time
        res["Voice"] = voicetype
        res["FileName"] = filename
        res["Language"] = self.language
        res["Iteration"] = i+1
                
        #print(f"For utterance:{WUW} ; Iteration: {iteration}:The total speech response time is {speech_response_time}")
        #logging.info(f"For utterance:{WUW} ; Iteration: {iteration}:The total speech response time is {speech_response_time}")
       
            
        #logging.info(f"the different WUW meansrurements for utterance :{WUW} in iteration {iteration} are {speech_response_time} seconds with start time :{start_measurement} and {total_response_time}")       
        
        return res
    
    def save_individual_logs(self, logs, utterance):
        utterance = utterance.split('\\')[-1]  
        utterance=utterance.split('.')[0] 
        log_directory = f"{self.rundirectory}/Individual_Logs"
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        log_file = f"{log_directory}/{utterance}.txt"
        with open(log_file, "a", encoding='ISO-8859-1') as file:
            for line in logs:
                file.writelines(f"{line}\n")


    def get_logcat_logs(self,start_time, end_time,logger):
            with open(f'{self.rundirectory}/Target_log_WUW_Test.txt', 'r', encoding='ISO-8859-1') as f:  
                data = f.read()  

            
            logs = data
            
            # Define a regular expression pattern for log timestamps
            pattern = r'^\d{2}-\d{2} (\d{2}:\d{2}:\d{2}\.\d{3})'
            
            # Filter logs for entries within the desired time range
            filtered_logs = []
            for line in logs.split('\n'):
                match = re.match(pattern, line)
                if match:
                    time = match.group(1)
                    if start_time <= time <= end_time:
                        filtered_logs.append(line)
            
            return filtered_logs
    
    def cal_WUW_respTime(self,logline,start_measurement,time_difference):
           # Define a regular expression pattern for log timestamps
        pattern =   r'^\d{2}-\d{2} (\d{2}:\d{2}:\d{2}\.\d{3})' # r for raw string -> all symbols seen as single element without specific meanings
        total_response_time=(re.match(pattern,logline)).group(1) # get time data from log flie line
        total_response_time = datetime.strptime(total_response_time, '%H:%M:%S.%f')
        speech_response_time=(total_response_time-start_measurement).total_seconds() - time_difference
        return speech_response_time
        
    
    
    def collect_logs(self):
        log_file=f"{self.rundirectory}/Target_log_WUW_Test.txt"
        with open(log_file, "w") as file:
            self.logcat_process = subprocess.Popen([f"adb", "-s", self.ip, "logcat"], stdout=file)

    def start_collecting_logs(self):
        self.logcat_thread = threading.Thread(target=self.collect_logs)
        self.logcat_thread.start()

    def stop_collecting_logs(self):
        if self.logcat_process is not None:
            self.logcat_process.terminate()
        if self.logcat_thread is not None:
            self.logcat_thread.join()
            self.logcat_thread = None

    def append_logs(self,logs):
        log_file=f"{self.rundirectory}/overall_Target_log_WUW_Test.txt"
        with open(log_file, "a", encoding='ISO-8859-1') as file:
            for line in logs:
                file.writelines(f"{line}\n")

    def realtime_far_analyse(self,hitCount,stop_event):
        log_file=f"{self.rundirectory}/Target_log_WUW_FAR_Test.txt"
        columns = ['WUW','Shown on HMI','Selected MIC','Correct MIC?','Highest ranked MIC',  
                    'Ranking','Confidence','Standard Deviation','Conf.+StdDev','Avg(Conf.+StdDev)','GeoAvg(Conf, StdDev)',
                    'Other detected MIC', 'Ranking2', 'Confidence2', 'Standard Deviation2','Conf.+StdDev2','Avg(Conf.+StdDev)2','GeoAvg(Conf, StdDev)2']
        df = pd.DataFrame(columns=columns)
        with open(log_file, "w", encoding='ISO-8859-1') as file:
          process = subprocess.Popen(["adb", "-s", self.ip, "logcat"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1, encoding='ISO-8859-1')
          temp_data = {}
          while not stop_event.is_set():
            line = process.stdout.readline()
            file.writelines(f"{line}\n")
            file.flush()
            if self.seatZone:
                if "SpeechRecognizerEngineImpl" in line and "newState=LISTENING" in line:
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
        if self.seatZone:
            df.to_excel(self.report_excel_file, index=False)

    def adjust_audio_for_SeatZone_test(self, audio):
        #max_volume = audio.max_dBFS
        mean_volume = audio.dBFS
            # Check if it's stereo
            
        if  audio.channels != 2:
            stereo_audio = AudioSegment.from_mono_audiosegments(audio, audio)
        else:
            stereo_audio = audio

        # Split the stereo audio into left and right channels
        left_channel = stereo_audio.split_to_mono()[0]
        right_channel = stereo_audio.split_to_mono()[1]
        # Ensure both channels have the same frame rate
        target_frame_rate = max(left_channel.frame_rate, right_channel.frame_rate)
        target_sample_width = max(left_channel.sample_width, right_channel.sample_width)
        left_channel = left_channel.set_frame_rate(target_frame_rate).set_sample_width(target_sample_width)
        right_channel = right_channel.set_frame_rate(target_frame_rate).set_sample_width(target_sample_width)

        slice_num = len(left_channel)
        smooth_reduction_db = 16
        slice_length = 1

        left_channel_modified = AudioSegment.empty()
        right_channel_modified = AudioSegment.empty()
        left_channel_padded = AudioSegment.empty()
        right_channel_padded = AudioSegment.empty()
        min_low = min(audio.get_array_of_samples())
        lowest_dbfs = 20 * np.log10(abs(min_low) / right_channel.max_possible_amplitude) if min_low != 0 else -float('inf')

        logging.info(f"Lowest dBFS: {lowest_dbfs}")

        # Relative reduction: 20% reduction to the range starting from the lowest dB
        gain_reduction_db = abs(lowest_dbfs) * 0.2
        logging.info(f"Gain Reduction (dB): {gain_reduction_db}")
                

        reduction_db = 0.4 * mean_volume  # mean

        if self.mic == "FRONT_LEFT":
            # Merge the channels back into a stereo track, if driver keep audio for passengen unmodified
            left_channel_modified = left_channel + AudioSegment.silent(duration=float(self.delay))
            right_channel_padded = AudioSegment.silent(duration=float(self.delay)) + right_channel
            adjusted_stereo = AudioSegment.from_mono_audiosegments( left_channel_modified,right_channel_padded-gain_reduction_db)
            adjusted_stereo.export("output_stereo.wav", format="wav")  
        else:
            # Merge the channels back into a stereo track
            left_channel_padded = AudioSegment.silent(duration=float(self.delay)) + left_channel
            right_channel_modified = right_channel +  AudioSegment.silent(duration=float(self.delay))
            adjusted_stereo = AudioSegment.from_mono_audiosegments( left_channel_padded-gain_reduction_db,right_channel_modified)

            
        # Convert to numpy array
        samples = np.array(adjusted_stereo.get_array_of_samples())
        samples = np.reshape(samples, (-1, 2))

        return samples

if __name__ == '__main__':
    kpitest_obj=WUWTest(tech='BCA',directory='/home/adin.n@acsiatech.com/Desktop/c_programs/PyPros/WuW/WUW_Recognition_Testrun_07_07_12_39',
                        mcuip='161.93.123.23',
                        iexcelpath='/home/adin.n@acsiatech.com/Downloads/4000-most-common-english-words-xlsx.xlsx',
                        oexcelname='output.xlsx',
                        audiopath='/home/adin.n@acsiatech.com/Music/Music',
                        lang='en_us',
                        iterations=10,
                        updatesignal=" ",
                        seatZone='',
                        mic= '',
                        delay=200
                        )

