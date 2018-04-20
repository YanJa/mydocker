README
---

## 参考资料

* <https://github.com/besnik/tutorials/tree/master/docker-mysql>
* <https://www.digitalocean.com/community/tutorials/how-to-prepare-for-your-mysql-5-7-upgrade>(升级时注意)

## 步骤

1.采用官方mysql: <https://hub.docker.com/_/mysql/>

* <https://github.com/docker-library/mysql/blob/10eb5eab8d3d793c49a701ed7a42e1e5d1c9bb59/5.7/Dockerfile>

注意：在官方Dockerfile的基础上，增加了`/sql`映射卷。

2.创建目录：

```
~/work/mysql
~/work/mysql/tmp/
~/work/mysql/data/
~/work/mysql/initdb.d/
```

3.启动.

```
-- compose

  mysql:
    image: registry.cn-hangzhou.aliyuncs.com/fangzx/mysql_5.7
    restart: unless-stopped
    environment:
      - MYSQL_ROOT_PASSWORD=KssX3sHpiM9Bno
    volumes:
    - ./conf.d:/etc/mysql/conf.d
    - ../../mysql/initdb.d:/docker-entrypoint-initdb.d
    - ../../mysql/data:/var/lib/mysql
    - ../../mysql/tmp:/sql
    ports:
      - "3306:3306" #must not change after created
```

注意：在deploy文件夹中，需要有conf.d/mysql.cnf文件.

5.如何导入数据？

```
docker exec ps_mysql_1 sh -c "mysql -uroot -p<psw> --execute='drop database sonnet2ps;'"
docker exec ps_mysql_1 sh -c "mysql -uroot -p<psw> --execute='create database sonnet2ps default character set utf8;'"

-- cp ps.sql ./mysql/tmp
docker exec ps_mysql_1 sh -c 'exec mysql -uroot -p<psw>o --database=sonnet2ps < /sql/ps.sql'
```

6.如何dump?

```
docker exec ps_mysql_1 \
    sh -c "mysqldump --quick --host=localhost -uroot -p<psw> --set-gtid-purged=OFF --result-file=/sql/ps.sql sonnet2ps"
```

7.权限控制

7.1 限制root只能本地访问(也不能被docker container访问)

```
dssh ps_mysql_1
mysql -uroot -p<psw>
mysql>use mysql;
mysql>UPDATE user SET host='localhost' WHERE user="root";
mysql>select host,user from user;
mysql>FLUSH PRIVILEGES;
```

7.2 为每个数据库创建一个用户

* 参考：<http://stackoverflow.com/questions/1720244/create-new-user-in-mysql-and-give-it-full-access-to-one-database>

```
CREATE USER 'ps'@'%' IDENTIFIED BY '<ps>';
GRANT ALL ON sonnet2ps.* TO 'ps'@'%';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'ps'@'%';

-- 删除权限
REVOKE ALL ON divo3me.* from 'ps'@'%';
```

8.其他设置

8.1 解决mysql has gone错误：<http://www.jb51.net/article/23781.htm>

```
-- mysql.cnf
max_allowed_packet=500M

8.2 加大默认的最大连接超时时间(秒)

```
-- mysql.cnf
innodb_lock_wait_timeout=300
wait_timeout=259200
```

END
