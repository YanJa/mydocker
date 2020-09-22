#coding=utf-8
import os
from oss.oss_api import OssAPI

BUCKET_NAME = "fzx-backup"
oss = OssAPI("oss.aliyuncs.com", "", "")

part = 'crontab.txt'
part_filename = './crontab.txt'
res = oss.put_object_from_file(BUCKET_NAME, part, part_filename)
if res.status == 200:
    print "ok"
else:
    print "not ok"

#EOP

