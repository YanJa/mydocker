#! /bin/bash
FPATH=/home/fzx/work

docker stop mysql
docker rm mysql
docker run \
  --name mysql \
  --restart unless-stopped \
  --net=myapp \
  -d \
  -p 3306:3306 \
  -e MYSQL_USER="dev" \
  -e MYSQL_PASS="divo@123" \
  -v $FPATH/mysql/tmp:/sql \
  -v $FPATH/mysql/data:/var/lib/mysql \
  fangzx/mysql:5.6

# Mac下，不要映射data，只要：-v /Users/fzx/mysql/tmp:/sql \

#EOP
