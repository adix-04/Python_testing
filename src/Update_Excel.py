# import os
# from openpyxl import Workbook, load_workbook

# def append_data_to_excel(file_name, row_data):
#     """
#     Appends a row of data to the specified Excel file.

#     Parameters:
#     - file_name (str): Name of the Excel file (e.g., 'data.xlsx').
#     - row_data (list): A list of values representing a single row to append.
#     """
#     # Check if the file exists
#     if os.path.exists(file_name):
#         workbook = load_workbook(file_name)
#         sheet = workbook.active
#     else:
#         workbook = Workbook()
#         sheet = workbook.active
    

#     # Append the row
#     sheet.append(row_data)

#     # Save the workbook
#     workbook.save(file_name)
#     print(f"Row appended to '{file_name}' successfully.")


from openpyxl import Workbook, load_workbook
import os
from datetime import datetime

FIELDS = [
    "timestamp", "wake_word", "utterance", "translated_text", "intent",
    "is_final_asr","cpu_usage" ,"seat_position",
    "asr_text", "response_text", "confidence", "language",
    "audio_path", "retry_count", "error_code"
]

EXCEL_FILE = "session_log.xlsx"

class Update_Excel():
    def __init__(self):
        self.data = {key: "" for key in FIELDS}
        self.data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#**kwargs = "Keyword Arguments" It allows the function to accept any number of named arguments, even ones that aren’t pre-defined.
    def update(self, **kwargs): 
        for key, value in kwargs.items():
            if key in self.data:
                self.data[key] = value

    def write(self, file_name=EXCEL_FILE):
        if not os.path.exists(file_name):
            wb = Workbook()
            ws = wb.active
            ws.title = "Log"
            ws.append(FIELDS)
        else:
            wb = load_workbook(file_name)
            ws = wb["Log"]

        row = [self.data.get(field, "") for field in FIELDS]
        ws.append(row)
        wb.save(file_name)
        print(f"✔ Session written to {file_name}")

    def reset(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data = {key: "" for key in FIELDS}
        self.data["timestamp"] = timestamp
if __name__ == "__main__":
    session = Update_Excel()
    #  Wake word detected
    session.update(wake_word="Hey Reva")
    #  ASR result comes in later
    session.update(asr_text="Turn on lights", intent="Control_Lights", confidence="0.91")
    # System info received
    session.update(cpu_usage="12%", mem_usage="155MB")
    # Response generated
    session.update(response_text="Turning on the lights", retry_count="0")
    # Finally write once everything is ready
    session.write()
    #  Start next session
    session.reset()
