import os
from openpyxl import Workbook, load_workbook

def append_data_to_excel(file_name, row_data):
    """
    Appends a row of data to the specified Excel file.

    Parameters:
    - file_name (str): Name of the Excel file (e.g., 'data.xlsx').
    - row_data (list): A list of values representing a single row to append.
    """
    # Check if the file exists
    if os.path.exists(file_name):
        workbook = load_workbook(file_name)
        sheet = workbook.active
    else:
        workbook = Workbook()
        sheet = workbook.active
    

    # Append the row
    sheet.append(row_data)

    # Save the workbook
    workbook.save(file_name)
    print(f"Row appended to '{file_name}' successfully.")

