#coding=utf-8
import ftplib
import datetime
from string import zfill
import ConfigParser
import os

DIR = os.path.dirname(os.path.abspath(__file__))
dir_backup = "/disk1/ftp/hisdocs/aliyserverbackup"

config = ConfigParser.RawConfigParser(allow_no_value=True)
config.read(os.path.dirname(os.path.abspath(__file__)) + '/backupcfg.ini')
running_fn = "ftp-backup-running.txt"

now = datetime.datetime.now()
now_date_text = now.strftime("%Y.%m.%d")

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t).strftime("%Y.%m.%d")

def allow_remove():
  fn = os.path.join(DIR,running_fn)
  return not os.path.exists(fn)

def get_date_text(dt):
    return str(dt.year)+"."+zfill(dt.month,2)+"."+zfill(dt.day,2)

def get_date_text_add_days(date_text,days):
    seq = date_text.split('.')
    y = int(seq[0])
    m = int(seq[1])
    d = int(seq[2])
    return get_date_text(datetime.datetime(y,m,d) + datetime.timedelta(days))

def delete_old_files(ftp,keep_for_days,split_callback):
    """
    @param ftp object: ftplib.FTP instance
    @param keep_for_days int: days
    @param split_callback function:
    """
    files = ftp.nlst()
    for file in files:
        year,month,date = split_callback(file)
        if not year: continue

        if get_date_text_add_days("%s.%s.%s" % (year,month,date),keep_for_days) < now_date_text:
            try:
               ftp.delete(file)
               print("file deleted: %s" % file)
            except:
               pass

def split_callback_of_confluencedb(file):
    if not 'confluencedb' in file: return (None,None,None)

    file_parts = file.split('-')
    year = int(file_parts[1])
    month = int(file_parts[2])
    date = int(file_parts[3].replace('.sql.gz',''))
    return (year,month,date)

def split_callback_of_jiradb(file):
    if not 'jiradb' in file: return (None,None,None)

    file_parts = file.split('-')
    year = int(file_parts[1])
    month = int(file_parts[2])
    date = int(file_parts[3].replace('.sql.gz',''))
    return (year,month,date)

def split_callback_of_shaka(file):
    if not 'shaka' in file: return (None,None,None)

    file_parts = file.split('.')
    year = int(file_parts[1])
    month = int(file_parts[2])
    date = int(file_parts[3])
    return (year,month,date)

def split_callback_of_svn(file):
    if not 'his.' in file: return (None,None,None)

    file_parts = modification_date(os.path.join(dir_backup,file)).split('.')
    year = int(file_parts[0])
    month = int(file_parts[1])
    date = int(file_parts[2])
    return (year,month,date)

def delete_old_files_of_svn_temp(keep_for_days):
    dir_temp = "/disk1/backup"

    for (path,dirs,files) in os.walk(dir_temp):
      for filename in files:
        if not 'his.' in filename: continue

        fn_path = os.path.join(dir_temp,filename)
        file_parts = modification_date(fn_path).split('.')
        year = int(file_parts[0])
        month = int(file_parts[1])
        date = int(file_parts[2])

        if get_date_text_add_days("%s.%s.%s" % (year,month,date),keep_for_days) < now_date_text:
           os.remove(fn_path)

if not allow_remove():
  exit()

ftp = ftplib.FTP(config.get("ftp", 'host'))
ftp.login(config.get("ftp", 'username'), config.get("ftp", 'password'))
ftp.cwd(config.get("ftp", 'dir'))

delete_old_files(ftp,1,split_callback_of_confluencedb)
delete_old_files(ftp,1,split_callback_of_jiradb)
delete_old_files(ftp,1,split_callback_of_shaka)
delete_old_files(ftp,1,split_callback_of_svn)

delete_old_files_of_svn_temp(10)

ftp.close()

#EOP
