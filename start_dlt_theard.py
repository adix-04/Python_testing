import subprocess
import time as t

def start_DLT_with_prg():
    process = subprocess.Popen(["C:/Users/jithin.sreekala/Downloads/release/release/dlt_viewer","-s","-p","C:/Users/jithin.sreekala/Downloads/release/release/file_DLT.dlp" ],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    start_DLT_with_prg()