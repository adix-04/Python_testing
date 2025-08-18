import subprocess
def stop_dlt():
    subprocess.call(["taskkill", "/F", "/IM", "dlt_viewer.exe"])
    pass


if __name__ == "__main__":
    stop_dlt()