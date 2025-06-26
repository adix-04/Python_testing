import testui
import pyttsx3
import Connect_DLT


def print_fun():
    print("TTS file")
    test=Connect_DLT.Connet_DLT_class("C:/Users/jithin.sreekala/AppData/Local/dlt_viewer/cache","C:/Users/jithin.sreekala/Downloads/release/release/dlt_viewer","C:/Users/jithin.sreekala/Downloads/release/release/file_DLT.dlp")

if __name__ == "__main__":

    print_fun()
    # engine = pyttsx3.init()
    # engine.setProperty("rate", 150)
    # engine.say("Hey mini what is the time ")
    # engine.runAndWait()