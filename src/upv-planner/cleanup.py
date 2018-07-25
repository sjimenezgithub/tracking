#! /usr/bin/env python
import sys,os

cmd=  "rm -rf *.pyc *.*~"
print cmd
os.system(cmd)

cmd=  "cd planner; ./cleanup.py; cd .."
print cmd
os.system(cmd)

sys.exit(0)

