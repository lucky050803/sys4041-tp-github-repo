import random
import time
import json

# Use while in examples
import sys
sys.path.append('../huskylens')
from huskylib import HuskyLensLibrary

# Use for actual app
# from huskylens.huskylib import HuskyLensLibrary

#hl = HuskyLensLibrary("SERIAL", "/dev/ttyS0", 115200)
hl = HuskyLensLibrary("I2C","", address=0x32)

try :
    print('Sending knock...')
    print(hl.knock())
except Exception as e:
    print(f"Error {e}")
