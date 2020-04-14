import sys
import json
import time
import subprocess
from jsondiff import diff

if __name__ == "__main__":
    current_json = None
    last_process = None
    while True:
        with open(r"D:\Study\AI_Competition\keyboard\BE\advanced_layout\helpers\config.json", 'r') as f:
            loaded_json = json.load(f)
            if diff(loaded_json, current_json) != {}:
                current_json = loaded_json
                if last_process is not None:
                    last_process.terminate()
                last_process = subprocess.Popen([r"C:\Users\xmolo\anaconda3\python.exe",
                                                 r"D:/Study/AI_Competition/keyboard/BE/advanced_layout/main.py",
                                                 r"D:\Study\AI_Competition\keyboard\BE\advanced_layout\helpers\config.json"])
                print("changed")
            else:
                time.sleep(1)
