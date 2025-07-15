from Update_Excel import Update_Excel
import re

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

        

        



if __name__ == "__main__":
   obj = Get_data(r'c:\Users\Adin N S\Downloads\Logs_trace\Logs_trace\traceLog.txt2025-07-15_18-01-04',"Will it rain in Hamburg")