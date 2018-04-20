#
# Thanks:https://github.com/tutumcloud/mysql
#
FROM fangzx/base:1.0
MAINTAINER fangzx <499233138@qq.com>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get -yq install mysql-server-5.6

RUN rm -rf /var/lib/mysql/*
RUN rm /etc/mysql/conf.d/mysqld_safe_syslog.cnf

ADD my.cnf /etc/mysql/conf.d/my.cnf
ADD mysqld_charset.cnf /etc/mysql/conf.d/mysqld_charset.cnf

ADD start_mysql.sh /start_mysql.sh
RUN chmod 755 /*.sh

ENV MYSQL_USER dev
ENV MYSQL_PASS 123

RUN mkdir /sql
VOLUME  ["/etc/mysql", "/var/lib/mysql", "/sql"]

EXPOSE 3306
CMD ["/start_mysql.sh"]

#EOP
