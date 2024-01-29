import subprocess
import sys
import time

process = subprocess.Popen([sys.executable, "start.py"])
process.wait()
time.sleep(0.2)
process1 = subprocess.Popen([sys.executable, "OBMEN.py"])
process1.wait()
time.sleep(0.2)
process2 = subprocess.Popen([sys.executable, "GUI_client.py"])
process2.wait()