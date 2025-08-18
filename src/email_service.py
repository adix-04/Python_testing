import win32com.client as win32com
import os
import psutil

def send_with_outlook(file_path):
    # Open Outlook
    os.startfile('outlook')
    outlook = win32com.Dispatch('outlook.application')    
    # Create a new mail item
    accounts = win32com.Dispatch("outlook.application").Session.Accounts
    print(accounts[0])
    mail = outlook.CreateItem(0)  # 0 = Mail item
    mail.SendUsingAccount  =  accounts[0]
    mail.To = "jithin.sreekala@acsiatech.com;adinnavakumar22@gmail.com;anurage.ss@acsiatech.com;adinkumar45@gmail.com"   
    mail.Subject = "Test Report"
    mail.Body = "Hi,\n\nPlease find the attached test report.\n\nRegards"
    # Attach the file
    if os.path.exists(file_path):
        mail.Attachments.Add(file_path)
    else:  
        print("File not found:", file_path)
    mail.display()   # opens Outlook draft window
    mail.Send()
    os.startfile('outlook')
    for P in psutil.process_iter():
        if "OUTLOOK.EXE" in P.name().upper():
            P.kill()
 
# Test run
if __name__ == "__main__":
    test_file = r"C:\Users\Adin N S\Documents\Python_testing\Night_run_15_07_25.xlsx"  #for testing
    send_with_outlook(test_file)

