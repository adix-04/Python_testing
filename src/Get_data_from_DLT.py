from Update_Excel import Update_Excel
import re
import subprocess
class Get_data():
    def __init__(self,txt_file,utterance):
        self.txt_file=txt_file
        self.utterance=utterance
        print(self.txt_file)
        self.check_line(self.txt_file)
        
    def check_line(self,file_name):
        self.excel = Update_Excel()
        print("in checker inside get data")
        with open (file_name,"r") as file:
            read_line=file.readlines()
            for line in read_line:
                if 'is_final_asr":true' in line:
                    self.Log_analyzer(line)
    
    def Log_analyzer(self,logline):
        # Extract the value of the "orthography" field
        match = re.search(r'"orthography":"(.*?)"', logline)
        if match:
            data=[]
            extracted_text = match.group(1)
            print(extracted_text)
            self.excel.update(wake_word='Hey Mini', utterance=self.utterance,translated_text=extracted_text,is_final_asr=True)
            self.excel.write()
            
        else:
            print("No orthography field found.")


# def calculate_cpu_usage(log_line):
#      # Extract the total CPU and idle values
#       total_cpu_match = re.search(r'(\d+)%cpu', log_line) 
#       idle_match = re.search(r'(\d+)%idle', log_line) 
#       if not total_cpu_match or not idle_match:
#          raise ValueError("Log line does not contain expected CPU or idle values.") 
#       total_cpu = int(total_cpu_match.group(1))
#       idle = int(idle_match.group(1)) 
#       usage = total_cpu - idle 
#       usage=float(usage//8)
#        # This sysytem have 8 core return usage
      
# def monitor_cpu_menu():
#     process = subprocess.Popen( ["adb", "shell", "top", "-d", "1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#     for line in process.stdout()

# def monitor_cpu_mem(): 
#     process = subprocess.Popen( ["adb", "shell", "top", "-d", "1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True )
#     for line in process.stdout: 
#     ````if re.search(r'\d+%cpu', line): 
#       ``    print("CPU:", line.strip())
#             calculate_cpu_usage(line.strip()) 
#         elif re.search(r'Mem:', line) or re.search(r'Swap:', line):
#             print("Memory:", line.strip()) 
#             process.terminate()        

#     try:
#       for line in process.stdout: 
#     ````    if re.search(r'\d+%cpu', line): 
#       ``     print("CPU:", line.strip())
#               calculate_cpu_usage(line.strip()) 
#             elif re.search(r'Mem:', line) or re.search(r'Swap:', line):
#             print("Memory:", line.strip()) 
#             process.terminate() 
#     except KeyboardInterrupt:
#         process.terminate()
#     finally:
#         process.terminate()

#     try:
#         for line in process.stdout: # Match CPU usage line
#     ````    if re.search(r'\d+%cpu', line): # 
#       ``     print("CPU:", line.strip())
#               calculate_cpu_usage(line.strip()) # Match Memory usage line 
#             elif re.search(r'Mem:', line) or re.search(r'Swap:', line): # 
#               print("Memory:", line.strip()) 
#             process.terminate() 
#     except KeyboardInterrupt: 
#         process.terminate() 
#     print("Stopped monitoring.") 
#     finally: 
#         process.stdout.close()
# if __name__ == "__main__": monitor_cpu_mem()
        

        



if __name__ == "__main__":
   obj = Get_data(r'c:\Users\Adin N S\Downloads\Logs_trace\Logs_trace\traceLog.txt2025-07-15_18-01-04',"Will it rain in Hamburg")