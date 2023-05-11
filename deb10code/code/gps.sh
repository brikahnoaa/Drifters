#!/bin/bash
cd /home/debian/code
Log=gps.log
Err=gps.err
interval=555 # 10 minutes minus 45s for phonecall
date > $Log
echo $$ > pid
while [[ -f pid ]]; do
  python3 ./phonehome.py >> $Log 2> $Err
  sleep $interval
done
