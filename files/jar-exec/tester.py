#!/usr/bin/python
import time
import sys

sys.stdout.write('hello!\n')
sys.stdout.flush()
s = sys.stdin.readline().strip()

while s not in ['break', 'quit']:
    sys.stdout.write(s.upper() + '\n')
    sys.stdout.flush()
    time.sleep(2)
    sys.stdout.write('Asynchronous output test\n')
    sys.stdout.flush()
    s = sys.stdin.readline().strip()
