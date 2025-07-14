import serial
from time import sleep
import argparse



parser = argparse.ArgumentParser(description='Ruetz Ibox 4.0 Host PC Controller')
parser.add_argument('-p','--port', type=str, required=True, help='Specify serial port')
parser.add_argument('--check_clamps',default=False, action="store_true", help="Check all clamp status")
parser.add_argument('--check_firmware',default=False, action="store_true", help="Check firmware version")
parser.add_argument('--start_clamps',default=False, action="store_true", help="Start all power clamps (cl30,cl30f,cl30b)")
parser.add_argument('--shutdown_clamps',default=False, action="store_true", help="Shutdown all power clamps (cl30,cl30f,cl30b)")
parser.add_argument('--turn_on',choices=['cl30', 'cl30f', 'cl30b','mute','obd'], help="Turn on clamp cl30/cl30f/cl30b/mute/obd")
parser.add_argument('--turn_off',choices=['cl30', 'cl30f', 'cl30b','mute','obd'], help="Turn off clamp cl30/cl30f/cl30b/mute/obd")
parser.add_argument('--restart',choices=['cl30', 'cl30f', 'cl30b','mute','obd'], help="Restart clamp cl30/cl30f/cl30b/mute/obd")
args = parser.parse_args()

clamps = ["cl30","cl30f","cl30b","mute","obd"]
on = {'cl30' : "HFBS0", 'cl30f' : "HFBSf", 'cl30b' : "HFBSb", 'mute' : "HFBSM",'obd' : "HFBSO"}
off = {'cl30' : "HFBC0", 'cl30f' : "HFBCf", 'cl30b' : "HFBCb", 'mute' : "HFBCM",'obd' : "HFBCO"}
status = {'cl30' : "HFBG0", 'cl30f' : "HFBGf", 'cl30b' : "HFBGb", 'mute' : "HFBGM",'obd' : "HFBGO"}

def func_clamps_action(clamp, status_clamp):
    #print (clamp)
    #print (status)
    if status_clamp == "FIRMWARE":
        ser.write(b'SV\n')
        firmware_status = ser.readline()
        print ("Firmware version: " + firmware_status.decode())
    if status_clamp == "ON":
        cmd_on = on.get(clamp, -1)
        ser.write(cmd_on.encode() + b'\n')
        print("Clamp " + clamp + " status: " + status_clamp)
    if status_clamp == "OFF":
        cmd_off = off.get(clamp, -1)
        ser.write(cmd_off.encode() + b'\n')
        print("Clamp " + clamp + " status: " + status_clamp)
    if status_clamp == "START":
        cmd_on = on.get(clamp, -1)
        ser.write(cmd_on.encode() + b'\n')
        print("Clamp " + clamp + " status: " + "ON")
    if status_clamp == "SHUTDOWN":
        cmd_off = off.get(clamp, -1)
        ser.write(cmd_off.encode() + b'\n')
        print("Clamp " + clamp + " status: " + "OFF")
    if status_clamp == "RESTART":
        cmd_off = off.get(clamp, -1)
        ser.write(cmd_off.encode() + b'\n')
        print("Clamp " + clamp + " status: " + "OFF")
        #print("Wait 1s...")
        sleep(1)
        cmd_on = on.get(clamp, -1)
        ser.write(cmd_on.encode() + b'\n')
        print("Clamp " + clamp + " status: " + "ON")
    if status_clamp == "STATUS":
        cmd_status = status.get(clamp, -1)
        ser.write(cmd_status.encode() + b'\n')
        #global status_clamps
        status_clamps = ser.readline()
        #print(status_clamps)
        #print(status_clamps.decode()[4])
        if status_clamps.decode()[4] == "1":
            status_clamps_text = "ON"
        else:
            status_clamps_text = "OFF"
        print("Clamp " + clamp + " status: " + status_clamps_text)

if __name__ == "__main__":
    try:
        serial_port = args.port
        #print (serial_port)
        # ser = serial.Serial( port=serial_port, baudrate=9600, bytesize=8, parity='N',stopbits=1,timeout = 1)
        ser = serial.Serial( port=serial_port, baudrate=115200, bytesize=8, parity='N',stopbits=1,timeout = 1)
        #print("Connected to: " + ser.portstr);
        sleep(0.1)
        if args.check_clamps is True:
            for x in clamps:
                func_clamps_action(x, "STATUS")

        if args.check_firmware is True:
            func_clamps_action(args.check_firmware, "FIRMWARE")

        if args.turn_on in clamps:
            func_clamps_action(args.turn_on, "ON")

        if args.turn_off in clamps:
            func_clamps_action(args.turn_off, "OFF")

        if args.restart in clamps:
            func_clamps_action(args.restart, "RESTART")

        if args.start_clamps is True:
            #func_restart_clamps()
            for x in clamps[:-2]:
                func_clamps_action(x, "START")

        if args.shutdown_clamps is True:
            #func_restart_clamps()
            for x in clamps[:-2]:
                func_clamps_action(x, "SHUTDOWN")

        ser.close()

    except Exception:
        print ("Can't open port: " + args.port)


# import serial

# if __name__ == '__main__':
#     try :
#         ser = serial.Serial(port='COM3',baudrate=9600)
#         print(f"connected to {ser}")
#     except serial.SerialException:
#         print("error")