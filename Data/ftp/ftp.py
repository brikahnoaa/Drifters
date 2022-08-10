#!/usr/bin/python3
#https://zetcode.com/python/ftp/

import ftplib

with ftplib.FTP('192.168.3.3') as ftp:
    ftp.login()
    ftp.cwd('Data')
    files = []
    ftp.retrlines('NLST', files.append)
    print(files[-4..])

# download text file
import ftplib
import os

with ftplib.FTP('ftp.debian.org') as ftp:
    file_orig = '/debian/README'
    file_copy = 'README'
    try:
        ftp.login()
        with open(file_copy, 'w') as fp:
            res = ftp.retrlines('RETR ' + file_orig, fp.write)
            if not res.startswith('226 Transfer complete'):
                print('Download failed')
                if os.path.isfile(file_copy):
                    os.remove(file_copy)

    except ftplib.all_errors as e:
        print('FTP error:', e)
        if os.path.isfile(file_copy):
            os.remove(file_copy)

