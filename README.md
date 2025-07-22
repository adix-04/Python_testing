
# IDC EVO and MINI IPA Test Automation

IPA Test Automation tool to run automated voice and speech test and peform KPI's for IDV evo platforms and MINI platforms


## Tech Stack Badges

### Programming Language
![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python&logoColor=white)
### Libraries
![Pandas](https://img.shields.io/badge/Pandas-1.3.3-green?logo=pandas&logoColor=white)  ![FFmpeg](https://img.shields.io/badge/FFmpeg-4.4-red?logo=ffmpeg&logoColor=white)  ![pyttsx3](https://img.shields.io/badge/pyttsx3-2.7.1-orange?logo=python&logoColor=white)  ![gTTS](https://img.shields.io/badge/gTTS-2.2.3-green?logo=google&logoColor=white)  ![PyQt5](https://img.shields.io/badge/PyQt5-5.15.4-blue?logo=python&logoColor=white) ![openpyxl](https://img.shields.io/badge/openpyxl-3.1.5-green?logo=python&logoColor=white) 
### Tools
![ADB](https://img.shields.io/badge/ADB-1.0.41-orange?logo=android&logoColor=white)  ![DLT Viewer](https://img.shields.io/badge/DLT%20Viewer-1.0.0-blue?logo=visualstudio&logoColor=white) 
### IDE
![VS Code](https://img.shields.io/badge/VS%20Code-1.60.0-blue?logo=visual-studio-code&logoColor=white)
### Operating Systems
![Windows](https://img.shields.io/badge/Windows-10-blue?logo=windows&logoColor=white)  ![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange?logo=linux&logoColor=white)  

## Features

- ✅Text To speech engine
- 🔊Live TTS conversion
- 📱ADB Integration to run adb command to android device 
- 🧨Custom abb command injection to check maximum throughput
- 🔧DLT viewer integration to for real time logging 
- 💽pandas framework for excel read and write functions
- 💻PyQt based UI/UX for efficent user interaction

## Prerequisites

Make sure you [enabled USB debugging][enable-adb] on your device(s).
[enable-adb]: https://developer.android.com/studio/debug/dev-options#enable
The Android device must have debugging mode enabled.

There should be a connection between device and host through a USB cable for USB debugging or Ethernet cable for TCP based debugginh

- adb exe path should be added in windows path variable , we have to execute adb commands from everywhere
- dlt exe path should be the same as adb , 
- Linux dont have these problems beacaue we can call adb and dlt from anywhere, if it is not working do add it in path variables

In some cases do restart abd server and manually check if the connection can be made using adb in TCP/IP mode:

```shell
adb kill-server
adb connnect [ip]:5555
```
then check if the device is available
```shell
adb devices
```
## Usage/Examples

```shell
git clone <repo>
```
```shell
cd <repo>
```
```shell
pip install -r requirements.txt
```
- if pip fails to install all do it manually one after the other

- run the code from the ui as entrypoint
```shell
 python {runner_UI.py}
```

## License

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

**Free Software, Hell Yeah!**

## Contributions are always welcomed
