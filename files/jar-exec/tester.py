#!/usr/bin/python
import time
import sys

sys.stdout.write('hello!\n')
sys.stdout.flush()
s = sys.stdin.readline().strip()

while s not in ['break', 'quit']:
    sys.stdout.write('Input: "' + s + '" and output: "' + s.upper() + '"\n')
    sys.stdout.flush()
    time.sleep(2)
    sys.stdout.write('Test if it works even after I executed command')
    sys.stdout.flush()

    fo = open("tester.txt", "a")
    fo.write('Input: "' + s + '" and output: "' + s.upper() + '"\n')
    fo.close()
    s = sys.stdin.readline().strip()
