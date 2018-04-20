#! /bin/bash
docker stop mysql
docker rm mysql
docker run \
  --name mysql \
  --restart unless-stopped \
  -d \
  -p 3306:3306 \
  -e MYSQL_USER="dev" \
  -e MYSQL_PASS="divo@123" \
  -v /Users/fzx/mysql/tmp:/sql \
  registry.aliyuncs.com/fangzx/mysql_5.6

#EOP

