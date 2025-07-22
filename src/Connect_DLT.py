import os
import glob
import subprocess
import time as t
import getpass
from datetime import datetime
import Get_data_from_DLT

class Connet_DLT_class():
    def __init__(self,file_path,project_file,output_dir):
        self.outDIR = output_dir
        self.dlp = project_file
        self.file_path = file_path
        self.file_name =''
        print(self.file_path)
        print("out put dire is==" +self.outDIR)
        self.cleaner()
    def cleaner(self):
        try:
            if os.listdir(self.file_path):
                self.remove_cache_files(self.file_path)
            else:
                print(self.project_file)
                # print("no files in cahce")
                pass 
        except Exception as e:
            print(e)
    
    
    def start_dlt(self):
        # print("called")
        #This will be called from TTS main
        try:
            process = subprocess.Popen(["dlt_viewer","-s","-p",str(self.dlp)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        except Exception as e:
            print(e)
        # print("DLT is opened")

    def remove_cache_files(self,file_path):
        try:
            files=glob.glob(os.path.join(file_path,"*"))
            for f in files:
                os.remove(f)
                 
        except Exception as e:
            print(e)
            print("error in clear DLT from cache")

    def convert_dlt_log_text(self):
        temp_file = os.listdir(self.file_path)
        print(temp_file[0])
        try:
# {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}
         self.file_name=f'{self.outDIR}/traceLog.txt'
         process = subprocess.run(["dlt_viewer","-c",f'C:/Users/{getpass.getuser()}/AppData/Local/dlt_viewer/cache/{temp_file[0]}',self.file_name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        
         
        except Exception as e:
             print(e)
       
    def get_cpu(self):
         Get_data_from_DLT.Get_data.monitor_cpu_mem()
    def check(self,uttearnce):
         Get_data_from_DLT.Get_data(self.file_name,utterance=uttearnce)

    def stop_dlt(self):

        subprocess.call(["taskkill", "/F", "/IM", "dlt_viewer.exe"])
        pass

            
        
if __name__ == "__main__":
    test="val"
    connect_dlt_test=Connet_DLT_class("C:/Users/jithin.sreekala/AppData/Local/dlt_viewer/cache","C:/Users/jithin.sreekala/Downloads/release/release/file_DLT.dlp")
    connect_dlt_test.start_dlt()
    t.sleep(10)
    connect_dlt_test.stop_dlt()
    connect_dlt_test.convert_dlt_log_text("C:/Users/jithin.sreekala/AppData/Local/dlt_viewer/cache")





