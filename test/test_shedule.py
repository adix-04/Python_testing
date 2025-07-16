import subprocess
import re

def get_total_cpu_usage():
    print('run')
    try:
        # Run adb top command
        process = subprocess.run(
            ["adb", "shell", "top", "-n", "1"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if process.returncode != 0:
            raise RuntimeError(f"ADB error: {process.stderr.strip()}")

        # Find the line with %cpu (usually first few lines)
        for line in process.stdout.splitlines():
            if '%cpu' in line.lower():
                print("Found CPU line:", line.strip())

                # Extract total and idle CPU
                total_match = re.search(r'(\d+)%cpu', line)
                idle_match = re.search(r'(\d+)%idle', line)

                if total_match and idle_match:
                    total = int(total_match.group(1))
                    idle = int(idle_match.group(1))
                    usage = total - idle
                    print(f"CPU Usage: {usage}%")
                    return usage

                raise ValueError("Failed to parse total or idle CPU usage.")

        raise ValueError("No CPU line found in top output.")
    
    except Exception as e:
        print(f"Error while fetching CPU usage: {e}")
        return None
    
get_total_cpu_usage()   
if __name__ == "__main__":
    get_total_cpu_usage()
