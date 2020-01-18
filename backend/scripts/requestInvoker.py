import subprocess
import sys
import os
FILE = os.path.dirname(os.path.realpath(__file__))

runningTimes = 100
if (len(sys.argv) > 1):
    runningTimes = int(sys.argv[1])

cmd = os.path.join(FILE, '..', 'ic20_windows.exe')
for x in range(runningTimes):
    subprocess.run(cmd, stdout=subprocess.PIPE)
