#!/bin/bash
python ./mysql_backup.py
python ./local_remove.py
python ./ftp_remove.py
./oss_sync.sh
