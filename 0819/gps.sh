#!/bin/bash
cd /home/debian/code
Log=gps.log
Err=gps.err
date > $Log
python3 ./phonehome.py > $Log 2> $Err
