import os
import glob
import subprocess
import time as t

class Connet_DLT_class():

    project_file_in_class=""
    val_path=""
    bool_dlt_status=True

    def __init__(self,file_path,val,project_file):
        try:
            if  os.listdir(file_path):
                self.project_file_in_class=project_file
                self.val_path=val
                self.remove_cache_files(file_path)
                # empty the local dir of DLT
            else:
                print(val)
                print(project_file)
                print("no files in cahce")
                self.start_dlt(project_file,val)
                #no files in DLT cache 
                pass
            
        except:
            print("error to del file")
    
    
    def start_dlt(self,project_file,val):
        print("called")
        # start_dlt_theard.start_DLT_with_prg()
        process = subprocess.Popen([str(val),"-s","-p",str(project_file)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        print("DLT is opened")
        t.sleep(2)
        subprocess.call(["taskkill", "/F", "/IM", "dlt_viewer.exe"])
        pass

    def remove_cache_files(self,file_path):
        print("remover")
        try:
            files=glob.glob(os.path.join(file_path,"*"))
            for f in files:
                os.remove(f)
            self.start_dlt(self.project_file_in_class,self.val_path)
                 
        except Exception as e:
            print(e)
            print("error in clear DLT from cache")

            
        

# test="val"
# connect_dlt_test=Connet_DLT("C:/Users/jithin.sreekala/AppData/Local/dlt_viewer/cache","C:/Users/jithin.sreekala/Downloads/release/release/dlt_viewer","C:/Users/jithin.sreekala/Downloads/release/release/file_DLT.dlp")





