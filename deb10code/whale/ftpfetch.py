#!/usr/bin/python3
# fetch  latest ftp file from hydrophone
from ftplib import FTP
import os
import sys
from scipy.io import wavfile
import Whale
#
#
where='/home/debian/whale'
#
ftp=FTP('192.168.3.3')
ftp.login()
ftp.cwd('Data')
#
filelist=ftp.nlst()
f = filelist[-1]
if '00.wav' not in f:
    print (f + " is not a complete wav file")
    f = filelist[-2]
if '00.wav' not in f:
    print (f + " is not a complete wav file")
    sys.exit(1)
for d in ['data','call','nada']:
    if f in os.listdir(d):
        sys.exit(2)
# get file and call check
fname=where+'/data/'+f
with open(fname, 'wb') as fp:
    ftp.retrbinary('RETR '+f, fp.write)
fs, data = wavfile.read(fname)
result=Whale.detect_whale_call_from_audio(data, fs)
if result:
    # make an empty file with the name
    open('call/'+f, 'a').close()
    with open('message', 'a') as fp:
        fp.write(f+'\r')
else:
    open('nada/'+f, 'a').close()
os.remove('data/'+f)
sys.exit(0)
