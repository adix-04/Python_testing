import subprocess
import os
import time
from datetime import datetime

# Configuration
device_id = 'J7S8WCZTROEQ8L9D'  # Replace with your device ID or IP
log_file = "adb_logs.log"         # Output log file name
duration = 3                      # Duration in seconds

def collect_logs():
    try:
        print(f"Starting ADB log collection for {device_id} (duration: {duration} seconds)")
        
        # Get current timestamp for the log file header
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Open log file with proper encoding
        with open(log_file, "w", encoding='ISO-8859-1') as file:
            file.write(f"ADB Log Collection - Device: {device_id} - Started at {timestamp}\n")
            file.write("="*60 + "\n\n")
            
            # Start the ADB logcat process
            process = subprocess.Popen(
                ["adb", "-s", device_id, "logcat"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1,
                encoding='ISO-8859-1'
            )
            
            # Record start time
            start_time = time.time()
            
            try:
                # Read lines for the specified duration
                while time.time() - start_time < duration:
                    line = process.stdout.readline()
                    if line:
                        file.write(line)
                        file.flush()
                    else:
                        break  # Exit if process ended
                        
            except KeyboardInterrupt:
                print("\nLog collection interrupted by user")
                
            finally:
                # Clean up the process
                process.terminate()
                try:
                    process.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    process.kill()
                
                # Add footer information
                file.write(f"\n\nLog collection completed after {duration} seconds")
                print(f"\nLogs saved to {os.path.abspath(log_file)}")
                
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        if 'process' in locals():
            process.terminate()

if __name__ == "__main__":
    collect_logs()
