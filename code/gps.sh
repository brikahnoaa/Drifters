#!/bin/bash
cd /home/debian/code
Log=gps.log
date > $Log
echo $HOSTNAME >> $Log
python3 ./phonehome.py >> $Log 2>&1
