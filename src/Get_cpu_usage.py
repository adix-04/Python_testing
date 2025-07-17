

import subprocess
import re
import time as t

def calculate_cpu_usage(log_line):
    # Extract the total CPU and idle values
    total_cpu_match = re.search(r'(\d+)%cpu', log_line)
    idle_match = re.search(r'(\d+)%idle', log_line)

    if not total_cpu_match or not idle_match:
        raise ValueError("Log line does not contain expected CPU or idle values.")

    total_cpu = int(total_cpu_match.group(1))
    idle = int(idle_match.group(1))

    # Calculate CPU usage
    usage = total_cpu - idle
    return(float(usage//8)) # This sysytem have 8 core 

def monitor_cpu_mem():
    process = subprocess.Popen(
        ["adb", "shell", "top", "-d", "1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )


    try:
        for line in process.stdout:
            # Match CPU usage line
            if re.search(r'\d+%cpu', line):
                # print("CPU:", line.strip())
                calculate_cpu_usage(line.strip())


            # Match Memory usage line
            elif re.search(r'Mem:', line) or re.search(r'Swap:', line):
                # print("Memory:", line.strip())
                process.terminate()
    except KeyboardInterrupt:
        process.terminate()
        print("Stopped monitoring.")
    finally:    
        process.stdout.close()
        
        
if __name__ == "__main__":
    monitor_cpu_mem()