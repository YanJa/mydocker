#!/usr/bin/env python
import ftplib
import os
import subprocess
import time
import yaml

# Load configuration from yaml file
f = open(os.path.dirname(os.path.abspath(__file__)) + '/mysql_backup_config.yaml')
config = yaml.load(f)

# Settings
FTP_USER    = config['ftp_user']
FTP_PASS    = str(config['ftp_pass'])
FTP_HOST    = config['ftp_host']
FILESTAMP   = time.strftime('%Y-%m-%d-%H')

def change_directory(dir):
    if (directory_exists(dir) is False):
        ftp.mkd(dir)
    ftp.cwd(dir)

def directory_exists(dir):
    filelist = []
    ftp.retrlines('LIST',filelist.append)
    return any(f.split()[-1] == dir and f.upper().startswith('D') for f in filelist)

# Ftp login
ftp = ftplib.FTP()
ftp.connect(FTP_HOST, "21")
ftp.login(FTP_USER, FTP_PASS)

# Loop each selected database, dump it and upload to ftp
for database in config['databases']:

    filename = "%s-%s.sql" % (database, FILESTAMP)
    host_filename = "/home/ubuntu/work/mysql/tmp/%s" % filename

    subprocess.call("docker exec mysql sh -c 'mysqldump -u %s -h localhost %s | gzip -9 > /sql/%s.gz'" % ('root',database, filename), shell = True)

    upfile = open("%s.gz" % host_filename, "r")
    name = "{0}/{1}.gz".format(ftp.pwd(),os.path.split(filename)[1])
    ftp.storbinary('STOR ' + name, upfile)

ftp.quit()

#EOP
