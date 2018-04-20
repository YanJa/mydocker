REAMDE
======

## mysql 备份

执行 mysql_backup.py, 它使用了配置文件 mysql_backup_config.yaml.

注意：此程序只生成备份文件，并保存到本地并上传到ftp, 但不删除本地文件。

## 本地旧文件删除

## ftp 旧文件删除

## 本地文件同步到aliyun oss

1.要先安装[oss 0.4.2](https://pypi.python.org/pypi/aliyun-python-sdk-oss/0.4.2)
2.用oss_test.py测试是否可用。
3.使用了<https://github.com/mehwww/oss-sync>, 配置文件参见 .oss-sync.json.

## 本地文件同步到s3

1.要先在本地安装[boto](http://boto.readthedocs.org/en/latest/s3_tut.html)
```
sudo pip install boto
```
2.用s3_test.py测试是否可用(需要翻墙)

END

