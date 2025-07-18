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
        check_cpu = False
        with open (file_name,"r") as file:
            read_line=file.readlines()
            for line in read_line:
                if 'is_final_asr":true' in line:
                    check_cpu = True
                    self.Log_analyzer(line)
                    # break
                if 'INTENT=' in line and 'CONFIDENCE=' and 'CONFIDENCE=' in line:
                    print(line)
                    self.Intent_analyzer(line)
                if 'PROMPT_TEXT=' in line:
                    self.prompt_text(line)
                if 'avgcpu:' in line and check_cpu:
                    self.get_cpu(line)
                    check_cpu = False
            
            self.excel.write()
            self.excel.reset()

    def prompt_text(self,log_line):
        promp_text = re.search(r'PROMPT_TEXT=([^\n]+)', log_line)
        promp_text = promp_text.group(1).strip() if promp_text else None
        # print(promp_text)
        self.excel.update(prompt_text=promp_text)
    def get_cpu(self,log_line):
        cpu = re.search(r'cpu:(\d+(\.\d+)?)%', log_line)
        cpu_usage = cpu.group(1) if cpu else None
        # print(cpu_usage)
        self.excel.update(cpu_usage=cpu_usage)
    def Log_analyzer(self,logline):
        match = re.search(r'"orthography":"(.*?)"', logline)
        if match:
            extracted_text = match.group(1)
            if extracted_text.lower()==str(self.utterance).lower():
                bool_asr=True
            else:
                bool_asr=False
            print(extracted_text)
            self.excel.update(is_final_asr=bool_asr)
        else:
            print("No orthography field found.")
    def Intent_analyzer(self,log_line):
        intent_match = re.search(r'INTENT=([^,]+)', log_line)
        intent = intent_match.group(1).strip() if intent_match else None
        # INTENT_DOMAIN
        domain_match = re.search(r'INTENT_DOMAIN=([^,]+)', log_line)
        intent_domain = domain_match.group(1).strip() if domain_match else None
        # CONFIDENCE
        confidence_match = re.search(r'CONFIDENCE=([^,]+)', log_line)
        confidence = confidence_match.group(1).strip() if confidence_match else None
        # SYSTEM_LANGUAGE
        lang_match = re.search(r'SYSTEM_LANGUAGE=([^,]+)', log_line)
        language = lang_match.group(1).strip() if lang_match else None
        # UTTERANCE
        utt_match = re.search(r'UTTERANCE=([^,]+)', log_line)
        utterance = utt_match.group(1).strip() if utt_match else None
        # Print the values
        # print("Intent:", intent)
        # print("Domain:", intent_domain)
        # print("Confidence:", confidence)
        # print("Language:", language)
        # print("Utterance:", utterance)
        # print("Weather Status:", weather_status)
        # print("City:", city_name)
        self.excel.update(wake_word='Hey Mini', utterance=self.utterance,recognized_text=utterance,intent=intent,confidence=confidence)

        

if __name__ == "__main__":
   obj = Get_data(r'c:\Users\Adin N S\Downloads\Logs_trace\Logs_trace\traceLog.txt2025-07-15_18-13-04',"Will it rain in Hamburg")