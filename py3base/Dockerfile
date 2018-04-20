FROM ubuntu:16.04

MAINTAINER Dockerfiles

# Install required packages and remove the apt packages cache when done.

RUN apt-get update && \
    apt-get upgrade -y && \ 	
    apt-get install -y \
	git \
	python3 \
	python3-dev \
	python3-setuptools \
	python3-pip \
	nginx \
	supervisor \
	sqlite3 && \
	pip3 install -U pip setuptools && \
   rm -rf /var/lib/apt/lists/*

# install uwsgi now because it takes a little while
RUN pip3 install uwsgi

# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

RUN rm /etc/nginx/sites-enabled/default
# nginx
COPY ./conf/nginx.conf /etc/nginx/conf.d/my-nginx.conf
# uwsgi
COPY ./conf/uwsgi/uwsgi.ini /opt/django/uwsgi.ini 
COPY ./conf/uwsgi/uwsgi_params:/opt/django/uwsgi_params
# supervisor
COPY ./conf/supervisor.conf /etc/supervisor/conf.d/
COPY requirements.txt /opt/django/app/
RUN pip3 install -r /opt/django/app/requirements.txt

EXPOSE 80

CMD ["supervisord", "-n"]
