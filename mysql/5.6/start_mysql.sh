#!/bin/bash

set -m
set -e

VOLUME_HOME="/var/lib/mysql"
CONF_FILE="/etc/mysql/conf.d/my.cnf"
LOG="/var/log/mysql/error.log"

# Set permission of config file
chmod 644 ${CONF_FILE}
chmod 644 /etc/mysql/conf.d/mysqld_charset.cnf

StartMySQL () {
    /usr/bin/mysqld_safe > /dev/null 2>&1 &

    # 没有下面一段，会出现 ERROR 2002, 无法连接
    # Time out in 1 minute
    LOOP_LIMIT=60
    for (( i=0 ; ; i++ )); do
        if [ ${i} -eq ${LOOP_LIMIT} ]; then
            echo "Time out. Error log is shown as below:"
            tail -n 100 ${LOG}
            exit 1
        fi
        echo "=> Waiting for confirmation of MySQL service startup, trying ${i}/${LOOP_LIMIT} ..."
        sleep 1
        mysql -uroot -e "status" > /dev/null 2>&1 && break
    done
}

CreateMySQLUser() {
    mysql -uroot -e "INSERT INTO mysql.user (Host,User,Password) VALUES('%','${MYSQL_USER}',PASSWORD('${MYSQL_PASS}'))"
    mysql -uroot -e "INSERT INTO mysql.user (Host,User,Password) VALUES('localhost','${MYSQL_USER}',PASSWORD('${MYSQL_PASS}'))"
    mysql -uroot -e "FLUSH PRIVILEGES"

    mysql -uroot -e "GRANT ALL PRIVILEGES ON *.* TO '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_PASS}'"
    mysql -uroot -e "GRANT ALL PRIVILEGES ON *.* TO '${MYSQL_USER}'@'%' IDENTIFIED BY '${MYSQL_PASS}'"

	echo "========================================================================"
	echo "You can now connect to this MySQL Server using:"
	echo ""
	echo "    mysql -u$MYSQL_USER -p$MYSQL_PASS -h<host> -P<port>"
	echo ""
	echo "Please remember to change the above password as soon as possible!"
	echo "MySQL user 'root' has no password but only allows local connections"
	echo "========================================================================"
}


# Initialize empty data volume and create MySQL user
if [[ ! -d $VOLUME_HOME/mysql ]]; then
    if [ ! -f /usr/share/mysql/my-default.cnf ] ; then
        cp /etc/mysql/my.cnf /usr/share/mysql/my-default.cnf
    fi
    mysql_install_db > /dev/null 2>&1
    StartMySQL
    CreateMySQLUser
else
    StartMySQL
fi

# 避免退出
tail -F $LOG &
fg %1

#EOP

