REAMDE
======

本机Mac
---

执行`~/mysql.sh`.

第一次运行
----------

  打开 run.sh, 进行下列设定：

  (1)设定用户名和密码(或接受默认的值）：

      -e MYSQL_USER="myuser"
      -e MYSQL_PASS="mypass"

  (2)设定目录映射（或接受默认的值）：

      -v /mysql/data:/var/lib/mysql
      -v /mysql/tmp:/sql

  (3)创建host上的映射目录：

      mkdir -p ./mysql/data ./mysql/tmp

  执行脚本创建容器：

    ./run.sh

  可以用 docker ps 查看启动的容器ID, 然后查看日志信息:

    docker logs mysql

  注意：在OSX下，不能映射 /var/lib/mysql 目录,  让其使用默认的映射。

测试能用NavicatSQL远程访问
------------------------

  第一次启动时创建的用户自动能远程访问, 用NavicatSQL进行测试。

创建数据库
----------

  保证有一个mysql docker 容器正在运行的前提下，执行：

  1. 进入容器 bash 终端：

    docker exec -it mysql bin/bash

    或 dssh mysql

  2. 进入 mysql 命令行：

    mysql -uroot

     注意：root 用户密码为空。

  3. 执行相应的命令, 如：

    create database divo3me default character set utf8;

导入数据库
----------

  保证有一个mysql docker 容器正在运行的前提下，执行：

  1. 先将要导入的数据库文件放入 /sql 对应的映射目录（如/mysql/tmp)。

  2. 进入容器 bash 终端：

    docker exec -it mysql bin/bash

    或 dssh mysql

  3. 导入

    mysql -uroot --database=divo3me < /sql/divo3me.sql

导出数据库
----------

  操作方法同“导入数据库”一节，最后的命令改为：

    mysqldump --quick --host=localhost --user=root --result-file=/sql/tmp.sql divo3me

  或者:

    docker exec mysql sh -c "mysqldump --quick --host=localhost --user=root fusion0hx | gzip > /sql/fusion0hx.sql.gz"

更新数据库
----------

  同“创建数据库”一节中的操作方法。

END


