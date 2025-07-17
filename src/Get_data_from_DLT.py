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
                if 'avgcpu:' in line:
                    self.get_cpu(line)
                    break
                if 'INTENT=' in line and 'CONFIDENCE=' and 'CONFIDENCE=' in line:
                    print(line)
                    self.Intent_analyzer(line)
                if 'PROMPT_TEXT=' in line:
                    self.prompt_text(line)
            
            self.excel.write()
            self.excel.reset()
    def prompt_text(self,log_line):
        promp_text = re.search(r'PROMPT_TEXT=([^,]+)', log_line)
        promp_text = promp_text.group(1).strip() if promp_text else None
        # print(promp_text)
        self.excel.update(prompt_text=promp_text)
    def get_cpu(self,log_line):
        print(log_line)
    def Log_analyzer(self,logline):
        # Extract the value of the "orthography" field
        match = re.search(r'"orthography":"(.*?)"', logline)
        if match:
            extracted_text = match.group(1)
            if extracted_text.lower()==str(self.utterance).lower():
                bool_asr=True
            else:
                bool_asr=False
            print(extracted_text)
        
            self.excel.update(is_final_asr=bool_asr)
            # self.excel.write()
            # self.excel.reset()
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
        # WEATHER STATUS SLOT
        weather_status_match = re.search(r'RECOG_SLOT_Apps_WeatherStatus\s*=\s*([^,]+)', log_line)
        weather_status = weather_status_match.group(1).strip() if weather_status_match else None
        # CITY NAME SLOT
        city_name_match = re.search(r'RECOG_SLOT_Nav_CityName\s*=\s*([^\s,]+)', log_line)
        city_name = city_name_match.group(1).strip() if city_name_match else None
        # 🔍 Print the values
        # print("Intent:", intent)
        # print("Domain:", intent_domain)
        # print("Confidence:", confidence)
        # print("Language:", language)
        # print("Utterance:", utterance)
        # print("Weather Status:", weather_status)
        # print("City:", city_name)
        self.excel.update(wake_word='Hey Mini', utterance=self.utterance,recognized_text=utterance,intent=intent,confidence=confidence)

        

if __name__ == "__main__":
   obj = Get_data(r'C:\Users\Adin N S\Downloads\Logs_trace\Logs_trace\traceLog.txt2025-07-15_18-13-04',"Will it rain in Hamburg")